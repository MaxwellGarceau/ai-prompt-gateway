// Result consumer: reads finished-prompts and writes results to cache/Redis.
package main

import (
	"fmt"
	"log"
	"os"
)

func main() {
	topic := envOrDefault("KAFKA_TOPIC_FINISHED", "finished-prompts")
	log.Printf("result-consumer starting (topic=%s, not yet implemented)", topic)
	fmt.Println("AI Prompt Gateway — result consumer")
	os.Exit(0)
}

func envOrDefault(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
