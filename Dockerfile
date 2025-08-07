# Multi-stage Dockerfile to slim down image

# ── Stage 1: Build wheels ─────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt ./
RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

# ── Stage 2: Runtime ─────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy only runtime wheels and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl \
    && rm -rf /wheels

# Copy application code
COPY app.py ./
# (optional) Copy any other scripts you need, e.g., test_api.py
# COPY test_api.py ./

# Expose port (match your app)
EXPOSE 8001

# Launch Uvicorn for FastAPI (better than python script directly)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
