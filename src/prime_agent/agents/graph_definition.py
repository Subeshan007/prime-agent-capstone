"""
LangGraph graph definition.
"""
from langgraph.graph import StateGraph, END
from prime_agent.agents.state import AgentState

from prime_agent.agents.orchestrator import orchestrator_node
from prime_agent.agents.research_agent import research_node
from prime_agent.agents.summarization_agent import summarization_node
from prime_agent.agents.credibility_agent import credibility_node
from prime_agent.agents.learning_agent import learning_node
from prime_agent.agents.knowledge_graph_agent import knowledge_graph_node
from prime_agent.agents.progress_agent import progress_node

def build_graph():
    """
    Construct the agent graph.
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("research", research_node)
    workflow.add_node("summarization", summarization_node)
    workflow.add_node("credibility", credibility_node)
    workflow.add_node("learning", learning_node)
    workflow.add_node("knowledge_graph", knowledge_graph_node)
    workflow.add_node("progress", progress_node)
    
    # Define edges (Linear flow for now)
    workflow.set_entry_point("orchestrator")
    
    workflow.add_edge("orchestrator", "research")
    workflow.add_edge("research", "summarization")
    workflow.add_edge("summarization", "credibility")
    workflow.add_edge("credibility", "learning")
    workflow.add_edge("learning", "knowledge_graph")
    workflow.add_edge("knowledge_graph", "progress")
    workflow.add_edge("progress", END)
    
    return workflow.compile()
