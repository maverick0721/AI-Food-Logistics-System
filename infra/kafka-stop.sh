#!/usr/bin/env bash

echo "[kafka-stop] Stopping Kafka broker..."
pkill -f "server.local.properties" 2>/dev/null && echo "[kafka-stop] Kafka stopped." || echo "[kafka-stop] Kafka was not running."

sleep 2

echo "[kafka-stop] Stopping ZooKeeper..."
pkill -f "zookeeper.properties" 2>/dev/null && echo "[kafka-stop] ZooKeeper stopped." || echo "[kafka-stop] ZooKeeper was not running."

echo "[kafka-stop] Done."
