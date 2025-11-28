#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-8000}
echo "Checking listeners on port $PORT..."
lsof -iTCP:${PORT} -sTCP:LISTEN || echo "No listener found on port $PORT"
