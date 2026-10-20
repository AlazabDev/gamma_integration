# Alazab Brand Kit — Design Rules

## Palette
- Primary headings & table header: **#030957**
- Accent, dividers and highlighted totals: **#FFB900**
- Surface: **#F8F8F8**; paper: **#FFFFFF**
- Text: **#170D02**; borders: **#E7E7E7**
- Success: **#008000**; danger: **#DC2626**

## Typography
- Arabic: Noto Sans Arabic, then Tahoma fallback.
- Latin: Arial, then Inter fallback.
- Regular content weight 400; headings 700–800.
- Body size defaults to 11 px in legacy print layout; adjust according to actual PDF preview and print engine.

## Icons
- Build *two* assets for every icon: 16×16 and 24×24 viewBox.
- Use outline strokes at consistent thickness (1.5 or 2), corner radius and optical alignment.
- Main stroke must be navy or gold; no arbitrary brand colors or embedded raster text.
- Keep accessibility title or adjacent label in UI; icons must not be the only semantic indicator.

## Documents
- Preserve six-column item layout for invoices with an explicit image column.
- Repeat table headers across multipage output; avoid row fragmentation.
- Totals and taxes must come from ERPNext, never from agents or mock data.
- Print in Arabic (RTL) or English (LTR) according to document language. Verify mixed numerals and SKU codes.
- Approved logos must be uploaded via AZ Brand Kit settings; no generated surrogate logo is allowed.

## Extension to additional print formats
Other ERPNext formats must opt into the shared base template. Adding the CSS file alone does **not** replace existing print formats.
