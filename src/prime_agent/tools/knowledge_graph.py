"""
Tool for extracting knowledge graph entities and relations.
"""
from typing import List, Dict
from prime_agent.llm.client import LLMClient
from prime_agent.config import DEFAULT_MODEL

def extract_graph(text: str) -> Dict[str, List]:
    """
    Extract nodes and edges from text.
    Returns dict with 'nodes' and 'edges'.
    """
    client = LLMClient(model_name=DEFAULT_MODEL)
    
    schema = {
        "title": "KnowledgeGraph",
        "description": "Entities and relationships extracted from text.",
        "type": "object",
        "properties": {
            "nodes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "Unique identifier for the entity"},
                        "label": {"type": "string", "description": "Display label"},
                        "type": {"type": "string", "description": "Type of entity (e.g., Person, Concept, Technology)"}
                    },
                    "required": ["id", "label", "type"]
                }
            },
            "edges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "description": "Source node ID"},
                        "target": {"type": "string", "description": "Target node ID"},
                        "relation": {"type": "string", "description": "Relationship type (e.g., CAUSES, IS_A)"}
                    },
                    "required": ["source", "target", "relation"]
                }
            }
        },
        "required": ["nodes", "edges"]
    }
    
    prompt = f"Extract key concepts and relationships from the following text to build a knowledge graph:\n\n{text[:10000]}"
    
    try:
        result = client.generate_structured(prompt, schema)
        if not result or not isinstance(result, dict):
            return {"nodes": [], "edges": []}
        return result
    except Exception as e:
        import logging
        logging.error(f"Graph extraction failed: {e}")
        return {"nodes": [], "edges": []}
