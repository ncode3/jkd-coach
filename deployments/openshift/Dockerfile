# SAMMO Fight IQ - OpenShift Deployment Dockerfile
# Multi-stage build for optimized container size

# Build stage
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-openshift.txt .
RUN pip install --no-cache-dir --user -r requirements-openshift.txt

# Final stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app.py .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# OpenShift runs containers using an arbitrarily assigned user ID
# Set permissions to allow any user to run the app
RUN chmod -R g+rwX /app && \
    chmod -R o+rX /app

# Expose port 8080 (standard for OpenShift)
EXPOSE 8080

# Set environment variables
ENV PORT=8080 \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
