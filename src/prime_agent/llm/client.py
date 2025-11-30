import os
import json
import google.generativeai as genai
from loguru import logger
from langchain_core.messages import HumanMessage, SystemMessage
from prime_agent.config import DEFAULT_MODEL

# --- HOTFIX: Inject missing MediaResolution feature ---
try:
    if not hasattr(genai.GenerationConfig, "MediaResolution"):
        class FakeMediaResolution:
            AUTO = "auto"
            LOW = "low"
            MEDIUM = "medium"
            HIGH = "high"
        genai.GenerationConfig.MediaResolution = FakeMediaResolution
except Exception as e:
    logger.warning(f"Hotfix warning: {e}")
# ------------------------------------------------------

from langchain_google_genai import ChatGoogleGenerativeAI

class LLMClient:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        # FIX: Accepted 'model_name' as an argument again to match summarizer.py
        self.model_name = model_name
        
        # Check both possible names for the API key
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            logger.error("❌ NO API KEY FOUND! Check your .env file.")
            raise ValueError("API Key missing. Please set OPENAI_API_KEY in .env")

        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=0.3,
            google_api_key=api_key
        )

    def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """
        Simple text generation wrapper.
        """
        messages = []
import os
import json
import ast
import google.generativeai as genai
from loguru import logger
from langchain_core.messages import HumanMessage, SystemMessage
from prime_agent.config import DEFAULT_MODEL

# --- HOTFIX: Inject missing MediaResolution feature ---
try:
    if not hasattr(genai.GenerationConfig, "MediaResolution"):
        class FakeMediaResolution:
            AUTO = "auto"
            LOW = "low"
            MEDIUM = "medium"
            HIGH = "high"
        genai.GenerationConfig.MediaResolution = FakeMediaResolution
except Exception as e:
    logger.warning(f"Hotfix warning: {e}")
# ------------------------------------------------------

from langchain_google_genai import ChatGoogleGenerativeAI

class LLMClient:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        # FIX: Accepted 'model_name' as an argument again to match summarizer.py
        self.model_name = model_name
        
        # Check both possible names for the API key
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            logger.error("❌ NO API KEY FOUND! Check your .env file.")
            raise ValueError("API Key missing. Please set OPENAI_API_KEY in .env")

        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=0.3,
            google_api_key=api_key
        )

    def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """
        Simple text generation wrapper.
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return "Error generating response."

    def generate_structured(self, prompt: str, schema: dict) -> dict:
        """
        Generates JSON output.
        """
        messages = [
            SystemMessage(content="You are a helpful assistant. Output ONLY valid JSON."),
            HumanMessage(content=f"{prompt}\n\nRespond using this JSON schema:\n{json.dumps(schema, indent=2)}")
        ]
        
        try:
            response = self.llm.invoke(messages)
            content = response.content
            
            if not content:
                logger.error("LLM returned empty content.")
                return {}

            # Handle case where content is a list (e.g. multi-modal response)
            if isinstance(content, list):
                # Join list elements if it's a list
                content = "".join([str(item) for item in content])
            
            cleaned_content = content.strip()
            
            # FIX: Handle case where content is a stringified Python dict (e.g. {'type': 'text', ...})
            if cleaned_content.startswith("{") and "'type':" in cleaned_content:
                try:
                    parsed = ast.literal_eval(cleaned_content)
                    if isinstance(parsed, dict) and "text" in parsed:
                        cleaned_content = parsed["text"]
                except Exception as e:
                    logger.warning(f"Failed to parse stringified dict: {e}")

            # Cleanup Markdown wrappers if present
            cleaned_content = cleaned_content.strip()
            if "```json" in cleaned_content:
                cleaned_content = cleaned_content.split("```json")[1].split("```")[0]
            elif "```" in cleaned_content:
                cleaned_content = cleaned_content.split("```")[1].split("```")[0]
            
            cleaned_content = cleaned_content.strip()
            
            return json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            logger.error(f"LLM structured generation failed: {e}")
            logger.error(f"Raw content: {content}")
            return {}
        except Exception as e:
            logger.error(f"LLM structured generation failed: {e}")
            return {}