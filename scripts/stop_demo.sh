#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[demo-stop] Stopping frontend..."
if [ -f "$ROOT_DIR/.pids/frontend.pid" ]; then
    pid="$(cat "$ROOT_DIR/.pids/frontend.pid" || true)"
    if [ -n "${pid}" ] && kill -0 "$pid" >/dev/null 2>&1; then
        kill "$pid" || true
    fi
    rm -f "$ROOT_DIR/.pids/frontend.pid"
fi

if pgrep -f "react-scripts start" >/dev/null 2>&1; then
    pkill -f "react-scripts start" || true
fi

echo "[demo-stop] Stopping backend stack..."
"$ROOT_DIR/scripts/stop_full_system.sh"

echo "[demo-stop] Done."
