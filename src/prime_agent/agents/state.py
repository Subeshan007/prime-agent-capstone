"""
Data models for agent state.
"""
from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage
import operator
from typing import Annotated

class AgentState(TypedDict):
    """
    Shared state for the agent graph.
    """
    # Input
    topic: str
    depth: int
    urls: List[str]
    pdf_files: List[str]
    
    # Session
    session_id: str
    
    # Research Data
    documents: List[Dict]  # List of chunks/docs
    
    # Outputs
    summary: str
    notes: Dict
    credibility_scores: List[Dict]
    quiz: List[Dict]
    graph_data: Dict
    
    # Flow Control
    next_step: str
    
    # Chat History (if needed for conversational flow)
    messages: Annotated[List[BaseMessage], operator.add]
