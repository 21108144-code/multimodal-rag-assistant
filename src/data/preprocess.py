import json
from pathlib import Path
from typing import List, Dict
from PIL import Image
from src.config import settings
from src.utils.logging import logger

class Preprocessor:
    def __init__(self, processed_dir: str = settings.PROCESSED_DATA_DIR):
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def resize_image(self, image_path: str, size: tuple = (224, 224)) -> str:
        """Resizes an image and saves it to processed dir."""
        try:
            img = Image.open(image_path).convert("RGB")
            img = img.resize(size)
            filename = Path(image_path).name
            dst = self.processed_dir / filename
            img.save(dst)
            return str(dst)
        except Exception as e:
            logger.error(f"Error resizing image {image_path}: {e}")
            return image_path

    def create_manifest(self, data: List[Dict], output_path: str):
        """Creates a JSONL manifest."""
        with open(output_path, "w") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")
        logger.info(f"Manifest created at {output_path}")

def preprocess_data():
    """Example preprocessing script."""
    logger.info("Starting preprocessing...")
    # Placeholder logic
