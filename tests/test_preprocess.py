import os
import pytest
from PIL import Image
from src.data.preprocess import Preprocessor

@pytest.fixture
def preprocessor(tmp_path):
    return Preprocessor(processed_dir=str(tmp_path))

def test_resize_image(preprocessor, tmp_path):
    # Create dummy image
    img_path = tmp_path / "test.jpg"
    Image.new("RGB", (500, 500)).save(img_path)
    
    processed_path = preprocessor.resize_image(str(img_path), size=(100, 100))
    
    assert os.path.exists(processed_path)
    with Image.open(processed_path) as img:
        assert img.size == (100, 100)
