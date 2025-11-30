"""
Orchestrator agent.
"""
from prime_agent.agents.state import AgentState
from loguru import logger
from prime_agent.tools.user_profile import create_session

def orchestrator_node(state: AgentState) -> AgentState:
    """
    Main entry point for the graph.
    Initializes session and determines the plan.
    """
    logger.info(f"Orchestrator started for topic: {state.get('topic')}")
    
    # Initialize session if not present
    if not state.get("session_id"):
        session_id = create_session(state["topic"], state.get("depth", 1))
        state["session_id"] = session_id
        logger.info(f"Created session: {session_id}")
    
    # For now, we enforce a linear flow: Research -> Summarize -> Credibility -> Learning -> KG -> Progress
    # In a more complex agent, this could dynamically choose steps.
    
    return state
