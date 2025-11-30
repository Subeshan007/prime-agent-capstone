import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def list_and_log_models():
    """
    Lists available Gemini models and logs them.
    Sets DEFAULT_MODEL env var if not set.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment.")
        return

    try:
        genai.configure(api_key=api_key)
        
        # Safely extract model names, catching errors during iteration
        names = []
        try:
            models = genai.list_models()
            for m in models:
                try:
                    if 'generateContent' in m.supported_generation_methods:
                        names.append(m.name)
                except (TypeError, AttributeError) as e:
                    # Skip models that have incompatible parameters (e.g., 'thinking')
                    logger.debug(f"Skipping model due to error: {e}")
                    continue
        except TypeError as e:
            # If the models iterator itself fails, log and continue with empty list
            logger.warning(f"Could not iterate models (API may have new unsupported fields): {e}")
            # Set a sensible default
            names = ["models/gemini-1.5-pro", "models/gemini-1.5-flash"]
        
        if names:
            logger.info(f"Available models: {', '.join(names)}")
            # Save the first model to env fallback if needed
            if "DEFAULT_MODEL" not in os.environ:
                # Prefer a flash model if available, else just the first one
                flash_models = [n for n in names if 'flash' in n]
                default = flash_models[0] if flash_models else names[0]
                os.environ["DEFAULT_MODEL"] = default
                logger.info(f"Set DEFAULT_MODEL to {default}")
        else:
            logger.warning("No models found with generateContent capability.")
            
    except Exception as e:
        logger.error(f"Failed listing models: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    list_and_log_models()
