"""
Test Google Gemini Provider
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm import get_llm_provider


def test_gemini():
    """Test Gemini provider"""
    print("=" * 70)
    print("GEMINI PROVIDER TEST")
    print("=" * 70)
    
    # Initialize provider
    print("\n[1/4] Initializing Gemini provider...")
    try:
        llm = get_llm_provider()
        print(f"✅ Provider initialized: {llm.get_model_info()}")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return False
    
    # Health check
    print("\n[2/4] Checking API health...")
    if llm.validate_health():
        print("✅ Gemini API is healthy")
    else:
        print("❌ Gemini API health check failed")
        return False
    
    # Test generation
    print("\n[3/4] Testing text generation...")
    try:
        response = llm.generate(
            prompt="Explain what a contract evaluation system does in one sentence.",
            max_tokens=100,
            temperature=0.3
        )
        print(f"✅ Generated response ({len(response)} chars):")
        print(f"   {response[:200]}..." if len(response) > 200 else f"   {response}")
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False
    
    # Test JSON output
    print("\n[4/4] Testing JSON output...")
    try:
        json_prompt = '''Generate a JSON object with this structure:
{
  "recommendation": "RENEW",
  "confidence": "HIGH",
  "reason": "Performance is excellent"
}

Output only valid JSON, no other text.'''
        
        response = llm.generate(
            prompt=json_prompt,
            max_tokens=200,
            temperature=0.1
        )
        print(f"✅ JSON response:")
        print(f"   {response}")
    except Exception as e:
        print(f"❌ JSON test failed: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = test_gemini()
    sys.exit(0 if success else 1)
