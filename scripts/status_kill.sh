#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-8000}
echo "Listing processes on TCP port $PORT..."
PIDS=$(lsof -tiTCP:${PORT} -sTCP:LISTEN || true)
if [ -z "$PIDS" ]; then
  echo "No processes found listening on port $PORT"
  exit 0
fi

for PID in $PIDS; do
  OWNER=$(ps -o user= -p $PID | awk '{print $1}')
  echo "PID: $PID owner: $OWNER"
  if [ "$OWNER" = "$(whoami)" ]; then
    echo "Killing $PID (owned by $(whoami))"
    kill $PID || echo "Failed to kill $PID"
  else
    echo "Skipping $PID: owned by $OWNER (requires sudo to kill)"
  fi
done
