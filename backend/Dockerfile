# Use official Python 3.12 slim image for minimal footprint
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy application code to container
COPY . /app

# Copy project dependencies file for pip install
COPY pyproject.toml /code/pyproject.toml

# Install dependencies from pyproject.toml
RUN pip install /code/.

# Expose backend API port
EXPOSE 8000

# Start the application using entrypoint script
CMD ["sh", "entrypoint.sh"]
