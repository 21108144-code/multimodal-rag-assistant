import faiss
import numpy as np
import os
from src.config import settings
from src.utils.logging import logger

class FAISSRetriever:
    def __init__(self, dim: int = settings.EMBEDDING_DIM, index_path: str = settings.INDEX_PATH):
        self.dim = dim
        self.index_path = index_path
        self.index = faiss.IndexFlatIP(dim)  # Inner Product for cosine similarity (normalized vectors)
        self.metadata = []  # Simple list to store metadata corresponding to IDs

    def add_embeddings(self, embeddings: np.ndarray, metadata: list[dict]):
        if embeddings.shape[1] != self.dim:
            raise ValueError(f"Embedding dimension mismatch. Expected {self.dim}, got {embeddings.shape[1]}")
        
        self.index.add(embeddings)
        self.metadata.extend(metadata)
        logger.info(f"Added {len(embeddings)} embeddings to index.")

    def search(self, query_embedding: np.ndarray, k: int = 5):
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "score": float(distances[0][i]),
                    "metadata": self.metadata[idx]
                })
        return results

    def save_index(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        
        # Save metadata
        metadata_path = self.index_path + ".meta.json"
        import json
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f)
            
        logger.info(f"Index saved to {self.index_path}")

    def load_index(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            
            # Load metadata
            metadata_path = self.index_path + ".meta.json"
            if os.path.exists(metadata_path):
                import json
                with open(metadata_path, "r") as f:
                    self.metadata = json.load(f)
            else:
                logger.warning("Index found but no metadata file.")
                self.metadata = []
                
            logger.info(f"Index loaded from {self.index_path}")
        else:
            logger.warning(f"Index not found at {self.index_path}, starting fresh.")
