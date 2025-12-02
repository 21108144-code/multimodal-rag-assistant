# Multimodal RAG Project - Interview Preparation Guide

This document provides a complete, deep-dive analysis of the Multimodal RAG project. It is designed to help you explain every aspect of the system in a technical interview.

---

## 1. Project Overview (The "Elevator Pitch")

**"I built a Multimodal Retrieval-Augmented Generation (RAG) system that allows users to chat with their documents (PDFs) and images."**

Unlike traditional text-only RAG systems, this project handles **multimodal inputs**. It uses **CLIP** to embed both text and images into a shared vector space and **Llama 3.3 (via Groq)** for high-speed generation. It features a modern, ChatGPT-like frontend, a robust FastAPI backend, and a scalable vector search implementation using FAISS.

**Key Tech Stack:**
- **LLM:** Llama 3.3 70B (via Groq API)
- **Embeddings:** CLIP (OpenAI/HuggingFace)
- **Vector DB:** FAISS
- **Backend:** FastAPI
- **Frontend:** Vanilla JS/HTML/CSS (Modern Chat UI)
- **Ops:** Docker, Prometheus, Grafana

---

## 2. Architecture Flow

```mermaid
graph TD
    User[User] -->|Text/Image Query| Frontend[Frontend (HTML/JS)]
    Frontend -->|HTTP POST| API[FastAPI Backend]
    
    subgraph "Inference Pipeline"
        API -->|Request| Pipeline[RAGPipeline]
        Pipeline -->|1. Check| Greeting[Greeting Detector]
        Pipeline -->|2. Encode| Encoder[CLIP Encoder]
        Pipeline -->|3. Search| Retriever[FAISS Vector DB]
        Pipeline -->|4. Generate| Generator[Groq LLM]
    end
    
    subgraph "Data Ingestion (Offline)"
        PDFs[PDF Documents] -->|Extract| Ingest[PDF Ingestor]
        Ingest -->|Chunk| Chunker[Text Chunker]
        Chunker -->|Encode| Encoder
        Encoder -->|Save| Retriever
    end

    Pipeline -->|Context + History| Generator
    Retriever -->|Relevant Chunks| Pipeline
    Generator -->|Answer| API
    API -->|JSON Response| Frontend
```

---

## 3. File-by-File Deep Dive

### `src/inference/pipeline.py`
**Role:** The "Brain" of the application.
- **Purpose:** Orchestrates the entire RAG process. It connects the Encoder, Retriever, and Generator.
- **Key Logic:**
    - `__init__`: Initializes `CLIPEncoder`, `FAISSRetriever`, `RAGGenerator`, and `EasyOCR`.
    - `query(query, history)`:
        1.  **Greeting Check:** Checks if the input is just "Hi" or "Hello" using Regex to avoid wasting API calls.
        2.  **Input Handling:**
            - If **Text**: Encodes text using CLIP.
            - If **Image**: Runs **OCR (EasyOCR)** to extract text. If text is found, it searches for that text. If not, it uses the image's visual embedding.
        3.  **Retrieval:** Calls `retriever.search()` to find the top 5 most relevant document chunks.
        4.  **Generation:** Passes the user query, retrieved context, and chat history to `generator.generate_answer()`.
- **Why this design?** Decoupling the pipeline from the API allows for easy testing and potential CLI usage.

### `src/models/encoder.py`
**Role:** The "Translator" (Text/Image → Numbers).
- **Purpose:** Converts human-readable text and images into vector embeddings (lists of numbers) that computers can compare.
- **Key Components:**
    - `CLIPModel`, `CLIPProcessor`: Loads the pre-trained CLIP model from HuggingFace.
    - `encode_text()`: Tokenizes text and passes it through the CLIP text encoder. Normalizes vectors for cosine similarity.
    - `encode_image()`: Preprocesses images and passes them through the CLIP image encoder.
- **Technical Concept:** **Shared Latent Space**. CLIP is trained to map similar images and text to the same point in vector space. This allows us to search for text using images and vice versa.

### `src/models/retriever.py`
**Role:** The "Librarian" (Storage & Search).
- **Purpose:** Stores the vector embeddings and finds the closest matches to a query.
- **Key Components:**
    - `faiss.IndexFlatIP`: Uses "Inner Product" (equivalent to Cosine Similarity for normalized vectors) for fast similarity search.
    - `add_embeddings()`: Adds vectors to the index and stores their corresponding text in `self.metadata`.
    - `search()`: Returns the `k` nearest neighbors to the query vector.
    - `save_index()` / `load_index()`: Persists the index and metadata to disk (`artifacts/faiss_index.bin`) so we don't have to re-ingest data on every restart.

### `src/models/generator.py`
**Role:** The "Speaker" (LLM).
- **Purpose:** Generates the final natural language answer.
- **Key Components:**
    - `OpenAI` Client: Used to connect to **Groq API** (which is OpenAI-compatible).
    - `generate_answer()`: Constructs the prompt.
        - **System Prompt:** "You are a helpful AI..."
        - **History:** Appends previous user/assistant messages for context.
        - **Context:** Appends the retrieved text chunks.
        - **Query:** Appends the user's latest question.
- **Why Groq?** It provides extremely fast inference (LPU) for Llama 3 models, making the chat feel real-time.

### `src/api/app.py`
**Role:** The "Doorway" (Web Server).
- **Purpose:** Exposes the pipeline as a REST API.
- **Key Endpoints:**
    - `POST /query`: Handles text chat. Accepts `text` and `history`.
    - `POST /query/image`: Handles image uploads.
    - `GET /`: Serves the frontend (`index.html`).
    - `GET /metrics`: Exposes Prometheus metrics (latency, request count).
- **Design:** Uses **FastAPI** for async performance and automatic validation (Pydantic).

### `src/data/ingest.py`
**Role:** The "Reader".
- **Purpose:** Extracts raw text from files.
- **Key Components:**
    - `PDFIngestor`: Uses `pypdf` to read text from PDF pages.
    - `DataIngestor`: (Legacy) Helper for loading images.

### `scripts/reindex.py`
**Role:** The "Builder".
- **Purpose:** Offline script to process data and build the vector index.
- **Workflow:**
    1.  Scans `data/pdfs`.
    2.  Extracts text using `PDFIngestor`.
    3.  **Chunks** text into 500-character segments (crucial for RAG context limits).
    4.  **Batches** encoding (size 32) to prevent memory crashes.
    5.  Saves the FAISS index to disk.

### `src/api/static/` (`index.html`, `style.css`)
**Role:** The "Face".
- **Purpose:** A clean, modern chat interface.
- **Features:**
    - **Chat History:** Maintains state in JavaScript.
    - **Markdown Rendering:** Formats the LLM's bold text/lists.
    - **Responsive Design:** Flexbox layout for proper scrolling.

---

## 4. Technical Concepts Explained

### What is RAG (Retrieval-Augmented Generation)?
RAG is a technique to give LLMs "long-term memory" without re-training them.
1.  **Retrieval:** When you ask a question, the system searches your private database (FAISS) for relevant information.
2.  **Augmentation:** It pastes that information into the prompt sent to the LLM.
3.  **Generation:** The LLM answers using that specific information.

### Why Multimodal?
Standard RAG only understands text. This system uses **CLIP**, which understands both.
- If you upload a photo of a cat, CLIP converts it to a vector.
- We can search our text database for "cat" concepts using that image vector.
- **OCR Fallback:** For document screenshots (which contain text, not just visual concepts), we extract the text first to get better search results.

### Vector Database (FAISS)
Think of it as a "semantic search engine." Instead of matching keywords (like Ctrl+F), it matches **meanings**.
- "King" - "Man" + "Woman" ≈ "Queen"
- FAISS calculates the distance between your question's vector and every document's vector to find the closest meanings.

---

## 5. Request Flow (Step-by-Step)

1.  **User** types "What is the penalty for unauthorized marriage?" in the UI.
2.  **Frontend** sends a POST request to `/query` with the text and chat history.
3.  **FastAPI** receives the request and calls `pipeline.query()`.
4.  **Pipeline** checks for greetings (it's not one).
5.  **Encoder** converts the question into a 512-dimensional vector.
6.  **Retriever** searches FAISS and finds 5 chunks of text from the "Muslim Family Laws Ordinance" PDF.
7.  **Generator** receives a prompt: *"Context: [PDF Chunks]... Question: What is the penalty...?"*
8.  **Groq API (Llama 3)** generates the answer: *"The penalty is simple imprisonment up to one year..."*
9.  **Backend** returns the answer to the Frontend.
10. **Frontend** displays the answer.

---

## 6. Key Challenges & Solutions

| Challenge | Solution |
| :--- | :--- |
| **Hallucinations** | Used RAG to ground the LLM in facts. If the info isn't in the PDF, it says "I don't know." |
| **Image Text Retrieval** | CLIP is bad at reading text in images. Added **EasyOCR** to extract text from images before embedding. |
| **Slow Inference** | Switched from local Flan-T5 (slow) to **Groq API** (Llama 3), reducing latency from 10s to <1s. |
| **Context Limits** | Implemented **Chunking** (500 chars) in `reindex.py` to fit relevant info into the LLM's context window. |
| **Memory Crashes** | Implemented **Batch Processing** (batch size 32) in the encoding step to handle large PDFs. |

---

## 7. Potential Interview Questions

**Q: Why did you use FAISS instead of Pinecone or Milvus?**
**A:** FAISS is lightweight, runs locally, and is perfect for this scale (thousands of chunks). For a distributed production system with millions of vectors, I would migrate to a managed service like Pinecone.

**Q: How do you handle data privacy?**
**A:** Currently, the vector DB is local. However, we use the Groq API, so data leaves the premise. For a strictly private deployment, I would swap Groq for a local generic LLM (like Llama.cpp) running on-premise.

**Q: How would you scale this?**
**A:**
1.  **Async Ingestion:** Use a message queue (Kafka) for processing PDFs so the user doesn't wait.
2.  **Vector DB:** Move to a distributed vector DB (Milvus).
3.  **Caching:** Cache frequent queries (Redis) to avoid hitting the LLM.

**Q: What happens if the PDF is scanned (images)?**
**A:** My `PDFIngestor` currently uses `pypdf`, which extracts text layers. For scanned PDFs, I would integrate the `EasyOCR` module into the ingestion pipeline to OCR every page before chunking.
