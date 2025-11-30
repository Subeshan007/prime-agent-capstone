"""
Tool for generating Mermaid.js mind maps.
"""
from prime_agent.llm.client import LLMClient
from prime_agent.config import DEFAULT_MODEL

def generate_mind_map(text: str) -> str:
    """
    Generate a Mermaid.js mind map from the text.
    Returns the Mermaid code string.
    """
    client = LLMClient(model_name=DEFAULT_MODEL)
    
    prompt = f"""Generate a hierarchical mind map of these concepts using Mermaid.js syntax. 
Focus on how X connects to Y.
Use the 'mindmap' diagram type if appropriate, or 'graph TD' / 'graph LR' for concept maps.
Ensure the code is valid Mermaid syntax.
Do not include markdown code blocks (```mermaid), just the raw code.

Text to visualize:
{text[:10000]}"""
    
    try:
        result = client.generate_text(prompt, system_prompt="You are an expert in data visualization and Mermaid.js syntax.")
        
        # Cleanup Markdown wrappers if present
        cleaned_result = result.strip()
        if "```mermaid" in cleaned_result:
            cleaned_result = cleaned_result.split("```mermaid")[1].split("```")[0]
        elif "```" in cleaned_result:
            cleaned_result = cleaned_result.split("```")[1].split("```")[0]
            
        return cleaned_result.strip()
    except Exception as e:
        import logging
        logging.error(f"Mind map generation failed: {e}")
        return ""
