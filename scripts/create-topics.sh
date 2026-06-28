#!/usr/bin/env bash
set -euo pipefail

BROKER="${KAFKA_BROKERS:-localhost:9092}"

docker compose exec kafka kafka-topics --create \
  --if-not-exists \
  --bootstrap-server "$BROKER" \
  --topic raw-prompts \
  --partitions 3 \
  --replication-factor 1

docker compose exec kafka kafka-topics --create \
  --if-not-exists \
  --bootstrap-server "$BROKER" \
  --topic finished-prompts \
  --partitions 3 \
  --replication-factor 1

echo "Topics ready: raw-prompts, finished-prompts"
