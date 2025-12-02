#!/bin/bash
set -e

echo "Starting API locally..."
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
