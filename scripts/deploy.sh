#!/bin/bash
set -e

ENV=$1

if [ -z "$ENV" ]; then
    echo "Usage: ./deploy.sh <environment>"
    exit 1
fi

echo "Deploying to $ENV..."

# Placeholder for actual deployment logic (e.g., kubectl apply, terraform apply)
if [ "$ENV" == "staging" ]; then
    echo "Applying staging configuration..."
    # kubectl apply -f infra/k8s/deployment.yaml
elif [ "$ENV" == "prod" ]; then
    echo "Applying production configuration..."
    # kubectl apply -f infra/k8s/deployment.yaml
else
    echo "Unknown environment: $ENV"
    exit 1
fi

echo "Deployment to $ENV successful (mock)."
