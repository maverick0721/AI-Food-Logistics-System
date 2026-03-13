#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT_DIR/logs"
PID_DIR="$ROOT_DIR/.pids"

mkdir -p "$LOG_DIR" "$PID_DIR"

wait_port_open() {
    local port="$1"
    for _ in $(seq 1 30); do
        if python - "$port" <<'PY'
import socket
import sys

port = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.4)
try:
    sys.exit(0 if s.connect_ex(("127.0.0.1", port)) == 0 else 1)
finally:
    s.close()
PY
        then
            return 0
        fi
        sleep 1
    done
    return 1
}

start_postgres() {
    echo "[full-start] Ensuring PostgreSQL is running..."

    if command -v pg_isready >/dev/null 2>&1 && pg_isready -q; then
        echo "[full-start] PostgreSQL is already running."
        return 0
    fi

    if command -v systemctl >/dev/null 2>&1; then
        systemctl start postgresql >/dev/null 2>&1 || true
    fi

    if command -v pg_isready >/dev/null 2>&1 && ! pg_isready -q && command -v service >/dev/null 2>&1; then
        service postgresql start >/dev/null 2>&1 || true
    fi

    if ! wait_port_open 5432; then
        echo "[full-start] ERROR: PostgreSQL did not start on port 5432."
        exit 1
    fi

    echo "[full-start] PostgreSQL is up on port 5432."
}

stop_port_holder() {
    local port="$1"
    local pids
    pids="$(lsof -ti tcp:${port} 2>/dev/null | sort -u || true)"
    if [ -n "$pids" ]; then
        echo "[full-start] Releasing port ${port} from existing process(es): $pids"
        kill $pids || true
        sleep 1
    fi
}

echo "[full-start] Starting Kafka + ZooKeeper..."
"$ROOT_DIR/infra/kafka-start.sh"

start_postgres

# Restart API if an old process is already running.
if pgrep -f "uvicorn backend.main:app" > /dev/null 2>&1; then
    echo "[full-start] Stopping existing FastAPI process..."
    pkill -f "uvicorn backend.main:app" || true
    sleep 1
fi

stop_port_holder 8000

# Restart dispatch consumer if already running.
if pgrep -f "backend/streaming/dispatch_consumer.py" > /dev/null 2>&1; then
    echo "[full-start] Stopping existing dispatch consumer..."
    pkill -f "backend/streaming/dispatch_consumer.py" || true
    sleep 1
fi

cd "$ROOT_DIR"
source .venv/bin/activate

echo "[full-start] Starting FastAPI..."
nohup python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload \
    > "$LOG_DIR/fastapi.log" 2>&1 &
echo $! > "$PID_DIR/fastapi.pid"

if ! wait_port_open 8000; then
    echo "[full-start] ERROR: FastAPI did not start on port 8000."
    tail -n 60 "$LOG_DIR/fastapi.log" || true
    exit 1
fi

echo "[full-start] Starting dispatch consumer..."
nohup python -u backend/streaming/dispatch_consumer.py \
    > "$LOG_DIR/dispatch_consumer.log" 2>&1 &
echo $! > "$PID_DIR/dispatch_consumer.pid"

sleep 2
if ! pgrep -f "backend/streaming/dispatch_consumer.py" > /dev/null 2>&1; then
    echo "[full-start] ERROR: Dispatch consumer exited during startup."
    tail -n 60 "$LOG_DIR/dispatch_consumer.log" || true
    exit 1
fi

echo "[full-start] Service status:"
for port in 5432 8000 9092; do
    if wait_port_open "$port"; then
        echo "  - port ${port}: open"
    else
        echo "  - port ${port}: closed"
    fi
done

echo

echo "[full-start] Ready."
echo "  API          : http://127.0.0.1:8000"
echo "  API docs     : http://127.0.0.1:8000/docs"
echo "  PostgreSQL   : 127.0.0.1:5432"
echo "  Kafka        : 127.0.0.1:9092"
echo "  API log      : $LOG_DIR/fastapi.log"
echo "  Consumer log : $LOG_DIR/dispatch_consumer.log"
echo

echo "[full-start] Test command:"
echo "  curl -X POST http://127.0.0.1:8000/orders -H 'Content-Type: application/json' -d '{\"user_id\":1,\"restaurant_id\":1,\"item\":\"burger\"}'"
echo

echo "[full-start] Watch consumer output:"
echo "  tail -f $LOG_DIR/dispatch_consumer.log"
