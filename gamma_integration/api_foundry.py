"""Whitelisted document generation endpoints for Gamma Integration."""
import json
import frappe
from frappe import _
from gamma_integration.services.foundry_client import call_agent, validate_endpoint

SUPPORTED = ("Quotation", "Sales Invoice", "Sales Order", "Purchase Order", "Delivery Note")


@frappe.whitelist()
def test_foundry_connection():
    frappe.only_for("System Manager")
    settings = frappe.get_single("AZ Foundry Settings")
    if not settings.enabled:
        frappe.throw(_("Foundry integration is disabled"))
    return {"status": "configured", "endpoint": validate_endpoint(settings.project_endpoint),
            "agent": settings.agent_name, "key_present": bool(settings.get_password("api_key"))}


@frappe.whitelist()
def generate_document(source_doctype, source_name):
    if frappe.request.method != "POST":
        frappe.throw(_("POST required"))
    if source_doctype not in SUPPORTED:
        frappe.throw(_("Unsupported source document"))
    source = frappe.get_doc(source_doctype, source_name)
    source.check_permission("read")
    settings = frappe.get_single("AZ Foundry Settings")
    if not settings.enabled:
        frappe.throw(_("Foundry integration is disabled"))
    job = frappe.get_doc({"doctype": "AZ Generated Proposal", "source_doctype": source_doctype,
        "source_name": source_name, "title": _("AI Proposal for {0}").format(source_name),
        "status": "Queued", "generated_by": frappe.session.user})
    job.insert(ignore_permissions=True)
    frappe.enqueue("gamma_integration.api_foundry.run_generation",
                   queue="long", job_name="gamma-proposal-" + job.name,
                   proposal_name=job.name, enqueue_after_commit=True)
    return {"proposal": job.name, "status": "Queued"}


def run_generation(proposal_name):
    proposal = frappe.get_doc("AZ Generated Proposal", proposal_name)
    try:
        doc = frappe.get_doc(proposal.source_doctype, proposal.source_name)
        item_rows = []
        for item in doc.get("items") or []:
            item_rows.append({"item_code": item.get("item_code"),
                "description": item.get("description"), "qty": item.get("qty"),
                "rate": item.get("rate"), "amount": item.get("amount")})
        payload = {"doctype": doc.doctype, "name": doc.name,
                   "party": doc.get("customer_name") or doc.get("supplier_name") or "",
                   "currency": doc.get("currency"), "company": doc.get("company"),
                   "items": item_rows, "net_total": doc.get("net_total"),
                   "taxes": doc.get("total_taxes_and_charges"),
                   "grand_total": doc.get("grand_total")}
        result = call_agent(frappe.get_single("AZ Foundry Settings"), payload)
        proposal.content_json = result["text"]
        proposal.foundry_response_id = result["response_id"]
        proposal.status = "Completed"
    except Exception:
        proposal.status = "Failed"
        proposal.error_message = "Foundry generation failed; inspect server error log"
        frappe.log_error(title="Gamma Foundry generation failure", message=frappe.get_traceback())
    proposal.save(ignore_permissions=True)


@frappe.whitelist()
def get_generated_document(proposal_name):
    proposal = frappe.get_doc("AZ Generated Proposal", proposal_name)
    proposal.check_permission("read")
    source = frappe.get_doc(proposal.source_doctype, proposal.source_name)
    source.check_permission("read")
    return {"name": proposal.name, "status": proposal.status,
            "content": proposal.content_json if proposal.status == "Completed" else None,
            "error": proposal.error_message if proposal.status == "Failed" else None}
