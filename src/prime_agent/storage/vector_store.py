"""
ChromaDB wrapper using Local Embeddings (HuggingFace) to avoid API rate limits.
"""
from typing import List, Dict, Optional
import logging
import shutil
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from prime_agent.config import CHROMA_PATH

logger = logging.getLogger(__name__)

class VectorStore:
    """
    Manages ChromaDB interactions using local CPU embeddings.
    """
    def __init__(self, persist_directory: str = CHROMA_PATH):
        self.persist_directory = persist_directory
        
        # Initialize Local Embeddings (Runs on your CPU, $0 cost, No Rate Limits)
        logger.info("⬇️ Loading local embedding model 'all-MiniLM-L6-v2'...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Initialize Chroma with local embeddings
        self.vector_store = Chroma(
            collection_name="prime_docs",
            embedding_function=self.embeddings,
            persist_directory=persist_directory,
        )

    def add_documents(self, documents: List[str], metadata: List[Dict], ids: List[str]):
        """
        Adds documents to the vector store using local CPU power.
        """
        batch_size = 32  # Local models are fast; we can process larger batches
        total_docs = len(documents)
        logger.info(f"🚀 Embedding {total_docs} documents locally (No API limits)...")

        for i in range(0, total_docs, batch_size):
            batch_docs = documents[i : i + batch_size]
            batch_meta = metadata[i : i + batch_size]
            batch_ids = ids[i : i + batch_size]
            
            try:
                self.vector_store.add_texts(
                    texts=batch_docs,
                    metadatas=batch_meta,
                    ids=batch_ids
                )
                logger.info(f"✅ Processed batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size}")
            except Exception as e:
                logger.error(f"❌ Error embedding batch: {e}")

    def search(self, query: str, k: int = 5, filter: Optional[Dict] = None) -> List[Dict]:
        """
        Search for relevant documents.
        """
        try:
            # similarity_search returns List[Document]
            results = self.vector_store.similarity_search(query, k=k, filter=filter)
            
            # Format results to match expected dictionary structure
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "id": doc.metadata.get("id", "") # Chroma might not return ID in metadata by default
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def clear(self):
        """
        Clear the collection.
        """
        try:
            self.vector_store.delete_collection()
            logger.info("✅ Vector store cleared.")
        except Exception as e:
            logger.warning(f"Could not clear vector store: {e}")

