import time
import json
import os
import hashlib
import logging
from typing import List

# --- HOTFIX START: Patch missing Google API attributes ---
import google.generativeai as genai
try:
    # If the library is missing 'MediaResolution', we manually create a dummy one
    if not hasattr(genai.GenerationConfig, "MediaResolution"):
        class FakeMediaResolution:
            # Add dummy values to satisfy LangChain's import
            AUTO = "auto"
            LOW = "low"
            MEDIUM = "medium"
            HIGH = "high"
        genai.GenerationConfig.MediaResolution = FakeMediaResolution
except Exception as e:
    print(f"Hotfix warning: {e}")
# --- HOTFIX END ---

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
EMBED_CACHE_PATH = os.path.expanduser("~/.prime_agent_embedding_cache.json")

# Initialize cache file if it doesn't exist
if not os.path.exists(EMBED_CACHE_PATH):
    try:
        with open(EMBED_CACHE_PATH, "w") as f:
            json.dump({}, f)
    except Exception as e:
        logger.warning(f"Failed to create embedding cache at {EMBED_CACHE_PATH}: {e}")

def _cache_load():
    if not os.path.exists(EMBED_CACHE_PATH):
        return {}
    try:
        with open(EMBED_CACHE_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load embedding cache: {e}")
        return {}

def _cache_save(cache):
    try:
        with open(EMBED_CACHE_PATH, "w") as f:
            json.dump(cache, f)
    except Exception as e:
        logger.warning(f"Failed to save embedding cache: {e}")

def _text_key(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def call_embedding_api(texts: List[str]) -> List[List[float]]:
    """
    Calls the Google Generative AI embedding API.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")
    
    # Use the model we verified earlier
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        google_api_key=api_key
    )
    return embeddings.embed_documents(texts)

def embed_texts_with_retry(texts: List[str]) -> List[List[float]]:
    """
    Returns list of embeddings for input texts with proper rate limiting.
    - Uses cache to avoid duplicate embeddings.
    - Implements batching with delays to respect API rate limits.
    - Retries with exponential backoff on 429 errors.
    """
    if not texts:
        return []

    cache = _cache_load()
    results = [None] * len(texts)
    to_request = []
    request_idxs = []

    # Prepare results and list which to request
    for i, t in enumerate(texts):
        k = _text_key(t)
        if k in cache:
            results[i] = cache[k]
        else:
            to_request.append(t)
            request_idxs.append(i)

    logger.info(f"Embedding: {len(texts)-len(to_request)} cached, {len(to_request)} to request")
    
    if to_request:
        # Ultra-safe: Process 1 at a time with longer delays
        BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "1"))
        SLEEP_TIME = float(os.getenv("EMBED_BATCH_SLEEP", "3.0"))
        
        embeddings_response = []
        total_batches = (len(to_request) + BATCH_SIZE - 1) // BATCH_SIZE
        
        for batch_num, i in enumerate(range(0, len(to_request), BATCH_SIZE), 1):
            batch = to_request[i:i+BATCH_SIZE]
            logger.info(f"Processing embedding batch {batch_num}/{total_batches} (size={len(batch)})")
            
            # Retry logic for this specific batch
            max_retries = 3
            for retry_attempt in range(max_retries):
                try:
                    resp = call_embedding_api(batch)
                    if not isinstance(resp, list):
                        raise RuntimeError("Unexpected embedding response type")
                    embeddings_response.extend(resp)
                    break  # Success, move to next batch
                    
                except Exception as e:
                    error_msg = str(e)
                    
                    # Check if it's a rate limit error (429)
                    if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                        if retry_attempt < max_retries - 1:
                            # Exponential backoff for rate limits
                            backoff_time = SLEEP_TIME * (2 ** retry_attempt)
                            logger.warning(f"Rate limit hit. Waiting {backoff_time}s before retry {retry_attempt + 1}/{max_retries}")
                            time.sleep(backoff_time)
                        else:
                            logger.error(f"Failed to embed batch after {max_retries} retries due to rate limits: {e}")
                            raise
                    else:
                        # Non-rate-limit error, log and re-raise
                        logger.error(f"Error embedding batch: {e}")
                        raise
                
            # Pause between batches to respect rate limits
            if batch_num < total_batches:  # Don't sleep after the last batch
                logger.debug(f"Waiting {SLEEP_TIME}s before next batch...")
                time.sleep(SLEEP_TIME)
            
        # store in cache and fill results
        for i, idx in enumerate(request_idxs):
            if i < len(embeddings_response):
                emb = embeddings_response[i]
                k = _text_key(texts[idx])
                cache[k] = emb
                results[idx] = emb
            else:
                logger.error(f"Missing embedding for index {idx}")
                
        _cache_save(cache)
        logger.info(f"Successfully embedded {len(embeddings_response)} new texts")
        
    # Filter out any Nones if something went wrong
    return [r for r in results if r is not None]
