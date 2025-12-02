# System Architecture

## Overview
The Multimodal RAG system is designed to handle both text and image queries by leveraging a shared embedding space (CLIP).

## Components

### 1. Data Ingestion
- **Ingestor**: Reads raw files (images, text).
- **Preprocessor**: Resizes images, normalizes text, creates a JSONL manifest.

### 2. Indexing
- **Encoder**: CLIP model (ViT-B/32) encodes images and text into 512-dim vectors.
- **Vector DB**: FAISS (IndexFlatIP) stores normalized embeddings for cosine similarity search.

### 3. Retrieval
- **Query**: User input (text/image) is encoded.
- **Search**: FAISS finds top-k nearest neighbors.

### 4. Generation
- **LLM**: Flan-T5 (or similar Seq2Seq model) takes the query + retrieved context to generate a natural language answer.

### 5. Serving
- **FastAPI**: Async web server.
- **Endpoints**: `/query` (text), `/query/image` (image upload).

## Infrastructure
- **Docker**: Containerized application.
- **Kubernetes**: Orchestration for scaling.
- **Terraform**: Infrastructure provisioning on GCP.
