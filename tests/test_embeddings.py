import pytest
import torch
from PIL import Image
from src.models.encoder import CLIPEncoder

@pytest.fixture
def encoder():
    return CLIPEncoder()

def test_encode_text(encoder):
    texts = ["Hello world", "Another sentence"]
    embeddings = encoder.encode_text(texts)
    assert embeddings.shape == (2, 512)
    assert isinstance(embeddings, torch.Tensor)

def test_encode_image(encoder):
    images = [Image.new("RGB", (224, 224)) for _ in range(2)]
    embeddings = encoder.encode_image(images)
    assert embeddings.shape == (2, 512)
    assert isinstance(embeddings, torch.Tensor)
