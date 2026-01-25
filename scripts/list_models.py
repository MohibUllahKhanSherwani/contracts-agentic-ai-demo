import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

def list_gemini_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file")
        return

    try:
        client = genai.Client(api_key=api_key)
        print("Available Gemini Models (v1beta):\n")
        print(f"{'Model Name':<40} | {'Supported Methods'}")
        print("-" * 70)
        
        # list_models() returns an iterator of Model objects
        for i, model in enumerate(client.models.list()):
            if i == 0:
                print(f"Debug: Model object attributes: {dir(model)}\n")
            print(f"{model.name:<40}")
            
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    list_gemini_models()
