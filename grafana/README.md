# Grafana Setup

1. Run `docker-compose up`.
2. Access Grafana at `http://localhost:3000` (admin/admin).
3. Add Prometheus data source: `http://prometheus:9090`.
4. Import dashboard (create one using the metrics exposed by the API).
