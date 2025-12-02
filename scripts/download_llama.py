import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
TOKEN = os.getenv("HF_TOKEN")

def download_model():
    print(f"Downloading {MODEL_NAME}...")
    print("This may take several minutes (model is ~6GB)...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=TOKEN)
        print("Tokenizer downloaded successfully!")
        
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, 
            token=TOKEN,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        print("Model downloaded successfully!")
        print("Download complete!")
    except Exception as e:
        print(f"Error downloading model: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    download_model()
