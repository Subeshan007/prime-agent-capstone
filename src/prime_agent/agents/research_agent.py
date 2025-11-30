"""
Research agent.
"""
from prime_agent.agents.state import AgentState
from prime_agent.tools.web_search import web_search
from prime_agent.tools.html_loader import load_html
from prime_agent.tools.pdf_loader import load_pdf
from prime_agent.utils.text_utils import clean_text, chunk_text
from prime_agent.storage.vector_store import VectorStore
from loguru import logger
import uuid

def research_node(state: AgentState) -> AgentState:
    """
    Perform research: Web Search, Load Content, Chunk, Store.
    """
    logger.info("Starting research phase...")
    topic = state["topic"]
    depth = state.get("depth", 1)
    urls = state.get("urls", [])
    pdf_files = state.get("pdf_files", [])
    
    raw_docs = []
    
    # 1. Web Search (if depth > 0)
    if depth > 0:
        logger.info(f"Searching web for: {topic}")
        search_results = web_search(topic, num_results=depth * 3)
        for res in search_results:
            link = res.get("link")
            if link:
                logger.info(f"Fetching: {link}")
                content = load_html(link)
                if content:
                    raw_docs.append({"content": content, "source": link, "title": res.get("title", topic)})
    
    # 2. Process provided URLs
    for url in urls:
        if url:
            logger.info(f"Fetching provided URL: {url}")
            content = load_html(url)
            if content:
                raw_docs.append({"content": content, "source": url, "title": url})
            
    # 3. Process PDFs
    for pdf_path in pdf_files:
        logger.info(f"Processing PDF: {pdf_path}")
        content = load_pdf(pdf_path)
        if content:
            raw_docs.append({"content": content, "source": pdf_path, "title": pdf_path})
            
    # 4. Clean, Chunk, and Store
    vs = VectorStore()
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    processed_docs_metadata = []
    
    for doc in raw_docs:
        cleaned = clean_text(doc["content"])
        chunks = chunk_text(cleaned)
        
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            all_chunks.append(chunk)
            meta = {"source": doc["source"], "title": doc["title"], "chunk_index": i}
            all_metadatas.append(meta)
            all_ids.append(chunk_id)
            
        processed_docs_metadata.append({"source": doc["source"], "title": doc["title"]})
            
    if all_chunks:
        vs.add_documents(all_chunks, all_metadatas, all_ids)
        
    state["documents"] = processed_docs_metadata
    logger.info(f"Research complete. Stored {len(all_chunks)} chunks.")
    
    return state
