from PIL import Image
from typing import List, Union, Optional
from src.models.encoder import CLIPEncoder
from src.models.retriever import FAISSRetriever
from src.models.generator import RAGGenerator
from src.utils.logging import logger

class RAGPipeline:
    def __init__(self):
        self.encoder = CLIPEncoder()
        self.retriever = FAISSRetriever()
        self.retriever.load_index()
        self.generator = RAGGenerator()
        try:
            import easyocr
            self.reader = easyocr.Reader(['en'], gpu=False) # CPU for compatibility
            logger.info("OCR Reader initialized.")
        except Exception as e:
            logger.warning(f"Could not initialize OCR: {e}")
            self.reader = None

    def index_data(self, images: List[Image.Image], texts: List[str], metadata: List[dict]):
        image_embeddings = self.encoder.encode_image(images).cpu().numpy()
        text_embeddings = self.encoder.encode_text(texts).cpu().numpy()
        
        # Combine or choose one. For simplicity, let's just index text embeddings for now 
        # or assume we are indexing multimodal embeddings in a shared space.
        # Here we'll just add text embeddings to demonstrate.
        self.retriever.add_embeddings(text_embeddings, metadata)
        self.retriever.save_index()

    def query(self, query: Union[str, Image.Image], k: int = 5, history: list = []) -> dict:
        if isinstance(query, str):
            # Handle greetings and chit-chat
            q_lower = query.lower()
            greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
            conversational = ["how are you", "who are you", "what is your name", "what can you do"]
            
            import re
            def is_whole_word(word, text):
                return re.search(r'\b' + re.escape(word) + r'\b', text) is not None

            is_greeting = any(is_whole_word(g, q_lower) for g in greetings)
            is_conversational = any(c in q_lower for c in conversational)
            
            if is_greeting or is_conversational:
                if "how are you" in q_lower:
                    return {"answer": "I'm doing well, thank you! I am an AI assistant designed to help you with RAG and MLOps questions. How can I help you today?", "sources": []}
                if "who are you" in q_lower or "your name" in q_lower:
                    return {"answer": "I am a Multimodal RAG assistant. I can answer questions about documents and analyze images.", "sources": []}
                return {
                    "answer": "Hello! I am your AI assistant. I can help you analyze documents and images. What would you like to know?",
                    "sources": []
                }
                
            query_embedding = self.encoder.encode_text([query]).cpu().numpy()
            query_text = query
        else:
            query_embedding = self.encoder.encode_image([query]).cpu().numpy()
            # Perform OCR
            query_text = "Describe this image."
            if self.reader:
                try:
                    import numpy as np
                    img_np = np.array(query)
                    ocr_result = self.reader.readtext(img_np, detail=0)
                    extracted_text = " ".join(ocr_result)
                    if extracted_text and len(extracted_text) > 10:
                        query_text = f"Image contains text: {extracted_text}. Explain this."
                        # CRITICAL FIX: Use the extracted text for retrieval, not the image embedding
                        logger.info(f"OCR Extracted: {extracted_text[:50]}... Using text for retrieval.")
                        query_embedding = self.encoder.encode_text([extracted_text]).cpu().numpy()
                    else:
                         logger.info("OCR found little/no text. Using image embedding.")
                except Exception as e:
                    logger.error(f"OCR Failed: {e}")
            
        retrieved_items = self.retriever.search(query_embedding, k=k)
        
        context = [item["metadata"].get("text", "") for item in retrieved_items]
        
        # Convert Pydantic models to dicts if needed
        history_dicts = []
        for h in history:
            if hasattr(h, 'dict'):
                history_dicts.append(h.dict())
            elif isinstance(h, dict):
                history_dicts.append(h)
                
        answer = self.generator.generate_answer(query_text, context, history=history_dicts)
        
        return {
            "answer": answer,
            "sources": retrieved_items
        }
