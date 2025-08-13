#!/bin/bash
set -e

echo "Starting AI Survey Generator app..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
