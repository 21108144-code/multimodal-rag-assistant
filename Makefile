.PHONY: setup test lint run-api build deploy-staging clean

PYTHON := python
PIP := pip

setup:
	$(PIP) install -r requirements.txt

test:
	pytest tests/

lint:
	black src/ tests/
	flake8 src/ tests/

run-api:
	uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload

build:
	docker build -t multimodal-rag:latest .

deploy-staging:
	@echo "Deploying to staging..."
	./scripts/deploy.sh staging

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
