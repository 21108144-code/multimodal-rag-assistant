import pytest
import numpy as np
from src.models.retriever import FAISSRetriever

@pytest.fixture
def retriever(tmp_path):
    return FAISSRetriever(dim=128, index_path=str(tmp_path / "index.bin"))

def test_add_and_search(retriever):
    # Create random embeddings
    embeddings = np.random.rand(10, 128).astype("float32")
    # Normalize
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    metadata = [{"id": i} for i in range(10)]
    
    retriever.add_embeddings(embeddings, metadata)
    
    # Search for the first vector
    query = embeddings[0:1]
    results = retriever.search(query, k=1)
    
    assert len(results) == 1
    assert results[0]["metadata"]["id"] == 0
