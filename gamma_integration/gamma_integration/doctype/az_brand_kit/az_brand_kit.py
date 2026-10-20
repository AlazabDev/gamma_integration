import re
import frappe
from frappe.model.document import Document

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")

class AZBrandKit(Document):
    def validate(self):
        for field in ("primary_color", "accent_color", "surface_color", "text_color", "border_color"):
            value = self.get(field)
            if value and not HEX.fullmatch(value):
                frappe.throw(f"{field} must use #RRGGBB hexadecimal notation")
        for field in ("logo", "logo_dark", "favicon"):
            value = (self.get(field) or "").strip()
            if value and not value.startswith(("/files/", "/private/files/", "/assets/")):
                frappe.throw(f"{field} must be a file uploaded to this Frappe site")
