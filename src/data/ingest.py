import os
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

class DataIngestor:
    def __init__(self):
        self.image_extensions = ['.jpg', '.jpeg', '.png']
        
    def load_images(self, data_dir: str) -> list[Image.Image]:
        images = []
        for filename in os.listdir(data_dir):
            if any(filename.lower().endswith(ext) for ext in self.image_extensions):
                path = os.path.join(data_dir, filename)
                try:
                    image = Image.open(path).convert("RGB")
                    images.append(image)
                except Exception as e:
                    print(f"Error loading image {path}: {e}")
        return images

class PDFIngestor:
    def load_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        import pypdf
        text = ""
        try:
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""
