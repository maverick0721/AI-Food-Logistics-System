#!/usr/bin/env bash
set -e

KAFKA_DIR="$(cd "$(dirname "$0")/kafka/current" && pwd)"
LOG_DIR="$(cd "$(dirname "$0")/kafka" && pwd)"

# Stop any existing instances cleanly
if pgrep -f "zookeeper.properties" > /dev/null 2>&1; then
    echo "[kafka-start] Stopping existing ZooKeeper..."
    pkill -f "zookeeper.properties" || true
    sleep 2
fi

if pgrep -f "server.local.properties" > /dev/null 2>&1; then
    echo "[kafka-start] Stopping existing Kafka broker..."
    pkill -f "server.local.properties" || true
    sleep 2
fi

echo "[kafka-start] Starting ZooKeeper..."
nohup "$KAFKA_DIR/bin/zookeeper-server-start.sh" "$KAFKA_DIR/config/zookeeper.properties" \
    > "$LOG_DIR/zookeeper.log" 2>&1 &

echo "[kafka-start] Waiting for ZooKeeper to be ready on port 2181..."
for i in $(seq 1 20); do
    if ss -ltnp | grep -q ':2181 '; then
        echo "[kafka-start] ZooKeeper is up."
        break
    fi
    sleep 1
done

echo "[kafka-start] Starting Kafka broker..."
nohup "$KAFKA_DIR/bin/kafka-server-start.sh" "$KAFKA_DIR/config/server.local.properties" \
    > "$LOG_DIR/kafka.log" 2>&1 &

echo "[kafka-start] Waiting for Kafka to be ready on port 9092..."
for i in $(seq 1 20); do
    if ss -ltnp | grep -q ':9092 '; then
        echo "[kafka-start] Kafka broker is up."
        break
    fi
    sleep 1
done

echo "[kafka-start] All services running."
echo "  ZooKeeper logs : $LOG_DIR/zookeeper.log"
echo "  Kafka logs     : $LOG_DIR/kafka.log"
echo "  Bootstrap      : 127.0.0.1:9092"
