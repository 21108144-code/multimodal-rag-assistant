# Project Manifest

## Root
- `README.md`: Main documentation.
- `LICENSE`: MIT License.
- `CHANGELOG.md`: Version history.
- `CONTRIBUTING.md`: Contribution guidelines.
- `Makefile`: Developer commands.
- `requirements.txt`: Python dependencies.
- `environment.yml`: Conda environment.
- `Dockerfile`: Service container definition.
- `docker-compose.yml`: Local dev stack.
- `INTERVIEW.md`: Interview talking points.
- `READY_FOR_GITHUB.md`: Verification checklist.

## GitHub
- `.github/workflows/ci.yml`: CI pipeline.
- `.github/workflows/cd.yml`: CD pipeline.
- `.github/PULL_REQUEST_TEMPLATE.md`: PR template.

## Infrastructure
- `infra/terraform/main.tf`: Terraform main config.
- `infra/terraform/variables.tf`: Terraform variables.
- `infra/terraform/outputs.tf`: Terraform outputs.
- `infra/k8s/deployment.yaml`: K8s Deployment.
- `infra/k8s/service.yaml`: K8s Service.
- `infra/k8s/hpa.yaml`: K8s HPA.
- `infra/k8s/ingress.yaml`: K8s Ingress.

## Source Code
- `src/__init__.py`: Package init.
- `src/config.py`: Configuration.
- `src/main.py`: CLI entrypoint.
- `src/utils/logging.py`: Logging setup.
- `src/utils/metrics.py`: Prometheus metrics.
- `src/utils/io.py`: I/O helpers.
- `src/data/ingest.py`: Data ingestion.
- `src/data/preprocess.py`: Data preprocessing.
- `src/data/dataset.py`: PyTorch dataset.
- `src/models/encoder.py`: CLIP encoder.
- `src/models/retriever.py`: FAISS retriever.
- `src/models/generator.py`: LLM generator.
- `src/models/registry.py`: Model registry.
- `src/train.py`: Training script.
- `src/inference/pipeline.py`: RAG pipeline.
- `src/inference/server.py`: Inference singleton.
- `src/api/app.py`: FastAPI app.

## Tests
- `tests/test_preprocess.py`: Preprocessing tests.
- `tests/test_embeddings.py`: Embedding tests.
- `tests/test_retriever.py`: Retriever tests.
- `tests/test_api.py`: API tests.

## Notebooks
- `notebooks/quickstart.py`: Demo script.

## Scripts
- `scripts/setup.sh`: Setup script.
- `scripts/run_local.sh`: Run local script.
- `scripts/build_image.sh`: Build script.
- `scripts/deploy.sh`: Deploy script.

## Ops & Docs
- `mlflow/README.md`: MLflow docs.
- `prometheus/prometheus.yml`: Prometheus config.
- `grafana/README.md`: Grafana docs.
- `docs/architecture.md`: Architecture docs.
- `docs/operations.md`: Operations docs.
- `examples/demo_requests.md`: Demo requests.
