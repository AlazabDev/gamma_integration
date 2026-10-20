# Alazab Brand Kit — Frappe 16

Settings DocType: **AZ Brand Kit** (Single), System Manager only.

Default palette: primary navy `#030957`, gold `#FFB900`, surface `#F8F8F8`, white `#FFFFFF`, text `#170D02`, border `#E7E7E7`.

## Set up

1. Run `bench --site YOUR_SITE migrate` after pulling `version-16`.
2. Open **AZ Brand Kit** in Frappe Desk.
3. Upload approved logo and optional alternate mark through the Attach Image fields.
4. Configure contact, legal, tax and bank data; no example invoice bank/tax numbers are preloaded.
5. Select the **AZ Alazab Invoice** print format to check rendering on a real Sales Invoice.

The Brand Kit controls CSS design tokens and the invoice footer/header. Customer, item and accounting figures always come from ERPNext. Logo files must be uploaded to the Frappe site. No font binaries are redistributed.

## Boundaries

The sample Invoice.pdf is a visual reference, not a source of trustworthy bank balances, tax IDs or accounting totals. Test HTML/PDF pagination and the installed site's Jinja environment before production adoption. The Brand Kit does not automatically restyle every native ERPNext print format; each format must explicitly include the shared template.
