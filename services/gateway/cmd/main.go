// Gateway: HTTP API + Kafka producer + result polling.
//
// Endpoints (planned):
//   POST /submit  -> produce to raw-prompts, return 202 + job_id
//   GET  /result/{job_id} -> read from cache, return 200 or 404 Pending
//   GET  /health  -> liveness
package main

import (
	"fmt"
	"log"
	"os"
)

func main() {
	port := envOrDefault("GATEWAY_PORT", "8080")
	log.Printf("gateway starting on :%s (not yet implemented)", port)
	fmt.Println("AI Prompt Gateway — submit API + result polling")
	os.Exit(0)
}

func envOrDefault(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
