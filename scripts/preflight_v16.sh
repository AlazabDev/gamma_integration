#!/usr/bin/env bash
# Read-only preflight for a Frappe v16/ERPNext v16 Bench. No installation or migration.
set -euo pipefail
SITE="${1:-}"
if [[ -z "$SITE" ]]; then echo "Usage: bash apps/gamma_integration/scripts/preflight_v16.sh SITE_NAME" >&2; exit 2; fi
if [[ ! -d apps/frappe || ! -d apps/erpnext ]]; then echo "FAIL: execute from bench root with frappe and erpnext apps" >&2; exit 1; fi
if [[ ! -d "sites/$SITE" ]]; then echo "FAIL: site not found: $SITE" >&2; exit 1; fi
echo "=== Bench versions ==="
bench version
echo "=== Installed apps ==="
bench --site "$SITE" list-apps
echo "=== Python ==="
./env/bin/python --version
echo "=== Node ==="
node --version
echo "=== Git branch/changes ==="
git -C apps/gamma_integration branch --show-current
git -C apps/gamma_integration status --short
echo "=== Python compile (no DB change) ==="
./env/bin/python -m compileall -q apps/gamma_integration/gamma_integration
echo "=== App fixtures scope ==="
./env/bin/python - <<'PY'
import ast
from pathlib import Path
tree=ast.parse(Path("apps/gamma_integration/gamma_integration/hooks.py").read_text())
fixture=[x.value for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="fixtures" for t in x.targets)]
assert len(fixture)==1
data=ast.literal_eval(fixture[0])
assert all(isinstance(f,dict) and f.get("dt")=="Custom Field" for f in data), data
print("PASS: only scoped Gamma Custom Fields exported")
PY
echo "PREFLIGHT COMPLETE — read-only; installation/migration not attempted"
