"""
Evaluation script for retrieval.
"""
def evaluate_retrieval(query: str, results: list) -> float:
    """
    Evaluate retrieval quality (simple relevance check).
    Returns a score between 0 and 1.
    """
    if not results:
        return 0.0
        
    # Simple keyword match heuristic
    keywords = query.lower().split()
    match_count = 0
    
    for res in results:
        content = res.get("content", "").lower()
        if any(k in content for k in keywords):
            match_count += 1
            
    return match_count / len(results)
