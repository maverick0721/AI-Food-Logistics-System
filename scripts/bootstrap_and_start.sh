#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT_DIR/logs"
PID_DIR="$ROOT_DIR/.pids"
KAFKA_VERSION="${KAFKA_VERSION:-3.7.0}"
KAFKA_SCALA="${KAFKA_SCALA:-2.13}"
KAFKA_DIR_NAME="kafka_${KAFKA_SCALA}-${KAFKA_VERSION}"
KAFKA_BASE_DIR="$ROOT_DIR/infra/kafka"
KAFKA_ARCHIVE="$KAFKA_BASE_DIR/${KAFKA_DIR_NAME}.tgz"

mkdir -p "$LOG_DIR" "$PID_DIR" "$KAFKA_BASE_DIR"

log() {
    echo "[bootstrap] $*"
}

have_cmd() {
    command -v "$1" >/dev/null 2>&1
}

run_root() {
    if [ "$(id -u)" -eq 0 ]; then
        "$@"
        return
    fi

    if have_cmd sudo; then
        sudo "$@"
        return
    fi

    echo "[bootstrap] ERROR: Need root privileges for: $*"
    echo "[bootstrap] Re-run with sudo or as root."
    exit 1
}

wait_port_open() {
    local port="$1"
    local retries="${2:-60}"
    for _ in $(seq 1 "$retries"); do
        if python3 - "$port" <<'PY'
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

psql_as_postgres() {
    local sql="$1"
    local escaped_sql
    escaped_sql="${sql//\"/\\\"}"

    if [ "$(id -u)" -eq 0 ] && have_cmd runuser; then
        runuser -u postgres -- psql -d postgres -v ON_ERROR_STOP=1 -tAc "$sql"
        return
    fi

    if have_cmd sudo; then
        sudo -u postgres psql -d postgres -v ON_ERROR_STOP=1 -tAc "$sql"
        return
    fi

    su postgres -c "psql -d postgres -v ON_ERROR_STOP=1 -tAc \"$escaped_sql\""
}

install_system_deps() {
    local need_install=0
    for cmd in python3 pip3 node npm java psql pg_isready curl tar lsof; do
        if ! have_cmd "$cmd"; then
            need_install=1
            break
        fi
    done

    if [ "$need_install" -eq 0 ]; then
        log "System dependencies already installed."
        return
    fi

    if ! have_cmd apt-get; then
        echo "[bootstrap] ERROR: apt-get not found; please install dependencies manually."
        exit 1
    fi

    log "Installing system dependencies (node, postgres, java, utils)..."
    run_root apt-get update
    run_root env DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3-venv python3-pip nodejs npm postgresql postgresql-contrib postgresql-client \
        openjdk-17-jre-headless curl tar lsof
}

ensure_python_env() {
    cd "$ROOT_DIR"

    if [ ! -f .venv/bin/activate ]; then
        log "Creating Python virtual environment..."
        python3 -m venv .venv
    fi

    # shellcheck disable=SC1091
    source .venv/bin/activate

    log "Installing Python dependencies..."
    pip install --upgrade pip >/dev/null
    pip install -r requirements.txt
    pip install -e .
}

ensure_kafka_binaries() {
    cd "$ROOT_DIR"

    if [ -x "$KAFKA_BASE_DIR/current/bin/kafka-server-start.sh" ]; then
        log "Kafka binaries already present."
        return
    fi

    log "Downloading Kafka ${KAFKA_VERSION}..."
    if [ ! -f "$KAFKA_ARCHIVE" ]; then
        curl -fL -o "$KAFKA_ARCHIVE" "https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/${KAFKA_DIR_NAME}.tgz"
    fi

    if [ ! -d "$KAFKA_BASE_DIR/$KAFKA_DIR_NAME" ]; then
        tar -xzf "$KAFKA_ARCHIVE" -C "$KAFKA_BASE_DIR"
    fi

    ln -sfn "$KAFKA_DIR_NAME" "$KAFKA_BASE_DIR/current"

    cp "$KAFKA_BASE_DIR/current/config/server.properties" "$KAFKA_BASE_DIR/current/config/server.local.properties"
    sed -i 's|^#listeners=PLAINTEXT://:9092|listeners=PLAINTEXT://127.0.0.1:9092|' "$KAFKA_BASE_DIR/current/config/server.local.properties"
    sed -i 's|^zookeeper.connect=.*|zookeeper.connect=127.0.0.1:2181|' "$KAFKA_BASE_DIR/current/config/server.local.properties"
    sed -i 's|^log.dirs=.*|log.dirs=/tmp/kafka-logs|' "$KAFKA_BASE_DIR/current/config/server.local.properties"

    log "Kafka binaries ready."
}

ensure_postgres_ready() {
    log "Starting PostgreSQL..."
    run_root service postgresql start

    if ! wait_port_open 5432 30; then
        echo "[bootstrap] ERROR: PostgreSQL did not open on 5432."
        exit 1
    fi

    log "Ensuring application DB user and database exist..."
    if ! psql_as_postgres "SELECT 1 FROM pg_roles WHERE rolname='food_app';" | grep -q 1; then
        psql_as_postgres "CREATE USER food_app WITH PASSWORD 'food_app_dev';"
    fi

    if ! psql_as_postgres "SELECT 1 FROM pg_database WHERE datname='food_delivery_ai';" | grep -q 1; then
        psql_as_postgres "CREATE DATABASE food_delivery_ai OWNER food_app;"
    fi

    psql_as_postgres "GRANT ALL PRIVILEGES ON DATABASE food_delivery_ai TO food_app;" >/dev/null
}

start_backend_stack() {
    cd "$ROOT_DIR"
    log "Starting backend stack (Kafka + FastAPI + consumer)..."
    ./scripts/start_full_system.sh
}

start_frontend() {
    cd "$ROOT_DIR/frontend"

    if [ ! -d node_modules ]; then
        log "Installing frontend dependencies..."
        npm install
    fi

    if pgrep -f "react-scripts start" >/dev/null 2>&1; then
        log "Frontend already running."
        return
    fi

    log "Starting frontend on port 3000..."
    nohup npm start > "$LOG_DIR/frontend.log" 2>&1 &
    echo $! > "$PID_DIR/frontend.pid"

    if ! wait_port_open 3000 60; then
        echo "[bootstrap] ERROR: Frontend did not start on port 3000."
        tail -n 80 "$LOG_DIR/frontend.log" || true
        exit 1
    fi
}

main() {
    install_system_deps
    ensure_python_env
    ensure_kafka_binaries
    ensure_postgres_ready
    start_backend_stack
    start_frontend

    echo
    log "All services are running."
    echo "  Frontend      : http://127.0.0.1:3000"
    echo "  API           : http://127.0.0.1:8000"
    echo "  API docs      : http://127.0.0.1:8000/docs"
    echo "  PostgreSQL    : 127.0.0.1:5432"
    echo "  Kafka         : 127.0.0.1:9092"
    echo "  Logs          : $LOG_DIR"
    echo
    log "Stop all services with: ./scripts/stop_demo.sh"
}

main "$@"
