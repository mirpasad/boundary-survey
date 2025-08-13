# Use official Python 3.12 slim image for minimal footprint
FROM python:3.12-slim

# Prevent .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application code
COPY . /app

RUN chmod +x /app/entrypoint.sh

# Expose backend API port
EXPOSE 8000

# Start the application using entrypoint script
CMD ["sh", "entrypoint.sh"]
