#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate || true
echo "Checking /health"
curl -v http://127.0.0.1:8000/health || true
echo
echo "Checking /metrics"
curl -v http://127.0.0.1:8000/metrics || true
echo
echo "Shorten a url (POST /shorten)"
curl -v -X POST http://127.0.0.1:8000/shorten -H 'Content-Type: application/json' -d '{"url":"https://example.com/abc"}' || true
