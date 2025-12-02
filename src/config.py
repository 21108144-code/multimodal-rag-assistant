import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Multimodal RAG"
    ENV: str = "development"
    DEBUG: bool = True
    
    # Paths
    DATA_DIR: str = "data"
    RAW_DATA_DIR: str = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR: str = os.path.join(DATA_DIR, "processed")
    ARTIFACTS_DIR: str = "artifacts"
    
    # Model
    ENCODER_MODEL_NAME: str = "openai/clip-vit-base-patch32"
    GENERATOR_MODEL_NAME: str = "llama-3.3-70b-versatile"  # Using Groq API
    DEVICE: str = "cpu"  # Not needed for API calls
    
    # Groq API
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    
    # Vector DB
    INDEX_PATH: str = os.path.join(ARTIFACTS_DIR, "faiss_index.bin")
    EMBEDDING_DIM: int = 512
    
    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    
    class Config:
        env_file = ".env"

settings = Settings()
