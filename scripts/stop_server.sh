#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-8000}
echo "Looking for processes listening on port $PORT..."
PIDS=$(lsof -tiTCP:${PORT} -sTCP:LISTEN || true)
if [ -z "$PIDS" ]; then
  echo "No processes found listening on port $PORT"
  exit 0
fi
echo "Found process(es): $PIDS"
echo "Killing..."
kill $PIDS
echo "Killed: $PIDS"
