"""
Tool for generating quizzes.
"""
from typing import List, Dict
from prime_agent.llm.client import LLMClient
from prime_agent.config import DEFAULT_MODEL

def generate_quiz(text: str, num_questions: int = 5, difficulty: str = "intermediate") -> List[Dict]:
    """
    Generate a quiz from text.
    Returns list of dicts with question, options, correct_index, explanation.
    """
    client = LLMClient(model_name=DEFAULT_MODEL)
    
    schema = {
        "title": "Quiz",
        "description": "A list of multiple choice questions.",
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "options": {"type": "array", "items": {"type": "string"}, "minItems": 4, "maxItems": 4},
                        "correct_index": {"type": "integer", "description": "Index of the correct option (0-3)"},
                        "explanation": {"type": "string", "description": "Explanation of the correct answer"}
                    },
                    "required": ["question", "options", "correct_index", "explanation"]
                }
            }
        },
        "required": ["questions"]
    }
    
    prompt = f"Generate {num_questions} {difficulty}-level multiple choice questions based on the following text:\n\n{text[:10000]}"
    
    try:
        result = client.generate_structured(prompt, schema)
        
        # Handle case where result is just the list of questions
        if isinstance(result, list):
            return result
            
        return result.get("questions", [])
    except Exception as e:
        import logging
        logging.error(f"Quiz generation failed: {e}")
        return []
