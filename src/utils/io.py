import json
import os
from typing import Any, Dict, List

def save_json(data: Any, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_json(path: str) -> Any:
    with open(path, "r") as f:
        return json.load(f)

def save_text(text: str, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)

def load_text(path: str) -> str:
    with open(path, "r") as f:
        return f.read()
