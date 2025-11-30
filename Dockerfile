FROM python:3.11-slim AS builder

WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt ./

RUN apt-get update \
    && apt-get install -y build-essential --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip \
    && python -m pip install --prefix=/install -r requirements.txt

# Copy source files into the image (builder context)
COPY . /app

FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from the builder stage
COPY --from=builder /install /usr/local
COPY --from=builder /app /app

# Install small runtime deps and cleanup
RUN apt-get update \
    && apt-get install -y curl --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENV DATABASE_URL=sqlite:///./tinyurlr.sqlite3
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
