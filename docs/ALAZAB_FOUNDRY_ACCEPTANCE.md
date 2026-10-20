# Foundry and Alazab printing acceptance checklist (Frappe 16)

## Implemented in branch
- Single DocType `AZ Foundry Settings` (endpoint, agent name/version, encrypted Password).
- `AZ Generated Proposal` record linked to source document through Dynamic Link.
- Whitelisted POST generation method, long-queue worker, status/result API.
- Foundry named-agent request via project `/openai/v1/responses` and `agent_reference`.
- Quotation actions to generate and browse linked proposal records.
- Alazab A4 Sales Invoice Jinja template and shared navy/gold CSS.
- Mocked request contract tests.

## Reference PDF inspected
- Source: user-provided Invoice.pdf (4 pages).
- Paper dimensions: 596 x 842 pt (A4).
- Columns in order: Total, Price, Qu, Item, Code, Image.
- Source repeated column headers on continuation pages.
- Final page contains totals, rules, bank details, QR, contact footer.
- Source also displays totals on page one; do not reuse the sample's totals as accounting truth.

## Incomplete: do not mark release ready
1. Verify named agent authentication and execution on *the actual Foundry project*.
2. Enforce generated-output JSON schema (currently stores raw model text).
3. Confirm full source-level permission behavior for generated results.
4. Install on disposable ERPNext v16 site; test `bench migrate`, `bench build`, and `run-tests`.
5. Compare generated PDF raster with source: table widths, row heights, continuation pages, headings, footer, and actual QR.
6. Add bank details and contact footer from Company/approved settings, not hardcoded values.
7. Add QR generation using a real business-safe destination.
8. Complete Arabic RTL, security review, and production-safe fixtures.
9. Add Entra identity authentication where API-key auth is unavailable.
10. Confirm long background worker runs and job commits on production infrastructure.

## Verification recorded
The PDF source was inspected as A4, 4 pages. **No actual application PDF render or live Foundry run has been verified.**
