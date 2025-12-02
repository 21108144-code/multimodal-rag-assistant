import json
import torch
from torch.utils.data import Dataset
from PIL import Image
from typing import List, Dict, Callable, Optional

class MultimodalDataset(Dataset):
    def __init__(
        self, 
        manifest_path: str, 
        transform: Optional[Callable] = None,
        tokenizer: Optional[Callable] = None
    ):
        self.data = []
        with open(manifest_path, "r") as f:
            for line in f:
                self.data.append(json.loads(line))
        self.transform = transform
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        image_path = item["image_path"]
        text = item["text"]

        image = Image.open(image_path).convert("RGB")
        if self.transform:
            image = self.transform(image)

        if self.tokenizer:
            text_tokens = self.tokenizer(text)
            return image, text_tokens

        return image, text
