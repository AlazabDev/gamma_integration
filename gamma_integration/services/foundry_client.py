"""Microsoft Foundry project Responses API integration using a named prompt agent."""
import json
from urllib.parse import urlparse

import frappe
import requests

ALLOWED_HOST_SUFFIXES = (".services.ai.azure.com", ".openai.azure.com")


def validate_endpoint(value):
    parsed = urlparse((value or "").strip())
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        frappe.throw("A valid HTTPS Foundry endpoint is required")
    if not parsed.hostname.lower().endswith(ALLOWED_HOST_SUFFIXES):
        frappe.throw("Foundry endpoint must be an Azure Foundry host")
    if parsed.query or parsed.fragment:
        frappe.throw("Foundry endpoint cannot contain query or fragment")
    return value.rstrip("/").removesuffix("/openai/v1")


def call_agent(settings, document_payload):
    endpoint = validate_endpoint(settings.project_endpoint)
    key = settings.get_password("api_key")
    if not key:
        frappe.throw("Configure the Foundry API key before running the agent")
    if not settings.agent_name:
        frappe.throw("Foundry agent name is required")
    reference = {"type": "agent_reference", "name": settings.agent_name}
    if settings.agent_version:
        reference["version"] = settings.agent_version
    body = {
        "agent_reference": reference,
        "input": [
            {"role": "user", "content": "Prepare a professional structured proposal in JSON. "
             "Never change financial values or invent missing facts. Source document follows:\n"
             + json.dumps(document_payload, ensure_ascii=False)}
        ]
    }
    response = requests.post(
        endpoint + "/openai/v1/responses",
        headers={"api-key": key, "Content-Type": "application/json"},
        json=body,
        timeout=min(max(int(settings.timeout_seconds or 90), 10), 180),
    )
    response.raise_for_status()
    output = response.json()
    texts = [part.get("text", "") for item in output.get("output", [])
             for part in item.get("content", []) if part.get("type") == "output_text"]
    result = "\n".join(texts).strip()
    if not result:
        frappe.throw("Foundry returned no text content")
    return {"response_id": output.get("id"), "text": result}
