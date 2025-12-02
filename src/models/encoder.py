import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from src.config import settings
from src.utils.logging import logger

class CLIPEncoder:
    def __init__(self, model_name: str = settings.ENCODER_MODEL_NAME):
        self.device = settings.DEVICE
        logger.info(f"Loading CLIP model: {model_name} on {self.device}")
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def encode_text(self, texts: list[str]) -> torch.Tensor:
        inputs = self.processor(text=texts, return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            embeddings = self.model.get_text_features(**inputs)
        return embeddings / embeddings.norm(p=2, dim=-1, keepdim=True)

    def encode_image(self, images: list[Image.Image]) -> torch.Tensor:
        inputs = self.processor(images=images, return_tensors="pt").to(self.device)
        with torch.no_grad():
            embeddings = self.model.get_image_features(**inputs)
        return embeddings / embeddings.norm(p=2, dim=-1, keepdim=True)
