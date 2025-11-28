#!/usr/bin/env bash
set -euo pipefail

# Start uvicorn in the background with logs
cd "$(dirname "$0")/.."
source .venv/bin/activate || true
nohup .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload > uvicorn.log 2>&1 &
echo "Started uvicorn (background) on http://127.0.0.1:8000, logs in uvicorn.log"
