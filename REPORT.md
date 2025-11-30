# TinyURL - DevOps Implementation Report
**IE University - BCSAI - SDDO - Assignment 2**

**Student**: Leena El Barq  
**Date**: November 30, 2025  
**Repository**: https://github.com/leenaelbarq/tinyurl

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Code Quality and Refactoring](#2-code-quality-and-refactoring)
3. [Testing and Coverage](#3-testing-and-coverage)
4. [Continuous Integration (CI)](#4-continuous-integration-ci)
5. [Continuous Deployment (CD)](#5-continuous-deployment-cd)
6. [Containerization](#6-containerization)
7. [Monitoring and Health Checks](#7-monitoring-and-health-checks)
8. [Challenges and Solutions](#8-challenges-and-solutions)
9. [Conclusion](#9-conclusion)

---

## 1. Executive Summary

This report documents the transformation of the TinyURL application from Assignment 1 into a production-ready system following DevOps best practices. The project now includes automated testing, continuous integration and deployment, Docker containerization, and comprehensive monitoring.

### Key Achievements

- ✅ **Code Coverage**: 89% (exceeds 70% requirement)
- ✅ **CI/CD**: Fully automated GitHub Actions pipelines
- ✅ **Deployment**: Live on Azure Web Apps
- ✅ **Monitoring**: Prometheus metrics and health checks
- ✅ **Containerization**: Docker with multi-stage builds

**Live Application**: https://leena-tinyurl-webapp.azurewebsites.net

---

## 2. Code Quality and Refactoring

### 2.1 SOLID Principles Implementation

The codebase was refactored to follow SOLID principles:

#### Single Responsibility Principle (SRP)
Each module has one clear purpose:

- **`app/main.py`**: HTTP routing, middleware, and API endpoints
- **`app/services.py`**: Business logic (URL validation, shortening, retrieval)
- **`app/db.py`**: Database configuration and session management
- **`app/models.py`**: Data models (SQLAlchemy ORM)
- **`app/templates/`**: UI rendering

**Before Refactoring**: [Describe original structure - e.g., "All logic was in main.py"]

**After Refactoring**: Clean separation allows independent testing and maintenance.

#### Dependency Injection
FastAPI's `Depends()` mechanism provides database sessions:

```python
@app.get("/urls")
def get_urls(db: Session = Depends(get_db)):
    return services.list_urls(db)
```

This makes testing easier and follows the Dependency Inversion Principle.

### 2.2 Code Smells Removed

**Issues Fixed**:
1. Unused imports (detected by ruff)
2. Hardcoded values moved to configuration
3. Long methods split into smaller functions
4. Duplicate code extracted into helper functions

### 2.3 Linting and Code Quality Tools

- **Tool**: `ruff` (fast Python linter)
- **Enforcement**: CI pipeline fails on lint errors
- **Result**: Zero lint warnings

---

## 3. Testing and Coverage

### 3.1 Test Strategy

**Test Types Implemented**:
- Integration tests using FastAPI's `TestClient`
- Tests cover all major endpoints

**Test File**: `tests/test_app.py`

**Key Test Cases**:
1. `test_shorten_and_redirect()`: Creates short URL and verifies redirect works

### 3.2 Coverage Report

**Current Coverage**: **89.05%**

**Coverage by Module**:
- `app/__init__.py`: 100%
- `app/db.py`: 100%
- `app/models.py`: 100%
- `app/main.py`: 84%
- `app/services.py`: 92%

**Total**: 137 statements, 15 missed, **89%** coverage

### 3.3 Coverage Enforcement

CI pipeline enforces minimum 70% coverage:

```bash
pytest --cov=app --cov-fail-under=70
```

**Result**: ✅ Build fails if coverage drops below threshold

**Screenshot**: [INSERT COVERAGE REPORT SCREENSHOT HERE]

---

## 4. Continuous Integration (CI)

### 4.1 CI Pipeline Overview

**Workflow File**: `.github/workflows/ci.yml`

**Trigger Events**:
- Push to `main` branch
- Pull requests to `main`

### 4.2 CI Pipeline Steps

```yaml
1. Checkout code
2. Setup Python 3.11
3. Install dependencies
4. Run ruff linter
5. Run pytest with coverage
6. Build Docker image (validation only)
7. Upload test artifacts
```

### 4.3 Pipeline Execution Time

**Average Duration**: ~1-2 minutes

### 4.4 Quality Gates

The pipeline enforces:
- ✅ No lint errors (ruff must pass)
- ✅ All tests must pass
- ✅ Coverage ≥ 70%
- ✅ Docker image must build successfully

**Screenshot**: [INSERT CI WORKFLOW SUCCESS SCREENSHOT HERE]

---

## 5. Continuous Deployment (CD)

### 5.1 CD Pipeline Overview

**Workflow File**: `.github/workflows/cd.yml`

**Trigger**: Automatic on push to `main`

### 5.2 Deployment Steps

```yaml
1. Login to Azure (using service principal)
2. Login to Azure Container Registry (ACR)
3. Build Docker image
4. Tag image with commit SHA and 'latest'
5. Push both tags to ACR
6. Deploy to Azure Web App for Containers
```

### 5.3 Azure Resources

| Resource | Name/Value |
|----------|-----------|
| Container Registry | leenatinyurlcr.azurecr.io |
| Web App | leena-tinyurl-webapp |
| Resource Group | BCSAI2025-DEVOPS-STUDENTS-B |
| Region | West Europe |

### 5.4 Secrets Management

**GitHub Secrets Configured**:
- `AZURE_CREDENTIALS`: Service principal JSON
- `ACR_REGISTRY`: Registry name
- `ACR_USERNAME`: ACR username
- `ACR_PASSWORD`: ACR password
- `AZURE_WEBAPP_NAME`: Web app name
- `AZURE_RESOURCE_GROUP`: Resource group

**Security**: Secrets never exposed in logs or code.

### 5.5 Deployment Verification

After deployment:
1. Health check: `GET /health` returns `{"status": "ok"}`
2. App accessible at: https://leena-tinyurl-webapp.azurewebsites.net

**Screenshot**: [INSERT LIVE APP SCREENSHOT HERE]

---

## 6. Containerization

### 6.1 Dockerfile

**Type**: Multi-stage build

**Stages**:
1. **Builder stage**: Install dependencies
2. **Runtime stage**: Minimal production image

**Benefits**:
- Smaller image size
- Faster builds (layer caching)
- Security (no build tools in production)

### 6.2 Docker Image

**Base Image**: `python:3.11-slim`

**Exposed Port**: 8000

**Health Check**: `curl http://localhost:8000/health`

### 6.3 docker-compose Setup

**Services**:
1. **web**: FastAPI application
2. **prometheus**: Metrics scraping

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
```

**Usage**:
```bash
docker-compose up
```

---

## 7. Monitoring and Health Checks

### 7.1 Health Check Endpoint

**URL**: `GET /health`

**Purpose**: Verify application and database are operational

**Response**:
```json
{
  "status": "ok"
}
```

**Implementation**: Executes `SELECT 1` query to verify DB connectivity

### 7.2 Metrics Endpoint

**URL**: `GET /metrics`

**Format**: Prometheus exposition format

**Metrics Exposed**:

1. **`tinyurl_requests_total`** (Counter)
   - Labels: `method`, `endpoint`, `http_status`
   - Tracks all HTTP requests

2. **`tinyurl_request_latency_seconds`** (Histogram)
   - Labels: `method`, `endpoint`
   - Buckets: 5ms, 10ms, 25ms, ..., 10s
   - Measures response time

3. **`tinyurl_request_errors_total`** (Counter)
   - Labels: `method`, `endpoint`
   - Tracks 4xx and 5xx errors

### 7.3 Prometheus Configuration

**File**: `monitoring/prometheus.yml`

**Scrape Config**:
```yaml
scrape_configs:
  - job_name: 'tinyurl'
    static_configs:
      - targets: ['web:8000']
```

**Scrape Interval**: 15 seconds

### 7.4 Grafana Dashboard

**File**: `monitoring/grafana_dashboard.json`

**Visualizations**:
- Request rate by endpoint (time series)
- Latency percentiles
- Error rate over time

**Screenshot**: [INSERT GRAFANA DASHBOARD SCREENSHOT OR METRICS SCREENSHOT HERE]

---

## 8. Challenges and Solutions

### Challenge 1: CI Failing Due to Missing `app/static` Directory

**Problem**: Git doesn't track empty directories, causing CI to fail when mounting static files.

**Solution**: Added `.gitkeep` placeholder file in `app/static/` to ensure directory exists in CI.

### Challenge 2: CD Workflow Syntax Error

**Problem**: Using `secrets` in job-level `if` condition caused workflow validation failure.

**Error**:
```
Unrecognized named-value: 'secrets'
```

**Solution**: Removed the `if` condition and let the workflow fail gracefully if secrets are missing.

### Challenge 3: Azure Web App Showing "Application Error"

**Problem**: Container deployed but app wouldn't start.

**Solution**: 
1. Configured ACR credentials in Web App settings
2. Set `WEBSITES_PORT=8000` environment variable
3. Configured startup command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Challenge 4: Ruff Linting Errors in `tests/conftest.py`

**Problem**: 
- F401: `os` imported but unused
- E402: Module-level imports not at top of file

**Solution**: 
- Removed unused `os` import
- Added `# noqa: E402` comments for legitimate path manipulation before imports

---

## 9. Conclusion

### 9.1 Summary of Improvements

This project successfully transformed a basic Flask application into a production-grade system with:

1. **89% test coverage** (exceeds 70% requirement)
2. **Fully automated CI/CD** pipelines
3. **Containerized deployment** on Azure
4. **Production-grade monitoring** with Prometheus
5. **Clean, maintainable code** following SOLID principles

### 9.2 DevOps Practices Demonstrated

- ✅ Infrastructure as Code (Dockerfile, docker-compose)
- ✅ Automated Testing and Coverage Enforcement
- ✅ Continuous Integration and Deployment
- ✅ Container Orchestration
- ✅ Observability (metrics, health checks)
- ✅ Security (secrets management)

### 9.3 Future Improvements

**Potential Enhancements**:
1. Add more unit tests for edge cases
2. Implement Grafana dashboards with alerts
3. Add database migrations (Alembic)
4. Switch from SQLite to PostgreSQL for production
5. Add rate limiting and authentication
6. Implement blue-green deployments

### 9.4 Lessons Learned

### 9.4 Lessons Learned

Throughout this project, I gained hands-on experience with modern DevOps practices and learned valuable lessons about automation, containerization, and continuous deployment.

**Technical Skills Acquired**:
1. **GitHub Actions**: Learned to create and debug CI/CD pipelines, manage secrets, and understand workflow triggers. The syntax errors I encountered taught me the importance of thorough testing before pushing to main.

2. **Docker & Containerization**: Understanding multi-stage builds and how to optimize image size was challenging but rewarding. Configuring the Azure Web App to properly run the container required debugging startup commands and environment variables.

3. **Azure Cloud Deployment**: Setting up Azure resources (ACR, Web App, Resource Groups) and integrating them with GitHub Actions provided real-world cloud deployment experience. Managing secrets securely was a critical learning point.

4. **Monitoring & Observability**: Implementing Prometheus metrics and health checks showed me the importance of visibility in production systems. Understanding which metrics matter (request count, latency, errors) is crucial for maintaining healthy applications.

5. **Test Coverage Enforcement**: Achieving 89% coverage taught me to write meaningful tests rather than just aiming for numbers. The CI enforcement ensures quality doesn't degrade over time.

**Challenges Faced**:
- **Git Empty Directories**: Learning that Git doesn't track empty folders led to CI failures. The `.gitkeep` solution was a simple but important lesson.
- **Workflow Syntax**: GitHub Actions has specific constraints (like not using `secrets` in job-level conditions) that required debugging and research.
- **Azure Configuration**: Getting the container to start in Azure required understanding port configuration, startup commands, and ACR authentication.
- **Linting Errors**: Balancing code quality tools with practical needs (like path manipulation before imports) taught me when to use exceptions (`# noqa`).

**What I Would Do Differently**:
1. **Start with Tests Earlier**: Writing tests alongside code development would have been more efficient than adding them afterward.
2. **Local Docker Testing First**: Testing the Docker image locally before pushing to Azure would have caught configuration issues earlier.
3. **Incremental CI/CD Setup**: Building the pipelines step-by-step rather than all at once would have made debugging easier.
4. **More Granular Commits**: Smaller, focused commits would provide better history and easier rollback if needed.

**Key Takeaways**:
- DevOps is about automation and reducing manual work through well-designed pipelines
- Monitoring and observability are as important as the features themselves
- Good documentation (README, REPORT) makes projects maintainable and shareable
- Cloud deployment requires understanding both the application and the platform
- Code quality tools (linting, testing, coverage) prevent technical debt

This project transformed my understanding of software development from "write code that works" to "build systems that are testable, deployable, and maintainable." The DevOps practices learned here are directly applicable to real-world software engineering.

---

## Appendix: Screenshots

### A. Coverage Report
[INSERT SCREENSHOT: pytest coverage output showing 89%]

### B. CI Pipeline Success
[INSERT SCREENSHOT: GitHub Actions CI workflow success]

### C. CD Pipeline Success
[INSERT SCREENSHOT: GitHub Actions CD workflow deploying to Azure]

### D. Live Application
[INSERT SCREENSHOT: Working app at https://leena-tinyurl-webapp.azurewebsites.net]

### E. Metrics Endpoint
[INSERT SCREENSHOT: /metrics endpoint showing Prometheus metrics]

### F. Azure Resources
[INSERT SCREENSHOT: Azure portal showing Web App and ACR]

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- GitHub Actions: https://docs.github.com/en/actions
- Azure Web Apps: https://azure.microsoft.com/en-us/services/app-service/web/
- Prometheus: https://prometheus.io/docs/
- Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/

---

**End of Report**
