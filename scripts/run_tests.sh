#!/usr/bin/env bash
set -euxo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
mkdir -p reports
pytest -q --maxfail=1 --disable-warnings --cov=app --cov-report=xml --cov-report=html --junitxml=reports/junit.xml
echo "Generated reports in ./reports"
