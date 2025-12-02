import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# Mocking pipeline for query test would be ideal, but for now we test structure
# def test_query_endpoint():
#     response = client.post("/query", json={"text": "test query"})
#     # This might fail if models aren't loaded or mock isn't set up
#     # assert response.status_code == 200
