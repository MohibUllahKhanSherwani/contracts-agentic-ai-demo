"""
LLM Provider Abstraction Layer
Allows switching between Ollama and Azure OpenAI with minimal code changes
"""
from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.0) -> str:
        """
        Generate text from prompt
        
        Args:
            prompt: Input prompt text
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 = deterministic)
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def validate_health(self) -> bool:
        """
        Check if LLM is responsive and available
        
        Returns:
            True if healthy, False otherwise
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Get information about the current model
        
        Returns:
            Dictionary with model metadata
        """
        pass
