# TinyURL - URL Shortener

Minimal URL shortener for quick links. Built with **FastAPI** and **SQLite**. Includes UI, REST API, Docker containerization, CI/CD pipelines, and Prometheus monitoring.

## Features

- ✅ Create short URLs
- ✅ Redirect using `/{code}`
- ✅ List all URLs with hit counter
- ✅ Delete short URLs
- ✅ Persistent storage (SQLite)
- ✅ Minimal HTML UI
- ✅ Health checks (`/health`)
- ✅ Prometheus metrics (`/metrics`)
- ✅ Docker & docker-compose support
- ✅ CI/CD with GitHub Actions
- ✅ Azure deployment

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Running Tests](#running-tests)
- [Docker](#docker)
- [CI/CD](#cicd)
- [Monitoring](#monitoring)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Deployment](#deployment)

---

## Prerequisites

- Python 3.10+
- pip
- Virtual environment (recommended)
- Docker (optional, for containerization)
- Azure CLI (optional, for deployment)

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/leenaelbarq/tinyurl.git
cd tinyurl
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

### 5. Access the application

- **UI**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health
- **Metrics**: http://127.0.0.1:8000/metrics

---

## Running Tests

### Run tests with coverage

```bash
python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=70
```

### Using helper scripts

```bash
./scripts/run_tests.sh
```

### Current Coverage

✅ **89%** (exceeds 70% requirement)

---

## Docker

### Build Docker image

```bash
docker build -t tinyurl:latest .
```

### Run with Docker

```bash
docker run --rm -p 8000:8000 tinyurl:latest
```

### Run with docker-compose (includes Prometheus)

```bash
docker-compose up
```

This starts:
- **App**: http://localhost:8000
- **Prometheus**: http://localhost:9090

---

## CI/CD

### GitHub Actions Workflows

This project uses two workflows:

#### 1. **CI Pipeline** (`.github/workflows/ci.yml`)

**Triggers**: Push and Pull Requests to `main`

**Steps**:
- ✅ Checkout code
- ✅ Setup Python 3.11
- ✅ Install dependencies
- ✅ Run linting (ruff)
- ✅ Run tests with pytest
- ✅ Enforce 70% code coverage
- ✅ Build Docker image
- ✅ Upload test reports

#### 2. **CD Pipeline** (`.github/workflows/cd.yml`)

**Triggers**: Push to `main` (automatic deployment)

**Steps**:
- ✅ Login to Azure
- ✅ Login to Azure Container Registry (ACR)
- ✅ Build Docker image
- ✅ Tag with commit SHA and `latest`
- ✅ Push to ACR
- ✅ Deploy to Azure Web App

### Required GitHub Secrets

For CD to work, configure these secrets in GitHub:

- `AZURE_CREDENTIALS` - Service principal JSON
- `ACR_REGISTRY` - Azure Container Registry name
- `ACR_USERNAME` - ACR username
- `ACR_PASSWORD` - ACR password
- `AZURE_WEBAPP_NAME` - Azure Web App name
- `AZURE_RESOURCE_GROUP` - Resource group name

---

## Monitoring

### Health Check Endpoint

**URL**: `GET /health`

**Response**:
```json
{
  "status": "ok"
}
```

Verifies database connectivity.

### Metrics Endpoint

**URL**: `GET /metrics`

**Exposed Metrics**:

1. **`tinyurl_requests_total`** - Total requests by endpoint, method, status
2. **`tinyurl_request_latency_seconds`** - Request latency histogram
3. **`tinyurl_request_errors_total`** - Total failed requests

### Prometheus Setup

Prometheus configuration is in `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'tinyurl'
    static_configs:
      - targets: ['web:8000']
```

### Grafana Dashboard

Import `monitoring/grafana_dashboard.json` to visualize:
- Request rate by endpoint
- Latency histograms
- Error rates

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page UI |
| POST | `/shorten` | Create short URL `{"url": "https://example.com"}` |
| GET | `/{code}` | Redirect to original URL |
| GET | `/urls` | List all shortened URLs with hit counts |
| DELETE | `/urls/{code}` | Delete a shortened URL |
| GET | `/health` | Health check endpoint |
| GET | `/metrics` | Prometheus metrics |
| GET | `/docs` | Interactive API documentation |

---

## Project Structure

```
tinyurl/
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI pipeline
│       └── cd.yml          # CD pipeline
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app + routes + monitoring
│   ├── db.py              # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── services.py        # Business logic
│   ├── static/            # Static files
│   │   └── .gitkeep
│   └── templates/
│       └── index.html     # UI template
├── monitoring/
│   ├── prometheus.yml     # Prometheus config
│   └── grafana_dashboard.json  # Grafana dashboard
├── scripts/
│   ├── run_tests.sh       # Test runner script
│   ├── start_server.sh    # Start server script
│   └── stop_server.sh     # Stop server script
├── tests/
│   ├── conftest.py        # Test configuration
│   └── test_app.py        # Integration tests
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Local dev environment
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── REPORT.md             # Assignment report
```

---

## Deployment

### Live Application

**URL**: https://leena-tinyurl-webapp.azurewebsites.net

### Azure Resources

- **Container Registry**: leenatinyurlcr.azurecr.io
- **Web App**: leena-tinyurl-webapp
- **Resource Group**: BCSAI2025-DEVOPS-STUDENTS-B

### Manual Deployment

If you need to deploy manually:

```bash
# Login to Azure
az login

# Build and push to ACR
az acr login --name leenatinyurlcr
docker build -t leenatinyurlcr.azurecr.io/tinyurl:latest .
docker push leenatinyurlcr.azurecr.io/tinyurl:latest

# Restart Web App
az webapp restart --resource-group BCSAI2025-DEVOPS-STUDENTS-B --name leena-tinyurl-webapp
```

---

## Code Quality

### SOLID Principles

This project follows SOLID principles:

- **Single Responsibility**: Each module has a clear purpose
  - `main.py` - HTTP routing and middleware
  - `services.py` - Business logic
  - `db.py` - Database configuration
  - `models.py` - Data models

- **Dependency Injection**: Database session injected via FastAPI's `Depends()`

### Linting

Code quality enforced with `ruff`:

```bash
ruff check .
```

---

## Academic Honesty

This project was developed with assistance from GitHub Copilot and AI tools for:
- Syntax suggestions
- Debugging assistance
- Code structure templates
- Documentation formatting

All logic, design decisions, and implementations were understood and verified to ensure learning objectives were met.

---

## License

This is an academic project for IE University BCSAI SDDO course.
