FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip \
    && python -m pip install --prefix=/install -r requirements.txt

COPY . /app

FROM python:3.11-slim

WORKDIR /app

# copy installed packages from build stage
COPY --from=builder /install /usr/local
COPY --from=builder /app /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV DATABASE_URL=sqlite:///./tinyurlr.sqlite3
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD curl -f http://localhost:8000/health || exit 1
