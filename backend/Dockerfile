# ============================================
# TruEditor Backend - Production Dockerfile
# ============================================
# Multi-stage build for optimized image size
# Platform-agnostic: AWS ECS, GCP Cloud Run, Azure Container, Render, vb.
#
# Geliştirici: Abdullah Doğan

# ====================
# Stage 1: Builder
# ====================
FROM python:3.11-slim as builder

WORKDIR /app

# System dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements/base.txt requirements/base.txt
COPY requirements/production.txt requirements/production.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/production.txt

# ====================
# Stage 2: Runtime
# ====================
FROM python:3.11-slim as runtime

# Labels
LABEL maintainer="Abdullah Dogan"
LABEL description="TruEditor Backend API"
LABEL version="1.0.0"

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000

WORKDIR /app

# Runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    # WeasyPrint dependencies for PDF generation
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copy application code
COPY --chown=appuser:appgroup . .

# Create necessary directories
RUN mkdir -p staticfiles media && \
    chown -R appuser:appgroup staticfiles media

# Switch to non-root user
USER appuser

# Collect static files (build time)
RUN python manage.py collectstatic --no-input --settings=core.settings.production || true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/api/v1/health/')" || exit 1

# Expose port
EXPOSE ${PORT}

# Default command (gunicorn)
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --worker-class gthread --worker-tmp-dir /dev/shm --access-logfile - --error-logfile -"]
