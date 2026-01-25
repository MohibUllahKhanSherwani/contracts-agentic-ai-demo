"""
Test LLM Provider Configuration and Health Check
Quick verification script for Phase 1 deliverable
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm import get_llm_provider, get_llm_config


def test_llm_setup():
    """Test LLM provider configuration and connectivity"""
    print("=" * 60)
    print("Phase 1 - LLM Configuration Test")
    print("=" * 60)
    
    # 1. Load configuration
    print("\n[1/4] Loading configuration...")
    try:
        config = get_llm_config()
        print(f"✅ Configuration loaded successfully")
        print(f"    Provider: {config['provider']}")
        print(f"    Temperature: {config['temperature']}")
        print(f"    Max Tokens: {config['max_tokens']}")
    except Exception as e:
        print(f"❌ Configuration failed: {str(e)}")
        return False
    
    # 2. Initialize provider
    print("\n[2/4] Initializing LLM provider...")
    try:
        provider = get_llm_provider()
        print(f"✅ Provider initialized: {provider.__class__.__name__}")
    except Exception as e:
        print(f"❌ Provider initialization failed: {str(e)}")
        return False
    
    # 3. Health check
    print("\n[3/4] Checking provider health...")
    try:
        is_healthy = provider.validate_health()
        if is_healthy:
            print("✅ Provider is healthy and responsive")
        else:
            print("⚠️  Provider is not responding (is Ollama running?)")
            print("    Run: ollama serve")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False
    
    # 4. Get model info
    print("\n[4/4] Retrieving model information...")
    try:
        model_info = provider.get_model_info()
        print("✅ Model information:")
        for key, value in model_info.items():
            print(f"    {key}: {value}")
    except Exception as e:
        print(f"⚠️  Could not retrieve model info: {str(e)}")
    
    # 5. Test generation (simple)
    print("\n[Bonus] Testing text generation...")
    try:
        test_prompt = "Say 'Hello from Ollama' and nothing else."
        response = provider.generate(test_prompt, max_tokens=50, temperature=0.0)
        print(f"✅ Generation test passed")
        print(f"    Prompt: {test_prompt}")
        print(f"    Response: {response[:100]}")
    except Exception as e:
        print(f"⚠️  Generation test failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Phase 1 Setup Complete!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_llm_setup()
    sys.exit(0 if success else 1)
