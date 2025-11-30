"""
Progress agent.
"""
from prime_agent.agents.state import AgentState
from prime_agent.tools.user_profile import update_summary
from loguru import logger

def progress_node(state: AgentState) -> AgentState:
    """
    Track progress: Update session summary in DB.
    """
    logger.info("Updating progress...")
    session_id = state.get("session_id")
    summary = state.get("summary")
    
    if session_id and summary:
        update_summary(session_id, summary)
        
    return state
