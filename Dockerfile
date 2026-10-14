# Dockerfile for Moly-Viet Production Deployment on Render / Cloud
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-cloud.txt /app/
RUN pip install --no-cache-dir -r requirements-cloud.txt

# Copy application code and assets
COPY tools/ /app/tools/
COPY web/ /app/web/
COPY archive/clients/local-overrides/ /app/archive/clients/local-overrides/
COPY archive/clients/offline-mirror/ /app/archive/clients/offline-mirror/
COPY data/server/ /app/data/server/

# Create runtime directories
RUN mkdir -p /app/archive/clients/captured-live /app/web/download

ENV PYTHONUNBUFFERED=1
ENV PORT=18080

# Start game servers: moly_probe_server in background, capture_proxy as foreground web server
CMD ["sh", "-c", "python tools/moly_probe_server.py --log /app/data/server/probe-events.jsonl & python tools/capture_proxy.py --archive /app/archive/clients/captured-live --host 0.0.0.0 --port ${PORT} --local-server 127.0.0.1 --overrides /app/archive/clients/local-overrides --mirror /app/archive/clients/offline-mirror"]
