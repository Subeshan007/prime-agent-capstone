"""
Credibility agent.
"""
from prime_agent.agents.state import AgentState
from prime_agent.tools.credibility import assess_credibility
from prime_agent.storage.vector_store import VectorStore
from loguru import logger
import time # <--- NEW: Import time module for throttling

def credibility_node(state: AgentState) -> AgentState:
    """
    Assess credibility of sources.
    """
    logger.info("Starting credibility assessment...")
    
    # We assess the sources found in the research phase
    documents = state.get("documents", [])
    scores = []
    
    # Deduplicate sources
    unique_sources = {}
    for doc in documents:
        source = doc.get("source")
        if source and source not in unique_sources:
            unique_sources[source] = doc
            
    # Assess each unique source
    vs = VectorStore()
    
    for source, doc_meta in unique_sources.items():
        
        # CRITICAL FIX: Throttle the API call burst
        # If the scores list is not empty, we made at least one call, so we must wait.
        if scores:
            logger.info("Throttling: Waiting 2 seconds before next source assessment...")
            time.sleep(2) 
            
        # Find a chunk from this source
        results = vs.search(source, k=1, filter={"source": source})
        if results:
            text_sample = results[0]["content"]
            
            # This is the call that hits the LLM
            assessment = assess_credibility(text_sample, source) 
            
            assessment["source"] = source
            assessment["title"] = doc_meta.get("title", source)
            scores.append(assessment)
            
    state["credibility_scores"] = scores
    return state