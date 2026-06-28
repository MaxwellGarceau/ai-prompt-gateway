# AI Prompt Gateway — Architecture

Async polyglot pipeline: Go at the edge, Kafka as the buffer, Python for heavy inference.

## Repository layout

```
kafka-go-python-demo/
├── docker-compose.yml           # Kafka, Zookeeper, Redis
├── schemas/prompt_job.json      # Shared event contract
├── scripts/create-topics.sh     # Topic bootstrap
├── services/
│   ├── gateway/cmd/main.go      # POST /submit, GET /result/{id}
│   ├── result-consumer/cmd/main.go
│   └── ai-worker/main.py
└── docs/architecture.md
```

## Data path

1. Client → `POST /submit` (gateway) → Kafka `raw-prompts` → `202` + `job_id`
2. Python worker consumes `raw-prompts` → inference → Kafka `finished-prompts`
3. Go result consumer → Redis/cache
4. Client → `GET /result/{job_id}` (gateway) → `200` or pending

## Run entrypoints

```bash
# Terminal 1 — processes raw-prompts -> finished-prompts
pip install -r services/ai-worker/requirements.txt
python services/ai-worker/main.py

# Terminal 2 — scaffold only for now
go run ./services/gateway/cmd
go run ./services/result-consumer/cmd
```
