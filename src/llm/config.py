"""
LLM Configuration and Provider Factory
Handles provider selection based on configuration
"""
import os
import yaml
from typing import Optional
from dotenv import load_dotenv
from .provider import LLMProvider
from .ollama_provider import OllamaProvider
from .azure_provider import AzureOpenAIProvider
from .gemini_provider import GeminiProvider


from pathlib import Path

# Load environment variables
load_dotenv()


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file"""
    target_path = Path(config_path)
    
    # If the file isn't found in current directory, try project root
    if not target_path.exists():
        # This assumes src/llm/config.py is 2 levels deep from root
        root_path = Path(__file__).parent.parent.parent
        target_path = root_path / config_path
        
    try:
        with open(target_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file not found: {target_path} (CWD: {os.getcwd()})")
    except yaml.YAMLError as e:
        raise RuntimeError(f"Invalid YAML configuration: {str(e)}")


def get_llm_provider(config_path: str = "config.yaml") -> LLMProvider:
    """
    Factory function to get LLM provider based on configuration
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configured LLM provider instance
    """
    config = load_config(config_path)
    llm_config = config.get("llm", {})
    provider_name = llm_config.get("provider", "ollama").lower()
    
    if provider_name == "ollama":
        ollama_config = llm_config.get("ollama", {})
        return OllamaProvider(
            model=os.getenv("OLLAMA_MODEL", ollama_config.get("model", "llama3.2:1b")),
            base_url=os.getenv("OLLAMA_BASE_URL", ollama_config.get("base_url", "http://localhost:11434"))
        )
    
    elif provider_name == "azure":
        azure_config = llm_config.get("azure", {})
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", azure_config.get("endpoint", ""))
        api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", azure_config.get("deployment", ""))
        
        if not all([endpoint, api_key, deployment]):
            raise ValueError(
                "Azure OpenAI requires AZURE_OPENAI_ENDPOINT, "
                "AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT"
            )
        
        return AzureOpenAIProvider(
            endpoint=endpoint,
            api_key=api_key,
            deployment=deployment
        )
    
    elif provider_name == "gemini":
        gemini_config = llm_config.get("gemini", {})
        api_key = os.getenv("GEMINI_API_KEY", gemini_config.get("api_key", ""))
        
        if not api_key:
            raise ValueError(
                "Gemini requires GEMINI_API_KEY environment variable or "
                "api_key in config.yaml"
            )
        
        return GeminiProvider(
            api_key=api_key,
            model=gemini_config.get("model", "gemini-1.5-flash")
        )
    
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}. Use 'ollama', 'azure', or 'gemini'.")


def get_llm_config(config_path: str = "config.yaml") -> dict:
    """Get LLM-specific configuration settings"""
    config = load_config(config_path)
    llm_config = config.get("llm", {})
    provider_name = llm_config.get("provider", "ollama")
    provider_config = llm_config.get(provider_name, {})
    
    return {
        "provider": provider_name,
        "temperature": provider_config.get("temperature", 0.0),
        "max_tokens": provider_config.get("max_tokens", 512)
    }
