"""
Ollama LLM Provider Implementation
Local LLM provider for on-premises deployment
"""
import requests
from typing import Optional
from .provider import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self, model: str = "llama3.2:1b", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama provider
        
        Args:
            model: Model name (e.g., llama3.2:1b)
            base_url: Ollama server URL
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.0) -> str:
        """Generate text using Ollama"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature,
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama API request failed: {str(e)}")
    
    def validate_health(self) -> bool:
        """Check if Ollama server is responsive"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_model_info(self) -> dict:
        """Get Ollama model information"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            
            models = response.json().get("models", [])
            model_info = next((m for m in models if m["name"] == self.model), None)
            
            if model_info:
                return {
                    "provider": "ollama",
                    "model": self.model,
                    "size": model_info.get("size", "unknown"),
                    "modified": model_info.get("modified_at", "unknown")
                }
            else:
                return {
                    "provider": "ollama",
                    "model": self.model,
                    "status": "not_found"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "provider": "ollama",
                "model": self.model,
                "error": str(e)
            }
