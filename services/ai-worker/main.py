"""AI worker: consumes raw-prompts, runs inference, produces finished-prompts."""

import json
import os
import signal
import time
from datetime import datetime, timezone

from confluent_kafka import Consumer, KafkaError, Producer

running = True


def env_or_default(key: str, fallback: str) -> str:
    value = os.getenv(key)
    return value if value else fallback


def mock_inference(prompt: str) -> str:
    time.sleep(2)
    return f"Echo: {prompt}"


def build_finished_job(job: dict, result: str) -> dict:
    return {
        **job,
        "result": result,
        "status": "completed",
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }


def create_consumer(brokers: str, topic_in: str) -> Consumer:
    return Consumer(
        {
            "bootstrap.servers": brokers,
            "group.id": "ai-worker",
            "enable.auto.commit": False,
            "auto.offset.reset": "earliest",
        }
    )


def create_producer(brokers: str) -> Producer:
    return Producer({"bootstrap.servers": brokers})


def handle_shutdown(_signum: int, _frame: object) -> None:
    global running
    running = False


def process_message(
    producer: Producer,
    topic_out: str,
    payload: bytes,
) -> None:
    job = json.loads(payload.decode("utf-8"))
    prompt = job["prompt"]
    job_id = job["job_id"]

    result = mock_inference(prompt)
    finished_job = build_finished_job(job, result)
    encoded = json.dumps(finished_job).encode("utf-8")

    producer.produce(
        topic_out,
        key=job_id.encode("utf-8"),
        value=encoded,
    )
    producer.flush()
    print(f"processed job_id={job_id}")


def run_worker(brokers: str, topic_in: str, topic_out: str) -> None:
    consumer = create_consumer(brokers, topic_in)
    producer = create_producer(brokers)
    consumer.subscribe([topic_in])

    print(f"ai-worker listening on {topic_in}, producing to {topic_out}")

    while running:
        message = consumer.poll(1.0)
        if message is None:
            continue
        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                continue
            raise RuntimeError(message.error())

        process_message(producer, topic_out, message.value())
        consumer.commit(message)

    consumer.close()
    print("ai-worker stopped")


def main() -> None:
    brokers = env_or_default("KAFKA_BROKERS", "localhost:9092")
    topic_in = env_or_default("KAFKA_TOPIC_RAW", "raw-prompts")
    topic_out = env_or_default("KAFKA_TOPIC_FINISHED", "finished-prompts")

    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        run_worker(brokers, topic_in, topic_out)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
