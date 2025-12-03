# Use a lightweight Python base image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies (if needed for building wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
# If requirements.txt exists, install from it; otherwise fall back to common packages
RUN if [ -f requirements.txt ]; then \
      pip install --upgrade pip && pip install -r requirements.txt; \
    else \
      pip install --upgrade pip && pip install Django djangorestframework drf-spectacular; \
    fi

# Expose development port
EXPOSE 8000

# Default command: run migrations and start server
CMD ["bash", "-lc", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
