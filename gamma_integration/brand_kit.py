"""Read-only, sanitized Brand Kit context for Jinja print templates."""
import re
import frappe

DEFAULTS = {
    "brand_name": "Alazab", "website": "https://al-azab.co",
    "primary_color": "#030957", "accent_color": "#FFB900",
    "surface_color": "#F8F8F8", "text_color": "#170D02",
    "border_color": "#E7E7E7", "font_family_latin": "Arial",
    "font_family_arabic": "Noto Sans Arabic", "heading_weight": "800",
    "body_size": 11, "print_language": "ar", "paper_size": "A4",
    "show_product_images": 1, "show_qr": 1,
}
PUBLIC_FIELDS = tuple(DEFAULTS) + (
    "logo", "logo_dark", "favicon", "legal_name", "contact_address",
    "contact_phone", "contact_email", "tax_id", "bank_name",
    "bank_account_name", "bank_account_number", "bank_swift", "footer_note",
)
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
FONTS = {"Arial", "Inter", "Liberation Sans", "Noto Sans Arabic", "Cairo", "Tahoma"}


def get_print_brand():
    """Jinja method. Never exposes secrets, credentials, or unrestricted DocType fields."""
    values = DEFAULTS.copy()
    if frappe.db.exists("DocType", "AZ Brand Kit"):
        doc = frappe.get_single("AZ Brand Kit")
        values.update({field: doc.get(field) for field in PUBLIC_FIELDS if doc.get(field) is not None})
    for field in ("primary_color", "accent_color", "surface_color", "text_color", "border_color"):
        if not HEX.fullmatch(str(values.get(field) or "")):
            values[field] = DEFAULTS[field]
    for field in ("font_family_latin", "font_family_arabic"):
        if values.get(field) not in FONTS:
            values[field] = DEFAULTS[field]
    if str(values.get("heading_weight")) not in ("600", "700", "800"):
        values["heading_weight"] = "800"
    values["body_size"] = max(9, min(18, int(values.get("body_size") or 11)))
    for field in ("logo", "logo_dark", "favicon"):
        if not str(values.get(field) or "").startswith(("/files/", "/private/files/", "/assets/")):
            values[field] = ""
    return values
