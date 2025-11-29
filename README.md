# tinyurl

Minimal URL shortener for quick links. Built with **FastAPI** and **SQLite**. Simple UI for creating links plus REST endpoints.

## Features
- Create short URLs  
- Redirect using `/{code}`  
- List all URLs with hit counter  
- Delete a short URL  
- Persistent storage (SQLite)  
- Minimal HTML UI (no frameworks)

## Prerequisites
- Python 3.10+  
- pip  
- Virtual environment (recommended)

## Setup

# clone
git clone https://github.com/leenaelbarq/tinyurl.git
cd tinyurl

# venv
Clone the repository and create a Python virtual environment (venv):
```
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# install
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
uvicorn app.main:app --reload
Install the Python dependencies:
```
pip install -r requirements.txt
```
- UI → http://127.0.0.1:8000
Start the FastAPI app using Uvicorn (development server):
```
uvicorn app.main:app --reload
```
## Endpoints
Open in your browser:
- UI: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
| GET | /{code} | Redirects to the original URL |
| GET | /urls | List all shortened URLs and hit counts |
| DELETE | /urls/{code} | Delete a shortened URL |

## Run Tests
Run tests and view coverage (locally):
```
./scripts/run_tests.sh
```
or
## Tests & coverage

This project uses `pytest` for testing and `pytest-cov` for measuring coverage. The CI enforces a minimum coverage threshold of 70% using `--cov-fail-under=70`.

Run tests locally with coverage:
```
./scripts/run_tests.sh
```
Or run pytest directly with coverage hints:
```
python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=70
```
│   ├── main.py          # FastAPI app + routes
│   ├── db.py            # SQLite engine/session
│   ├── models.py        # SQLAlchemy models
│   ├── services.py      # business logic (create/list/get/delete)
│   ├── templates/
│   │   └── index.html   # minimal UI
│   └── static/          # static assets
├── tests/
│   └── test_app.py      # test for shorten and redirect
├── requirements.txt
├── tinyurl.sqlite3      # local DB (auto-created)
├── .gitignore
└── README.md

## Quick Usage
1. Run the app.  
2. Paste any long URL in the field and click Shorten.  
3. Use the generated short URL to redirect.  
4. View all links and delete unwanted ones.  
5. Optionally, open /docs for the interactive API page.
6. Health endpoint → GET /health
7. Metrics endpoint → GET /metrics (Prometheus format)

## Useful local scripts

All scripts are under the `scripts/` folder. Use these to run, test, and manage the local server safely:

- `./scripts/pretest.sh` — Ensure venv exists, activate it, set `PYTHONPATH`, install requirements, and run tests with coverage. Use this to reproduce the CI tests locally.
- `./scripts/start_server.sh` — Start the app using uvicorn in the background. It will try to stop any process on port 8000 first.
- `./scripts/stop_server.sh 8000` — Stop processes listening on the given port (default 8000).
## Docker / Container

The repository contains a `Dockerfile` that produces a container image for this FastAPI app and runs the Uvicorn server on port 8000.

Build and run the image with Docker:
```
docker build -t tinyurl:latest .
docker run --rm -p 8000:8000 tinyurl:latest
```

Alternatively, use `docker-compose` to run the app together with Prometheus (for metrics scraping):
```


## Docker / Container
Prometheus UI will be available at http://localhost:9090 and the app at http://localhost:8000

Grafana: create a dashboard using `monitoring/grafana_dashboard.json` to visualize metrics and request latency/errors.
Build Docker image:
```
docker build -t tinyurl:latest .
The project uses two GitHub Actions workflows stored under `.github/workflows`:

- `ci.yml` — Continuous Integration (CI)
	- Trigger: `push` and `pull_request` to `main`.
	- What it does: Checks out code, sets up Python (3.11), installs deps, runs linting with `ruff`, runs unit tests using `pytest` with coverage (enforced `--cov-fail-under=70`), validates Docker build (no push), and uploads test/coverage reports as artifacts.

- `cd.yml` — Continuous Deployment (CD) to Azure
	- Trigger: `push` to `main` and `workflow_dispatch`.
	- What it does: Logs in to Azure (using `AZURE_CREDENTIALS`), logs in to ACR, builds a multi-stage Docker image, tags it with the commit SHA and `latest`, pushes both tags to ACR, and deploys the `latest` image to an Azure Web App.
	- Guard clause: `cd.yml` only runs the `deploy` job when the following GitHub Secrets are set (non-empty): `AZURE_CREDENTIALS`, `ACR_NAME`, `AZURE_WEBAPP_NAME`, `AZURE_RESOURCE_GROUP`.

Prometheus UI will be available at http://localhost:9090 and the app at http://localhost:8000

Grafana: create a dashboard using `monitoring/grafana_dashboard.json` to visualize metrics and request latency/errors.

- `GET /health` — Basic health endpoint that verifies the app can access the database and returns `{"status": "ok"}` on success. This is used in the Dockerfile's `HEALTHCHECK`.
- `GET /metrics` — Prometheus metrics endpoint; instrumentation includes request count (`tinyurl_requests_total`), latency histogram (`tinyurl_request_latency_seconds`), and error counter (`tinyurl_request_errors_total`).

Prometheus & Grafana support:
- `monitoring/prometheus.yml` — A basic scrape config for Prometheus that targets the `web` service on port 8000 (works with `docker-compose`).
- `monitoring/grafana_dashboard.json` — An example Grafana dashboard JSON file for visualizing latency and error metrics.

The project uses two GitHub Actions workflows stored under `.github/workflows`:

- `ci.yml` — Continuous Integration (CI)
	- Trigger: `push` and `pull_request` to `main`.
	- What it does: Checks out code, sets up Python (3.11), installs deps, runs linting with `ruff`, runs unit tests using `pytest` with coverage (enforced `--cov-fail-under=70`), validates Docker build (no push), and uploads test/coverage reports as artifacts.

- `cd.yml` — Continuous Deployment (CD) to Azure
	- Trigger: `push` to `main` and `workflow_dispatch`.
	- What it does: Logs in to Azure (using `AZURE_CREDENTIALS`), logs in to ACR, builds a multi-stage Docker image, tags it with the commit SHA and `latest`, pushes both tags to ACR, and deploys the `latest` image to an Azure Web App.
	- Guard clause: `cd.yml` only runs the `deploy` job when the following GitHub Secrets are set (non-empty): `AZURE_CREDENTIALS`, `ACR_NAME`, `AZURE_WEBAPP_NAME`, `AZURE_RESOURCE_GROUP`.

To enable the CD workflow, configure these repo GitHub Secrets (do not store secrets in code):
	- `AZURE_CREDENTIALS` — Service principal JSON (Azure CLI `--sdk-auth` output), required by `azure/login`
	- `ACR_NAME` — Azure Container Registry short name (the full FQDN is `<ACR_NAME>.azurecr.io`)
	- `AZURE_WEBAPP_NAME` — The Azure Web App name to deploy to
	- `AZURE_RESOURCE_GROUP` — Resource group that contains the ACR and the Azure Web App


## SDLC Model
This project followed a Lean / Iterative model.  
It started with the core shorten and redirect functions, then expanded step-by-step with testing, a minimal UI, and cleanup. Each phase allowed fast feedback and improvement without overcomplication.

## DevOps Reflection
To adapt this app for DevOps practices:
- Add a Dockerfile for containerization.  
- Configure GitHub Actions for CI (automatic testing on push).  
- Deploy to a platform like Render or Railway.  
- Later migrate from SQLite to a production database like PostgreSQL.  
- Add monitoring endpoints and automated formatting/linting checks.
Additional notes:
- CI: GitHub Actions workflows provided in `.github/workflows/` for test and container image build (push-only on `main`).
- Docker: `Dockerfile` and `docker-compose.yml` included for local development and monitoring with Prometheus.

## Academic Honesty
I used GitHub Copilot and AI tools occasionally for syntax help, debugging, and structuring repetitive sections (like test setup and function templates).  
All code, logic, and design decisions were fully implemented and verified by me to ensure I understood how every part works.
