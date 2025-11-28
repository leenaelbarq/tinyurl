#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-8000}
echo "Restarting server on port $PORT..."
./scripts/stop_server.sh "$PORT" || true
sleep 1
./scripts/start_server.sh
echo "Restart finished. Check status with ./scripts/status_server.sh $PORT"
