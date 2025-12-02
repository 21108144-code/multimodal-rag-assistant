import logging
import sys
from src.config import settings

def setup_logging():
    logger = logging.getLogger("multimodal_rag")
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

logger = setup_logging()
