"""Brand kit tests executed with bench --site SITE run-tests --app gamma_integration."""
import re
import frappe
from frappe.tests.utils import FrappeTestCase
from gamma_integration.brand_kit import DEFAULTS, get_print_brand

class TestAZBrandKit(FrappeTestCase):
    def test_default_colors_are_valid(self):
        for key in ("primary_color", "accent_color", "surface_color", "text_color", "border_color"):
            self.assertRegex(DEFAULTS[key], r"^#[0-9A-Fa-f]{6}$")

    def test_print_context_uses_sanitized_colors(self):
        result = get_print_brand()
        for key in ("primary_color", "accent_color", "surface_color", "text_color", "border_color"):
            self.assertTrue(re.fullmatch(r"#[0-9A-Fa-f]{6}", result[key]))
        self.assertNotIn("api_key", result)

    def test_settings_access_restricted(self):
        meta = frappe.get_meta("AZ Brand Kit")
        self.assertTrue(meta.issingle)
        self.assertTrue(any(p.role == "System Manager" and p.write for p in meta.permissions))
