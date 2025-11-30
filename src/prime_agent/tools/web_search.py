"""
Tool for web search.
"""
from typing import List, Dict
from ddgs import DDGS
from loguru import logger

def web_search(query: str, num_results: int = 5) -> List[Dict]:
    """
    Perform a web search using DuckDuckGo.
    Returns a list of dicts with 'title', 'link', 'snippet'.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
        
        # DDGS returns list of dicts: {'title': ..., 'href': ..., 'body': ...}
        # We map 'href' to 'link' and 'body' to 'snippet' to match expected format
        formatted_results = []
        if results:
            for r in results:
                formatted_results.append({
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
        return formatted_results
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return []
