"""
Summarization agent.
"""
from prime_agent.agents.state import AgentState
from prime_agent.storage.vector_store import VectorStore
from prime_agent.tools.summarizer import generate_learning_content
from loguru import logger
import time

def summarization_node(state: AgentState) -> AgentState:
    logger.info("Starting summarization phase...")
    topic = state["topic"]
    
    vs = VectorStore()
    # INCREASED CONTEXT: Fetch 25 chunks to ensure we get the Lifecycle and Roles tables
    results = vs.search(topic, k=25)
    context = "\n\n".join([r["content"] for r in results])
    
    if not context:
        logger.warning("No context found for summarization.")
        state["notes"] = {"content": "No relevant information found."}
        return state
        
    # --- SINGLE STEP: Generate The Master Study Guide ---
    logger.info("Generating comprehensive Study Guide...")
    
    # We use the new 'study_guide' mode which targets the Lifecycle specifically
    study_guide = generate_learning_content(context, topic, mode="study_guide")
    
    # Store result directly in 'notes'
    state["notes"] = {
        "content": study_guide
    }
    
    # Clear other fields to avoid confusion in UI
    state["summary"] = "" 
    state["mind_map"] = None
    
    return state
