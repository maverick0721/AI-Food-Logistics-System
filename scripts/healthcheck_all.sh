#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUN_FRONTEND_CHECKS="${RUN_FRONTEND_CHECKS:-1}"

cd "$ROOT_DIR"

echo "[healthcheck] root=$ROOT_DIR"

if [ ! -f .venv/bin/activate ]; then
  echo "[healthcheck] ERROR: .venv not found. Create env first: python3 -m venv .venv"
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "[healthcheck] running backend tests..."
python -m pytest -q

echo "[healthcheck] running backend import sweep..."
python - <<'PY'
import importlib
import pkgutil

packages = ["backend", "backend.routers", "backend.services", "backend.streaming"]
failed = []
checked = 0

for pkg_name in packages:
    pkg = importlib.import_module(pkg_name)
    paths = getattr(pkg, "__path__", None)
    if not paths:
        checked += 1
        continue
    for mod in pkgutil.walk_packages(paths, prefix=pkg.__name__ + "."):
        checked += 1
        try:
            importlib.import_module(mod.name)
        except Exception as exc:
            failed.append((mod.name, repr(exc)))

print(f"checked_modules={checked}")
if failed:
    for name, err in failed:
        print(f"IMPORT_FAIL {name} => {err}")
    raise SystemExit(1)
PY

echo "[healthcheck] probing API root..."
if curl -fsS http://127.0.0.1:8000/ >/tmp/afls_api_root.json; then
  echo "[healthcheck] api_up=yes"
  cat /tmp/afls_api_root.json
else
  echo "[healthcheck] api_up=no (start services with ./scripts/start_full_system.sh)"
fi

if [ "$RUN_FRONTEND_CHECKS" = "1" ]; then
  if command -v npm >/dev/null 2>&1; then
    echo "[healthcheck] running frontend tests..."
    (cd frontend && CI=true npm test -- --watchAll=false --runInBand)

    echo "[healthcheck] running frontend build..."
    (cd frontend && npm run build)
  else
    echo "[healthcheck] frontend checks skipped: npm not installed"
  fi
fi

echo "[healthcheck] done"
