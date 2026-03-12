#!/usr/bin/env bash
set -euo pipefail

stop_by_pattern() {
	local pattern="$1"
	if pgrep -f "$pattern" > /dev/null 2>&1; then
		pkill -f "$pattern" || true
	fi
}

wait_port_closed() {
	local port="$1"
	for _ in $(seq 1 20); do
		if ! ss -ltnp | grep -q ":${port} "; then
			return 0
		fi
		sleep 1
	done
	return 1
}

echo "[kafka-stop] Stopping Kafka broker..."
stop_by_pattern "server.local.properties"
stop_by_pattern "kafka.Kafka"
stop_by_pattern "kafka-server-start.sh"

if wait_port_closed 9092; then
	echo "[kafka-stop] Kafka stopped."
else
	echo "[kafka-stop] Kafka may still be running on port 9092."
fi

sleep 2

echo "[kafka-stop] Stopping ZooKeeper..."
stop_by_pattern "zookeeper.properties"
stop_by_pattern "QuorumPeerMain"
stop_by_pattern "zookeeper-server-start.sh"

if wait_port_closed 2181; then
	echo "[kafka-stop] ZooKeeper stopped."
else
	echo "[kafka-stop] ZooKeeper may still be running on port 2181."
fi

echo "[kafka-stop] Done."
