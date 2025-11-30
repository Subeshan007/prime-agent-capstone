"""
Evaluation script for quizzes.
"""
def evaluate_quiz(quiz: list) -> float:
    """
    Evaluate quiz quality (structural validity).
    Returns a score between 0 and 1.
    """
    if not quiz:
        return 0.0
        
    valid_count = 0
    for q in quiz:
        if "question" in q and "options" in q and "correct_index" in q and "explanation" in q:
            if len(q["options"]) >= 2 and 0 <= q["correct_index"] < len(q["options"]):
                valid_count += 1
                
    return valid_count / len(quiz)
