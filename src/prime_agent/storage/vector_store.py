import logging
from typing import List, Dict, Optional
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.config import Settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        logger.info("🟦 Starting Chroma in EPHEMERAL in-memory mode (Streamlit Cloud compatible)")

        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # ❗IMPORTANT: No persist directory, no custom settings
        self.vector_store = Chroma(
            collection_name="prime_docs",
            embedding_function=self.embeddings,
            client_settings=Settings()  # <- DEFAULT only (fixes ValidationError)
        )

    def add_documents(self, documents: List[str], metadata: List[Dict], ids: List[str]):
        batch_size = 32
        for i in range(0, len(documents), batch_size):
            try:
                self.vector_store.add_texts(
                    texts=documents[i:i + batch_size],
                    metadatas=metadata[i:i + batch_size],
                    ids=ids[i:i + batch_size]
                )
            except Exception as e:
                logger.error(f"Error embedding batch: {e}")

    def search(self, query: str, k: int = 5, filter: Optional[Dict] = None):
        try:
            results = self.vector_store.similarity_search(query, k=k, filter=filter)
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "id": doc.metadata.get("id", "")
                }
                for doc in results
            ]
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    def clear(self):
        try:
            self.vector_store.delete_collection()
        except Exception:
            pass
