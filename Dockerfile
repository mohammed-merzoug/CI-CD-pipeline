# ============================================================
# Dockerfile – Django E-commerce Application
# Base image: python:3.11-slim
# ============================================================

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn==21.2.0

# Copy application files
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Create directories and preserve media files for seeding
RUN mkdir -p /app/media /app/staticfiles /app/media-seed \
    && if [ -d /app/media/products ]; then cp -r /app/media/products /app/media-seed/; fi \
    && chmod +x /app/entrypoint.sh

# Collect static files
RUN python manage.py collectstatic --noinput --settings=ecommerce_project.settings || true

# Apply migrations (database will be initialized)
RUN python manage.py migrate --noinput

# Create a non-root user for security
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose the application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000')" || exit 1

# Use entrypoint script for initialization
ENTRYPOINT ["/app/entrypoint.sh"]

# Start Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "ecommerce_project.wsgi:application"]
