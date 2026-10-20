"""Explicit Foundry connection helpers; no credentials stored in the repository."""
from urllib.parse import urlparse

import frappe
import requests


def validate_endpoint(endpoint: str) -> str:
    parsed = urlparse(endpoint)
    if parsed.scheme != "https" or not parsed.hostname:
        frappe.throw("Foundry endpoint must be a valid HTTPS URL")
    if parsed.username or parsed.password or parsed.fragment:
        frappe.throw("Foundry endpoint cannot contain credentials or fragments")
    return endpoint.rstrip("/")


def check_foundry_auth(endpoint: str, api_key: str, api_version: str) -> dict:
    """Probe a configured Foundry endpoint. Does not generate any documents."""
    endpoint = validate_endpoint(endpoint)
    if not api_key:
        frappe.throw("Foundry API key is required")
    if not api_version:
        frappe.throw("API version must be specified")
    response = requests.get(
        f"{endpoint}/openai/models",
        params={"api-version": api_version},
        headers={"api-key": api_key},
        timeout=15,
    )
    response.raise_for_status()
    return {"status": "connected", "http_status": response.status_code}
