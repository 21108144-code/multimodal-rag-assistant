import os
import sys
os.environ["PYTHONPATH"] = "C:\\mlopsproject"
sys.path.insert(0, "C:\\mlopsproject")

from src.utils.logging import logger

def reindex():
    logger.info("Starting simplified re-indexing...")
    
    try:
        from src.models.encoder import CLIPEncoder
        from src.models.retriever import FAISSRetriever
        
        logger.info("Loading CLIP encoder...")
        encoder = CLIPEncoder()
        
        logger.info("Creating retriever...")
        retriever = FAISSRetriever()
        
        # Load knowledge base (JSON)
        import json
        kb_path = "data/knowledge_base.json"
        if os.path.exists(kb_path):
            with open(kb_path, "r") as f:
                data = json.load(f)
                texts = [item["text"] for item in data]
                logger.info(f"Loaded {len(texts)} items from JSON knowledge base.")
        else:
            texts = []

        # Load PDFs
        pdf_dir = "data/pdfs"
        if os.path.exists(pdf_dir):
            from src.data.ingest import PDFIngestor
            pdf_ingestor = PDFIngestor()
            pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
            for pdf_file in pdf_files:
                pdf_path = os.path.join(pdf_dir, pdf_file)
                logger.info(f"Ingesting PDF: {pdf_file}")
                pdf_text = pdf_ingestor.load_pdf(pdf_path)
                # Chunk the PDF text (simple chunking by paragraphs or length)
                # For simplicity, let's just split by newlines for now, or keep it as one big chunk if small
                # Better: Split into chunks of ~500 characters
                chunks = [pdf_text[i:i+500] for i in range(0, len(pdf_text), 500)]
                texts.extend(chunks)
                logger.info(f"Extracted {len(chunks)} chunks from {pdf_file}")
        
        if not texts:
            logger.warning("No data found! Using dummy data.")
            texts = ["The quick brown fox jumps over the lazy dog."]
        
        logger.info(f"Encoding {len(texts)} text samples...")
        
        # Batch processing
        batch_size = 32
        all_embeddings = []
        
        import numpy as np
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            logger.info(f"Encoding batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}...")
            try:
                batch_embeddings = encoder.encode_text(batch_texts).cpu().numpy()
                all_embeddings.append(batch_embeddings)
            except Exception as e:
                logger.error(f"Error encoding batch {i}: {e}")
                # Skip this batch or handle it
                continue
                
        if not all_embeddings:
            raise ValueError("No embeddings were generated!")
            
        embeddings = np.vstack(all_embeddings)
        
        metadata = [{"text": t, "id": i} for i, t in enumerate(texts)]
        
        logger.info("Adding embeddings to index...")
        retriever.add_embeddings(embeddings, metadata)
        
        logger.info("Saving index...")
        retriever.save_index()
        
        logger.info("✅ Re-indexing complete!")
        
    except Exception as e:
        logger.error(f"❌ Error during re-indexing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    reindex()
