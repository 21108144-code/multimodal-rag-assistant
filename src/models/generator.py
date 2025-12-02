from openai import OpenAI
from src.config import settings
from src.utils.logging import logger

class RAGGenerator:
    def __init__(self, model_name: str = settings.GENERATOR_MODEL_NAME):
        self.model_name = model_name
        logger.info(f"Initializing Groq API client with model: {model_name}")
        
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is not set!")
            
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url=settings.GROQ_BASE_URL
        )

    def generate_answer(self, query: str, context: list[str], history: list[dict] = []) -> str:
        context_str = "\n".join(context)
        
        # Base system message
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful and intelligent AI assistant. Use the context provided to answer the user's question. If the answer is not in the context, say so politely."
            }
        ]
        
        # Add conversation history
        for msg in history:
            # Ensure we only pass valid roles to the API
            if msg.get("role") in ["user", "assistant"]:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current turn
        messages.append({
            "role": "user", 
            "content": f"Context:\n{context_str}\n\nQuestion: {query}"
        })
        
        try:
            logger.info(f"Calling Groq API with model: {self.model_name}")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            
            answer = response.choices[0].message.content
            logger.info("Groq API call successful")
            return answer
            
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
