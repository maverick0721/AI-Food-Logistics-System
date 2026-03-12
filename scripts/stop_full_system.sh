#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

stop_postgres() {
    echo "[full-stop] Stopping PostgreSQL..."

    if command -v systemctl >/dev/null 2>&1; then
        systemctl stop postgresql >/dev/null 2>&1 || true
    fi

    if command -v service >/dev/null 2>&1; then
        service postgresql stop >/dev/null 2>&1 || true
    fi

    if pg_isready -q; then
        echo "[full-stop] PostgreSQL still appears up; check privileges/service manager."
    else
        echo "[full-stop] PostgreSQL stopped."
    fi
}

if pgrep -f "backend/streaming/dispatch_consumer.py" > /dev/null 2>&1; then
    echo "[full-stop] Stopping dispatch consumer..."
    pkill -f "backend/streaming/dispatch_consumer.py" || true
fi

if pgrep -f "uvicorn backend.main:app" > /dev/null 2>&1; then
    echo "[full-stop] Stopping FastAPI..."
    pkill -f "uvicorn backend.main:app" || true
fi

echo "[full-stop] Stopping Kafka + ZooKeeper..."
"$ROOT_DIR/infra/kafka-stop.sh"

stop_postgres

echo "[full-stop] Done."
