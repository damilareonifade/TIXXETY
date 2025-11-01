# Use a newer, smaller, and more secure base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Install system dependencies (only what’s needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first for better caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# # Expose the FastAPI port
# EXPOSE 8000

# # Default command (can be overridden in docker-compose)
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
