"""
Tool for loading and extracting text from HTML.
"""
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def load_html(url: str) -> str | None:
    """
    Fetches and parses text from a URL. Returns None if the request fails.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "DNT": "1",
    }
    
    try:
        # 1. Attempt the request
        response = requests.get(url, headers=headers, timeout=10)
        
        # 2. Check for HTTP errors (like 403 Forbidden or 404 Not Found)
        response.raise_for_status() 

        # 3. Parse the content if successful
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        return soup.get_text(separator=' ', strip=True)

    except requests.exceptions.RequestException as e:
        # 4. Gracefully handle failure
        logger.warning(f"Skipping {url} due to error: {e}")
        return None
