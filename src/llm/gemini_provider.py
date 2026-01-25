"""
Google Gemini API Provider Implementation (using latest google-genai SDK)
"""
from google import genai
from google.genai import types
from .provider import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini API provider using the latest SDK"""
    
    def __init__(self, api_key: str, model: str = "gemini-flash-latest"):
        """
        Initialize Gemini provider
        
        Args:
            api_key: Google AI API key
            model: Model name (strictly gemini-flash-latest)
        """
        self.api_key = api_key
        self.model_name = model
        
        # Initialize the new Google GenAI Client
        self.client = genai.Client(api_key=api_key)
    
    def generate(self, prompt: str, max_tokens: int = 4096, temperature: float = 0.0) -> str:
        """Generate text using Gemini with 429 retry logic"""
        import time
        max_retries = 3
        retry_delay = 20  # Seconds
        
        for attempt in range(max_retries):
            try:
                # Use a dictionary for config to avoid SDK version discrepancies
                config = {
                    "max_output_tokens": max_tokens,
                    "temperature": temperature
                }
                
                # Generate response
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
                
                return response.text
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt < max_retries - 1:
                        print(f"[Gemini] Rate limit hit (429). Retrying in {retry_delay}s (Attempt {attempt + 1}/{max_retries})...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                raise RuntimeError(f"Gemini API (google-genai) request failed: {error_str}")
    
    def validate_health(self) -> bool:
        """Check if Gemini API is accessible"""
        try:
            # Try a simple generation
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Hello"
            )
            return bool(response.text)
        except:
            return False
    
    def get_model_info(self) -> dict:
        """Get Gemini model information"""
        return {
            "provider": "gemini",
            "model": self.model_name,
            "status": "operational"
        }
