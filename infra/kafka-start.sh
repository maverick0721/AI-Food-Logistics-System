#!/usr/bin/env bash
set -euo pipefail

KAFKA_DIR="$(cd "$(dirname "$0")/kafka/current" && pwd)"
LOG_DIR="$(cd "$(dirname "$0")/kafka" && pwd)"

wait_port_open() {
    local port="$1"
    for _ in $(seq 1 30); do
        if ss -ltnp | grep -q ":${port} "; then
            return 0
        fi
        sleep 1
    done
    return 1
}

echo "[kafka-start] Cleaning up existing Kafka/ZooKeeper processes..."
"$(dirname "$0")/kafka-stop.sh" || true
sleep 2

echo "[kafka-start] Starting ZooKeeper..."
nohup "$KAFKA_DIR/bin/zookeeper-server-start.sh" "$KAFKA_DIR/config/zookeeper.properties" \
    > "$LOG_DIR/zookeeper.log" 2>&1 &

echo "[kafka-start] Waiting for ZooKeeper to be ready on port 2181..."
if wait_port_open 2181; then
    echo "[kafka-start] ZooKeeper is up."
else
    echo "[kafka-start] ERROR: ZooKeeper did not start on port 2181."
    tail -n 40 "$LOG_DIR/zookeeper.log" || true
    exit 1
fi

echo "[kafka-start] Starting Kafka broker..."
nohup "$KAFKA_DIR/bin/kafka-server-start.sh" "$KAFKA_DIR/config/server.local.properties" \
    > "$LOG_DIR/kafka.log" 2>&1 &

echo "[kafka-start] Waiting for Kafka to be ready on port 9092..."
if wait_port_open 9092; then
    echo "[kafka-start] Kafka broker is up."
else
    echo "[kafka-start] ERROR: Kafka did not start on port 9092."
    tail -n 60 "$LOG_DIR/kafka.log" || true
    exit 1
fi

echo "[kafka-start] All services running."
echo "  ZooKeeper logs : $LOG_DIR/zookeeper.log"
echo "  Kafka logs     : $LOG_DIR/kafka.log"
echo "  Bootstrap      : 127.0.0.1:9092"
