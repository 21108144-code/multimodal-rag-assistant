# Multimodal RAG Portfolio

![CI](https://github.com/username/multimodal-rag-portfolio/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/docker-enabled-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

**Multimodal RAG Portfolio** is an end-to-end Machine Learning Operations (MLOps) project demonstrating a production-ready Retrieval-Augmented Generation (RAG) system capable of processing both text and images.

This system ingests multimodal data (product manuals, FAQs, screenshots), generates joint embeddings using CLIP/OpenCLIP, indexes them in a vector database (FAISS/Milvus), and serves a high-performance FastAPI inference endpoint. It includes a complete MLOps lifecycle with experiment tracking, CI/CD, infrastructure-as-code, and monitoring.

## Architecture

```mermaid
graph TD
    subgraph Data Pipeline
    A[Raw Data (Images/Text)] --> B[Ingestor]
    B --> C[Preprocessor (OCR/Resize)]
    C --> D[Multimodal Dataset]
    end

    subgraph Training & Indexing
    D --> E[Encoder (CLIP)]
    E --> F[Vector Index (FAISS/Milvus)]
    E --> G[MLflow Experiment Tracking]
    end

    subgraph Inference Service
    H[User Query (Text/Image)] --> I[FastAPI Gateway]
    I --> J[Retriever]
    F -.-> J
    J --> K[Generator (LLM)]
    K --> L[Response]
    end

    subgraph MLOps & Infra
    M[GitHub Actions CI/CD] --> N[Container Registry]
    N --> O[Kubernetes (GKE)]
    P[Prometheus/Grafana] -.-> I
    end
```

## Key Features

- **Multimodal Ingestion**: Handles images and text, performing OCR and preprocessing.
- **State-of-the-Art Embeddings**: Uses CLIP/OpenCLIP for joint image-text vector space.
- **Hybrid Retrieval**: Combines vector similarity with keyword search (BM25).
- **Generative AI**: Integrates LLMs (e.g., Flan-T5) for answer synthesis.
- **Production API**: FastAPI service with Pydantic validation and async endpoints.
- **MLOps Stack**:
  - **Tracking**: MLflow for experiment and model registry.
  - **CI/CD**: GitHub Actions for automated testing and deployment.
  - **IaC**: Terraform for cloud infrastructure (GCP/AWS).
  - **Monitoring**: Prometheus and Grafana for metrics and dashboards.
  - **Containerization**: Docker and Kubernetes manifests.

## Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Make

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/username/multimodal-rag-portfolio.git
    cd multimodal-rag-portfolio
    ```

2.  **Install dependencies:**
    ```bash
    make setup
    ```

3.  **Run the application locally:**
    ```bash
    make run-api
    ```
    Access the API docs at `http://localhost:8000/docs`.

4.  **Run tests:**
    ```bash
    make test
    ```

### Deployment

1.  **Build Docker Image:**
    ```bash
    make build
    ```

2.  **Deploy to Staging (Simulated):**
    ```bash
    make deploy-staging
    ```

## Project Structure

```
├── .github/            # CI/CD workflows
├── docs/               # Documentation
├── infra/              # Terraform & Kubernetes manifests
# Multimodal RAG Portfolio

![CI](https://github.com/username/multimodal-rag-portfolio/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/docker-enabled-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

**Multimodal RAG Portfolio** is an end-to-end Machine Learning Operations (MLOps) project demonstrating a production-ready Retrieval-Augmented Generation (RAG) system capable of processing both text and images.

This system ingests multimodal data (product manuals, FAQs, screenshots), generates joint embeddings using CLIP/OpenCLIP, indexes them in a vector database (FAISS/Milvus), and serves a high-performance FastAPI inference endpoint. It includes a complete MLOps lifecycle with experiment tracking, CI/CD, infrastructure-as-code, and monitoring.

## Architecture

```mermaid
graph TD
    subgraph Data Pipeline
    A[Raw Data (Images/Text)] --> B[Ingestor]
    B --> C[Preprocessor (OCR/Resize)]
    C --> D[Multimodal Dataset]
    end

    subgraph Training & Indexing
    D --> E[Encoder (CLIP)]
    E --> F[Vector Index (FAISS/Milvus)]
    E --> G[MLflow Experiment Tracking]
    end

    subgraph Inference Service
    H[User Query (Text/Image)] --> I[FastAPI Gateway]
    I --> J[Retriever]
    F -.-> J
    J --> K[Generator (LLM)]
    K --> L[Response]
    end

    subgraph MLOps & Infra
    M[GitHub Actions CI/CD] --> N[Container Registry]
    N --> O[Kubernetes (GKE)]
    P[Prometheus/Grafana] -.-> I
    end
```

## Key Features

- **Multimodal Ingestion**: Handles images and text, performing OCR and preprocessing.
- **State-of-the-Art Embeddings**: Uses CLIP/OpenCLIP for joint image-text vector space.
- **Hybrid Retrieval**: Combines vector similarity with keyword search (BM25).
- **Generative AI**: Integrates LLMs (e.g., Flan-T5) for answer synthesis.
- **Production API**: FastAPI service with Pydantic validation and async endpoints.
- **MLOps Stack**:
  - **Tracking**: MLflow for experiment and model registry.
  - **CI/CD**: GitHub Actions for automated testing and deployment.
  - **IaC**: Terraform for cloud infrastructure (GCP/AWS).
  - **Monitoring**: Prometheus and Grafana for metrics and dashboards.
  - **Containerization**: Docker and Kubernetes manifests.

## Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Make

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/username/multimodal-rag-portfolio.git
    cd multimodal-rag-portfolio
    ```

2.  **Install dependencies:**
    ```bash
    make setup
    ```

3.  **Run the application locally:**
    ```bash
    make run-api
    ```
    Access the API docs at `http://localhost:8000/docs`.

4.  **Run tests:**
    ```bash
    make test
    ```

### Deployment

1.  **Build Docker Image:**
    ```bash
    make build
    ```

2.  **Deploy to Staging (Simulated):**
    ```bash
    make deploy-staging
    ```

## Project Structure

```
├── .github/            # CI/CD workflows
├── docs/               # Documentation
├── infra/              # Terraform & Kubernetes manifests
├── src/                # Source code
│   ├── api/            # FastAPI application
│   ├── data/           # Data ingestion & preprocessing
│   ├── inference/      # RAG pipeline
│   ├── models/         # Encoder, Retriever, Generator
│   └── utils/          # Logging, Metrics, IO
├── tests/              # Unit & Integration tests
├── Dockerfile          # Service container definition
├── Makefile            # Developer commands
└── requirements.txt    # Python dependencies
```

## 📚 Knowledge Base

The system uses a hybrid knowledge base:
1.  **JSON Data**: `data/knowledge_base.json` (for definitions and facts).
2.  **PDF Documents**: `data/pdfs/` (for long-form documents).

### How to Add New Data
1.  **Add PDFs**: Place your `.pdf` files in the `data/pdfs/` folder.
2.  **Add Facts**: Edit `data/knowledge_base.json` to add new entries.
3.  **Re-index**: Run the re-indexing script:
    ```bash
    python scripts/reindex.py
    ```
4.  **Restart Server**: Restart the API server to load the new data.

## 🚀 Future Roadmap

Here are the planned improvements and potential extensions for this project:

- [ ] **Scalable Vector DB**: Migrate from local FAISS to a distributed solution like **Milvus** or **Pinecone** for handling millions of documents.
- [ ] **Async Ingestion**: Implement a **Kafka** or **RabbitMQ** pipeline to process file uploads asynchronously, preventing user wait times.
- [ ] **Caching Layer**: Integrate **Redis** to cache frequent queries and reduce LLM costs/latency.
- [ ] **Advanced Chunking**: Move from fixed-size chunking to semantic chunking or recursive character splitting for better context retrieval.
- [ ] **Quantization**: Implement model quantization (e.g., ONNX, TensorRT) to reduce memory usage and speed up inference on smaller devices.
- [ ] **User Auth**: Add user authentication (OAuth2) to secure the API and manage per-user chat history.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
