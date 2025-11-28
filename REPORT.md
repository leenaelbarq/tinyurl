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
