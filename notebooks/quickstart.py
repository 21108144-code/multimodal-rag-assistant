# Quickstart Guide
# This script demonstrates the end-to-end flow of the Multimodal RAG system.

import os
from PIL import Image
from src.data.ingest import DataIngestor
from src.inference.pipeline import RAGPipeline

def main():
    print("=== Multimodal RAG Quickstart ===")
    
    # 1. Setup Data
    print("\n[1] Ingesting Data...")
    ingestor = DataIngestor()
    
    # Create dummy data
    os.makedirs("data/raw/images", exist_ok=True)
    img_path = "data/raw/images/sample.jpg"
    Image.new("RGB", (224, 224), color="red").save(img_path)
    
    texts = ["This is a red image.", "This is a blue image."]
    metadata = [{"text": t, "id": i} for i, t in enumerate(texts)]
    
    # 2. Initialize Pipeline
    print("\n[2] Initializing Pipeline...")
    pipeline = RAGPipeline()
    
    # 3. Index Data
    print("\n[3] Indexing Data...")
    # For demo, we just index text. In real app, we'd process images too.
    pipeline.index_data([], texts, metadata)
    
    # 4. Query
    query = "What color is the image?"
    print(f"\n[4] Querying: '{query}'")
    result = pipeline.query(query)
    
    print("\n=== Result ===")
    print(f"Answer: {result['answer']}")
    print("Sources:")
    for source in result['sources']:
        print(f"- {source['metadata']['text']} (Score: {source['score']:.4f})")

if __name__ == "__main__":
    main()
