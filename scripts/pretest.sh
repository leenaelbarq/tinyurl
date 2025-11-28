#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
  echo ".venv not found; creating..."
  python3 -m venv .venv
fi
source .venv/bin/activate

export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"
mkdir -p reports
echo "Running tests with pytest using: $(which python)" 
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=70 --junitxml=reports/junit.xml
