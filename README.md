# AI Prompt Gateway

Kafka-backed async prompt pipeline (Go + Python monorepo).

## Structure

| Path | Role |
|------|------|
| `services/gateway/` | HTTP API, Kafka producer, result polling |
| `services/result-consumer/` | Consumes `finished-prompts`, writes cache |
| `services/ai-worker/` | Consumes `raw-prompts`, runs inference |
| `schemas/` | Shared JSON event contracts |
| `scripts/` | Local dev helpers |
| `docs/` | Architecture notes |

## Quick start (scaffold)

```bash
cp .env.example .env
docker compose up -d
go run ./services/gateway/cmd
go run ./services/result-consumer/cmd
python services/ai-worker/main.py
```
See [docs/architecture.md](docs/architecture.md) for the full data path.
