"""AI worker: consumes raw-prompts, runs inference, produces finished-prompts."""

import os
import sys


def main() -> None:
    topic_in = os.getenv("KAFKA_TOPIC_RAW", "raw-prompts")
    topic_out = os.getenv("KAFKA_TOPIC_FINISHED", "finished-prompts")
    print(f"AI Prompt Gateway — ai-worker (in={topic_in}, out={topic_out})")
    print("not yet implemented")
    sys.exit(0)


if __name__ == "__main__":
    main()
