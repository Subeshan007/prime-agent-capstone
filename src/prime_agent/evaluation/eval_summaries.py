"""
Evaluation script for summaries.
"""
from prime_agent.llm.client import LLMClient
from prime_agent.config import DEFAULT_MODEL

def evaluate_summary(summary: str, reference: str = None) -> float:
    """
    Evaluate summary quality using LLM.
    Returns a score between 0 and 10.
    """
    client = LLMClient(model_name=DEFAULT_MODEL)
    
    prompt = f"""
    Rate the following summary on a scale of 1-10 based on clarity, conciseness, and coverage of key points.
    
    Summary:
    {summary}
    
    Return ONLY the numeric score.
    """
    
    try:
        score_str = client.generate_text(prompt)
        score = float(score_str.strip())
        return score
    except:
        return 0.0
