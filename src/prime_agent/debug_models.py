import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") # Using the variable name from your setup

if not api_key:
    print("❌ Error: No API Key found in .env variable 'OPENAI_API_KEY'")
    exit()

print(f"🔑 Testing Key: {api_key[:5]}...{api_key[-3:]}")

# Configure the Google library
genai.configure(api_key=api_key)

print("\n📡 Connecting to Google API to list available models...")

try:
    # Ask Google what models are available for this key
    found_any = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ AVAILABLE: {m.name}")
            found_any = True
    
    if not found_any:
        print("⚠️ No models found with 'generateContent' capability.")
        
except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")
    print("Check if your API Key is valid and has 'Generative Language API' enabled in Google Cloud Console.")