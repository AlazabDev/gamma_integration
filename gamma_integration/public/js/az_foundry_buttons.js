frappe.ui.form.on("Quotation", {
  refresh(frm) {
    if (frm.is_new()) return;
    frm.add_custom_button(__("Generate AI Proposal"), () => {
      frappe.call({
        method: "gamma_integration.api_foundry.generate_document",
        args: {source_doctype: frm.doctype, source_name: frm.doc.name},
        freeze: true,
        callback(r) {
          if (!r.message || !r.message.proposal) return;
          frappe.show_alert({message: __("Proposal generation queued"), indicator: "blue"});
          frappe.set_route("Form", "AZ Generated Proposal", r.message.proposal);
        }
      });
    }, __("Gamma"));
    frm.add_custom_button(__("AI Proposals"), () => {
      frappe.set_route("List", "AZ Generated Proposal", {
        source_doctype: frm.doctype,
        source_name: frm.doc.name
      });
    }, __("Gamma"));
  }
});
