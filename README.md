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

From the repo root:

```bash
cd path/to/kafka-go-python-demo
cp .env.example .env
docker compose up -d
./scripts/create-topics.sh
go run ./services/gateway/cmd
go run ./services/result-consumer/cmd
python services/ai-worker/main.py
```

See [docs/architecture.md](docs/architecture.md) for the full data path.

## Send a test message

Publishing to `raw-prompts` alone does **not** fill `finished-prompts`. Something
must consume the input topic and produce to the output topic — the Python
`ai-worker` does that.

**Run all commands below from the repo root** (the folder that contains
`docker-compose.yml`). If you see `no configuration file provided: not found`,
`cd` into the project first:

```bash
cd path/to/kafka-go-python-demo
```

### 1. Start infrastructure

```bash
docker compose up -d
./scripts/create-topics.sh
```

### 2. Start the ai-worker

In one terminal, install deps once then run the worker:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r services/ai-worker/requirements.txt
python services/ai-worker/main.py
```

Leave this running. You should see `ai-worker listening on raw-prompts...`.

### 3. Watch the output topic

In a second terminal:

```bash
docker compose exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic finished-prompts \
  --from-beginning
```

Leave this running.

### 4. Publish a raw prompt (simulates the gateway)

In a third terminal, produce a job to `raw-prompts`:

```bash
echo '{"job_id":"550e8400-e29b-41d4-a716-446655440000","prompt":"Hello, Kafka!","status":"pending","created_at":"2026-06-28T12:00:00Z"}' \
  | docker compose exec -T kafka kafka-console-producer \
      --bootstrap-server localhost:9092 \
      --topic raw-prompts
```

After ~2 seconds (mock inference), you should see:

- `processed job_id=...` in the ai-worker terminal
- the finished JSON in the `finished-prompts` consumer terminal

### 5. HTTP flow (coming soon)

When the gateway is implemented, submitting and polling will look like:

```bash
# Submit a prompt — returns 202 + job_id
curl -X POST http://localhost:8080/submit \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello, Kafka!"}'

# Poll for the result
curl http://localhost:8080/result/{job_id}
```

Message shape is defined in [`schemas/prompt_job.json`](schemas/prompt_job.json).
