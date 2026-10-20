"""Unit tests for Foundry agent request contract; no Azure credentials required."""
import json
import sys
import types
from unittest.mock import MagicMock, patch

frappe = types.ModuleType("frappe")
frappe.throw = lambda message: (_ for _ in ()).throw(ValueError(message))
sys.modules.setdefault("frappe", frappe)

from gamma_integration.services.foundry_client import call_agent, validate_endpoint


class Settings:
    project_endpoint = "https://example.services.ai.azure.com/api/projects/demo"
    agent_name = "proposal-agent"
    agent_version = "2"
    timeout_seconds = 60

    def get_password(self, key):
        assert key == "api_key"
        return "test-secret"


def test_endpoint_validation():
    assert validate_endpoint("https://example.services.ai.azure.com/api/projects/demo").endswith("/demo")
    for url in ("http://example.services.ai.azure.com", "https://attacker.invalid",
                "https://example.services.ai.azure.com.evil.org"):
        try:
            validate_endpoint(url)
        except ValueError:
            continue
        raise AssertionError("unsafe endpoint accepted: " + url)


def test_agent_request_contract():
    fake_response = MagicMock()
    fake_response.json.return_value = {
        "id": "resp_test", "output": [
            {"content": [{"type": "output_text", "text": '{"title":"Proposal"}'}]}]}
    with patch("gamma_integration.services.foundry_client.requests.post", return_value=fake_response) as post:
        result = call_agent(Settings(), {"name": "QTN-1", "grand_total": 250})
    assert result["response_id"] == "resp_test"
    assert json.loads(result["text"])["title"] == "Proposal"
    args, kwargs = post.call_args
    assert args[0].endswith("/openai/v1/responses")
    assert kwargs["json"]["agent_reference"] == {
        "type": "agent_reference", "name": "proposal-agent", "version": "2"}
    assert kwargs["headers"]["api-key"] == "test-secret"
