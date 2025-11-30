"""
Tool for assessing source credibility.
"""
from typing import Dict
from prime_agent.llm.client import LLMClient
from prime_agent.config import DEFAULT_MODEL

def assess_credibility(text: str, source: str) -> Dict:
    """
    Assess the credibility of a source.
    Returns dict with score (0-1), label, bias, explanation.
    """
    client = LLMClient(model_name=DEFAULT_MODEL)
    
    schema = {
        "title": "CredibilityAssessment",
        "description": "Assessment of source credibility and bias.",
        "type": "object",
        "properties": {
            "score": {"type": "number", "description": "Credibility score between 0.0 and 1.0"},
            "label": {"type": "string", "enum": ["High", "Medium", "Low"], "description": "Credibility label"},
            "bias": {"type": "string", "description": "Potential bias (e.g., Commercial, Political, Neutral)"},
            "explanation": {"type": "string", "description": "Brief explanation for the rating"}
        },
        "required": ["score", "label", "bias", "explanation"]
    }
    
    prompt = f"Assess the credibility and bias of the following text from source '{source}':\n\n{text[:2000]}"
    
    return client.generate_structured(prompt, schema)
