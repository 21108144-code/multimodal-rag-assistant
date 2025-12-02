# Operations Guide

## Deployment

### Staging
1. Push changes to `main`.
2. GitHub Actions CI builds the image.
3. CD pipeline deploys to Staging automatically.

### Production
1. Go to GitHub Actions.
2. Approve the "Deploy to Production" job in the CD pipeline.

## Monitoring

- **Metrics**: Available at `/metrics`.
- **Dashboards**: Grafana (port 3000).
- **Logs**: Structured logs to stdout (captured by Fluentd/Cloud Logging).

## Troubleshooting

- **High Latency**: Check GPU utilization or scale up replicas in `infra/k8s/hpa.yaml`.
- **OOM Errors**: Increase memory limits in `infra/k8s/deployment.yaml`.
