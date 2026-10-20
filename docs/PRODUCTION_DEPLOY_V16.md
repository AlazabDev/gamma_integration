# Gamma Integration v16 — Production pull and deployment gate
This release branch is intended for Frappe v16 + ERPNext v16. **A GitHub push or pull is not proof of runtime compatibility.** Install first on a cloned/staging site and verify CI before production.

## 0. Gate checks
- Verify Frappe and ERPNext are v16; verify Bench Python and Node versions match the deployed stack.
- Confirm a successful GitHub Actions run for `version-16`.
- Clone production DB/files into isolated staging, with outgoing emails, scheduled notifications and external actions disabled.
- Ensure backups and a documented rollback point. Never use `bench --site ... uninstall-app` as a rollback strategy.
- Review pre-existing property setters, site-specific custom fields, and print formats for collisions.
- Review Foundry endpoint and credentials in **AZ Foundry Settings** after installation; do not enable until live agent tests pass.

## 1. Fetch into bench (run as bench owner)
```bash
cd /home/frappe/frappe-bench
git status --short
bench version
# New app (if not already present):
bench get-app --branch version-16 https://github.com/AlazabDev/gamma_integration.git
# Existing app instead:
# git -C apps/gamma_integration fetch origin
# git -C apps/gamma_integration switch version-16
# git -C apps/gamma_integration pull --ff-only origin version-16
```
Run the appropriate **one** fetch path. This does not install the app onto a site.

## 2. Read-only preflight
```bash
bash apps/gamma_integration/scripts/preflight_v16.sh YOUR_STAGING_SITE
```

## 3. Stage and validate first
```bash
bench --site YOUR_STAGING_SITE backup --with-files
bench --site YOUR_STAGING_SITE install-app gamma_integration
bench --site YOUR_STAGING_SITE migrate
bench build --app gamma_integration
bench --site YOUR_STAGING_SITE run-tests --app gamma_integration
```
If already installed, skip `install-app`, but still run `migrate` after backing up. Run visual PDF tests for single and multi-page invoices, RTL/English, and item images. Run Quotation creation/link/unlink tests and verify the Foundry agent connectivity with approved test data. Verify no unexpected fixture changes in other DocTypes.

## 4. Production only after stage gates are green
Back up the real site and use the same tested commit SHA. For a first-time install:
```bash
bench --site YOUR_PRODUCTION_SITE backup --with-files
bench --site YOUR_PRODUCTION_SITE install-app gamma_integration
bench --site YOUR_PRODUCTION_SITE migrate
bench build --app gamma_integration
bench --site YOUR_PRODUCTION_SITE clear-cache
```
For an already-installed app, omit `install-app`. Take a maintenance window if schema migration or print format changes are involved. Do **not** run the entire block blindly against production.

## Known limitations
- Foundry agent generation has not yet been proven against a live configured Foundry endpoint.
- PDF output and visual fidelity to the user-supplied invoice reference have not yet been verified.
- Brand Kit is currently used by the custom Sales Invoice format, not all ERPNext print formats.
- Legacy Property Setter fixtures are intentionally not imported; existing site customizations are untouched.
- Deployed assets and migration on the user's production Bench have not been tested by this repository-only change.
