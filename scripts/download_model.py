from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

model_name = "google/flan-t5-base"
print(f"Downloading {model_name}... this may take a while (~1GB)...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print(f"Successfully downloaded {model_name}!")
