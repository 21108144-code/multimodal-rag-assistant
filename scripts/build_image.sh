#!/bin/bash
set -e

TAG=$(date +%s)
IMAGE_NAME="multimodal-rag"

echo "Building Docker image ${IMAGE_NAME}:${TAG}..."
docker build -t ${IMAGE_NAME}:${TAG} -t ${IMAGE_NAME}:latest .

echo "Build complete."
