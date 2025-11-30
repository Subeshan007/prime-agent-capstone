"""
Knowledge Graph agent.
"""
from prime_agent.agents.state import AgentState
from prime_agent.tools.knowledge_graph import extract_graph
from prime_agent.storage.db import Database
from loguru import logger
import uuid

def knowledge_graph_node(state: AgentState) -> AgentState:
    """
    Build knowledge graph and store in DB.
    """
    logger.info("Starting knowledge graph extraction...")
    
    # Handle notes structure which might be a dict of sections or a string
    notes_content = ""
    notes = state.get("notes", {})
    if isinstance(notes, str):
        notes_content = notes
    elif isinstance(notes, dict):
        # Join all values if it's a dict of sections
        notes_content = "\n\n".join([str(v) for v in notes.values()])
    
    context = state.get("summary", "") + "\n\n" + notes_content
    
    if context:
        # Extract Knowledge Graph
        graph_data = extract_graph(context)
        state["graph_data"] = graph_data
        
        # Store in SQLite
        db = Database()
        
        for node in graph_data.get("nodes", []):
            try:
                # Check if exists (simple upsert logic or ignore)
                db.execute(
                    "INSERT OR IGNORE INTO nodes (id, label, type, metadata) VALUES (?, ?, ?, ?)",
                    (node["id"], node["label"], node["type"], "")
                )
            except Exception as e:
                logger.warning(f"Failed to insert node {node}: {e}")
                
        for edge in graph_data.get("edges", []):
            try:
                edge_id = str(uuid.uuid4())
                db.execute(
                    "INSERT INTO edges (id, source_id, target_id, relation, metadata) VALUES (?, ?, ?, ?, ?)",
                    (edge_id, edge["source"], edge["target"], edge["relation"], "")
                )
            except Exception as e:
                logger.warning(f"Failed to insert edge {edge}: {e}")
                
    else:
        state["graph_data"] = {"nodes": [], "edges": []}
        
    return state
