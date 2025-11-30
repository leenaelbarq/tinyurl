# TinyURL — Assignment 2 Report

This report documents the architecture, design decisions, testing, continuous integration, continuous deployment, containerization, and monitoring additions implemented for the TinyURL project. It explains how the code has been reorganized to improve readability and testability, how CI/CD pipelines were implemented for repeatable automation, and how the project can be run and monitored locally and in Azure.

## Executive summary

- The TinyURL project is a minimal FastAPI application that provides short URL creation, redirection, hit counting and a small UI.
- We applied a set of incremental improvements to support modern DevOps workflows: a clearer separation of concerns and SOLID-inspired refactorings for testability, unit & integration tests with coverage thresholds, CI and CD pipelines using GitHub Actions that build/run tests and deploy to Azure Container Registry (ACR) and Azure Web App, containerization via a multi-stage Dockerfile, and monitoring using Prometheus and Grafana.
- The local development experience supports a `venv` and a docker-compose stack for running the app together with Prometheus for metrics scraping and Grafana dashboarding.
- CI ensures code quality gates (lint and test coverage) and a CD pipeline pushes images to a private registry (ACR) and deploys the latest image to an Azure Web App only when required secrets are configured.

---

## 1) Code quality & refactoring (SOLID / SRP)

### 1.1 Layered code organization

The codebase is organized in the `app/` package into distinct files, each serving a single area of responsibility:

- `app/models.py` — declares SQLAlchemy models. The `Url` model contains the schema for the short URL entry (id, original_url, code, created_at, hits).
- `app/db.py` — database setup and session management. The engine creation, session factory and `get_db` dependency are centralized here, allowing swapping database configuration as needed.
- `app/services.py` — contains business logic and helper methods: code generation, unique code generation strategy, create/list/delete helper functions. The `code_generator` injection pattern provides separation between code generation and persistence logic and enables stable testing.
- `app/main.py` — FastAPI routes, middleware for metrics, and minimal view layer for the UI and Jinja templates. Routes use `services` functions, and the `get_db` dependency provides DB access.

This structure follows SRP (single responsibility principle): each module focuses only on one part of the application (data model, data access, business rules, or HTTP layer), which keeps the code clearer and easier to test and maintain.

### 1.2 Notable refactorings

- Moved all business logic into `app/services.py`, keeping `main.py` focused on HTTP routes, responses, and instrumentation.
- Kept DB engine and session management in `app/db.py` so that tests can create in-memory database sessions and the app uses the configured `DATABASE_URL`.
- Introduced dependency injection for `code_generator` in `services` functions to allow deterministic behavior in tests — this reduces flakiness in tests and makes collision testing predictable.
- Added docstrings and enhanced type hints (when applicable) to improve maintainability.

These refactorings improved unit testability and reduced coupling between modules.

---

## 2) Testing & coverage

### 2.1 Test suite

Unit tests and a small set of integration tests are included to give confidence in both business logic and end-to-end behavior.

- `tests/test_services.py` (unit tests for the `services` layer):
  - `test_validate_url` — validates HTTP scheme checking logic.
  - `test_create_short_url_with_custom_generator` — tests deterministic generation of short codes and idempotency: creating a short URL twice returns the same DB record.
  - `test_generate_unique_code_avoids_collision` — simulates code collisions by providing a code generator that produces duplicates and validates the collision handling loop.
  - `test_delete_by_code` — verifies deletion logic removes a record and returns `False` when not present.

- `tests/test_app.py` (integration tests using `TestClient`):
  - `test_shorten_and_redirect` — posts to `/shorten`, lists via `/urls`, and checks redirect behavior (the `/{code}` endpoint returns a redirect to the original URL).
  - `test_health_and_metrics_endpoints` — validates `/health` returns `ok` and `/metrics` expose a Prometheus-format output with `tinyurl_requests_total`.
  - `test_metrics_count_errors` — invokes a non-existing code to trigger a 404 and checks that error metrics are incremented in `/metrics` output (metric `tinyurl_request_errors_total`).

### 2.2 Test tooling and enforcement

- Tests use `pytest` together with `pytest-cov`. The repository includes helper scripts (`./scripts/run_tests.sh`, `./scripts/pretest.sh`) to install dependencies and run tests with coverage and a junit report.
- The CI workflow uses `--cov-fail-under=70` to enforce a minimum coverage threshold of 70%. Tests are also uploaded as artifacts in the CI for later review.
- Locally, running tests with coverage can be executed with:
```
./scripts/run_tests.sh
```
or
```
python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=70
```

The local coverage has exceeded 70% consistently (the repository reports ~88% in local runs).

---

## 3) Continuous Integration (CI)

### 3.1 Workflow: `ci.yml`

- Name: `CI`
- Location: `.github/workflows/ci.yml`
- Triggers: push & pull_request on `main` branch.
- High-level steps executed in CI:
  1. Checkout the repository
  2. Set up Python (3.11)
  3. Debug environment (basic information printed for diagnostics)
  4. Install dependencies (`pip install -r requirements.txt`)
  5. Lint code with `ruff` to enforce basic code style and quality
  6. Run tests with `pytest` and `pytest-cov` and enforce `--cov-fail-under=70`
  7. Build the Docker image (validate build using `docker/build-push-action`, but do not push in CI)
  8. Upload coverage and junit XML artifacts for CI reporting

This CI pipeline ensures that code commits and PRs are validated: lint, tests, and minimum coverage. It prevents merging bad or untested code into `main`.

---

## 4) Continuous Deployment (CD)

### 4.1 Workflow: `cd.yml`

- Name: `CD`
- Location: `.github/workflows/cd.yml`
- Triggers: `push` to `main` and `workflow_dispatch` (manual trigger)

This workflow will only proceed when all required GitHub Secrets are present and non-empty: `AZURE_CREDENTIALS`, `ACR_NAME`, `AZURE_WEBAPP_NAME`, and `AZURE_RESOURCE_GROUP`. This reduces noise from the CI/CD pipeline if secrets aren’t configured.

### 4.2 High-level job flow

1. Checkout the repository.
2. Login to Azure using `azure/login@v2` with `AZURE_CREDENTIALS` secret.
3. Obtain ACR credentials (or use CLI-based auth) and use `docker/login-action@v3` to authenticate to Azure Container Registry (`<ACR_NAME>.azurecr.io`).
4. Build the multi-stage Docker image using `docker/build-push-action` and tag images as:
   - `<ACR_NAME>.azurecr.io/tinyurl:${{ github.sha }}` — image for traceability
   - `<ACR_NAME>.azurecr.io/tinyurl:latest` — stable tag used for deployment
5. Push both tags to ACR.
6. Deploy the `latest` image to the target Azure Web App using `azure/webapps-deploy@v2`.

This setup allows automatically building and pushing images as part of a `main` push and ensures consistent image tags and traceability for rollbacks.

### 4.3 Secrets and safe deployment

- All cloud and registry credentials are provided via GitHub Secrets. The `cd.yml` workflow checks these secrets are present before running the deploy job. Credential values are never committed to the repository.
- The `azure_setup.sh` helper can be used to create the necessary resources in Azure and to produce `AZURE_CREDENTIALS` for the workflow.

---

## 5) Docker & deployment

### 5.1 Dockerfile

- A multi-stage Dockerfile is included to produce lean runtime images. The builder stage installs dependencies and compiles any build-time assets; the final stage copies only needed packages and application code.
- The final image runs `uvicorn app.main:app` and exposes port `8000`. The image also installs `curl` for the healthcheck.
- A `HEALTHCHECK` is included to probe `http://localhost:8000/health` at runtime.

### 5.2 Local & Azure parity

- The Docker image used locally in `docker run` and in `docker-compose` is the same that is built and pushed to ACR for Azure deployments. This reduces drift between environment behaviors.

### 5.3 Example docker commands

```
docker build -t tinyurl:latest .
docker run --rm -p 8000:8000 tinyurl:latest
```

Using docker-compose also provides a quick way to start the app and Prometheus for local testing:
```
docker-compose up --build
```

---

## 6) Monitoring & observability

### 6.1 Endpoints

- `/health` — Basic health endpoint that checks DB connectivity and returns `{"status": "ok"}` when healthy.
- `/metrics` — Exposes Prometheus metrics. The application uses `prometheus_client` to expose:
  - `tinyurl_requests_total` — request counter with labels: method, endpoint, http_status
  - `tinyurl_request_latency_seconds` — latency histograms with labels: method, endpoint
  - `tinyurl_request_errors_total` — errors counter with labels: method, endpoint

These metrics are exposed by the `/metrics` route and collected by a Prometheus server configured in `monitoring/prometheus.yml`.

### 6.2 Local dashboards and scraping

- `monitoring/prometheus.yml` provides scrape configs for the `web:8000` service (matching the docker-compose `web` service name).
- `monitoring/grafana_dashboard.json` is an example Grafana dashboard that can be imported to visualize metrics.
- With `docker-compose`, you can run `web` and `prometheus` together and import the Grafana dashboard to inspect request latency, counts, and errors.

---

## 7) Security & operational considerations

- Keep secrets out of the repository; only store them in GitHub Secrets.
- Prefer ACR access via managed identity (Web App system-assigned identity using `AcrPull`) rather than ACR admin credentials for least privilege in production. The `cd.yml` includes a path for pushing images with appropriate credentials and the `azure_setup.sh` includes setup helpers for the resource group and SP.
- The default database is SQLite for simplicity in this assignment. For production, move to a managed database and add schema migrations (Alembic).

---

## 8) Future work and improvements

- Add a dedicated `lint` job in CI and a `pre-commit` configuration to catch formatting and lint errors earlier.
- Add E2E tests that run in a Docker-based environment to validate full system behavior on each push.
- Consider moving from SQLite to PostgreSQL (or a managed DB) in production. Add migration tooling (Alembic) and test fixtures that use a real DB instance in CI.
- Implement feature flags or a canary/deployment strategy for safer production rollouts.

---

## Conclusion

This assignment updated the TinyURL project to follow clearer architecture patterns, improve test coverage and automation, and enable a robust CI/CD pipeline with monitoring and sensible runtime management. With the new workflows and Docker-based deployment, the project is now better prepared for iterative development and safe automated deployments.

If you want, I can extend this report by including basic diagrams (e.g., pipeline flow, architecture boxes) and add a short appendix listing GitHub Action run examples.
# TinyURL — Assignment 2 Report

Summary of improvements and automation added to the TinyURL project.

1) Code quality and refactoring
- Extracted and typed functions in `app/services.py`, added docstrings and dependency injection for the random code generator to improve testability and separation of concerns.
- Added `app/main.py` improvements: health endpoint, Prometheus metrics, and middleware for request instrumentation.

2) Testing and coverage
- Added unit tests for services in `tests/test_services.py` and expanded integration tests in `tests/test_app.py` to include health and metrics endpoints.
- Achieved >70% coverage (88% locally) using pytest-cov.
- Added `scripts/run_tests.sh` to generate coverage and junit reports.

3) Continuous Integration (CI)
- Added GitHub Actions workflow `ci.yml` to run tests and enforce coverage threshold of 70%.

4) Containerization and Deployment (CD)
- Added `Dockerfile` and `docker-compose.yml` for local runnable environment and Prometheus scraping configuration.
- Included a `deploy.yml` GitHub Actions workflow to build and push images to GitHub Container Registry on pushes to `main`.

5) Monitoring and Health Checks
- Added `/health` endpoint for simple application status checks.
- Added `/metrics` endpoint and Prometheus middleware instrumentation for request count, latency, and errors. Included `monitoring/prometheus.yml` for local Prometheus setup.

6) Documentation
- Extended `README.md` to include run/test/deploy instructions and note monitoring endpoints.
- This report provides a summary of implementation decisions and automation steps performed.

This assignment followed an incremental approach: refactor and test, then add automation, and finally add CI/CD and monitoring.
