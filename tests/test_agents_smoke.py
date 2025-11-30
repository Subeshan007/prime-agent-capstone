"""
Smoke tests for agents.
"""
from prime_agent.agents.graph_definition import build_graph
import pytest

def test_orchestrator():
    app = build_graph()
    assert app is not None

@pytest.mark.skip(reason="Requires API keys and internet")
def test_end_to_end_flow():
    app = build_graph()
    initial_state = {
        "topic": "Test Topic",
        "depth": 1,
        "urls": [],
        "pdf_files": [],
        "documents": [],
        "summary": "",
        "notes": {},
        "credibility_scores": [],
        "quiz": [],
        "graph_data": {},
        "messages": []
    }
    
    # Run one step or full flow
    # Since it calls LLMs, we might just check if it compiles and starts
    # For a real test, we'd mock the tools.
    pass
