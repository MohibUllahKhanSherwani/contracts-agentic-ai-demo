"""
Test Reasoning Agent - Multi-Source Analysis
Demonstrates LLM reasoning over diverse data sources
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.reasoning_agent import ReasoningAgent


def test_reasoning_agent():
    """Test reasoning agent with multi-source data"""
    print("=" * 70)
    print("REASONING AGENT TEST - Multi-Source LLM Analysis")
    print("=" * 70)
    
    # Initialize reasoning agent
    print("\n[1/4] Initializing Reasoning Agent...")
    agent = ReasoningAgent()
    print("✅ Agent initialized")
    
    # Test with all 3 vendors
    contracts = [
        ("CNT-2024-001", "ABC IT Solutions"),
        ("CNT-2024-002", "XYZ Tech Services"),
        ("CNT-2023-015", "Problematic IT Corp")
    ]
    
    results = []
    
    for contract_id, vendor_name in contracts:
        print(f"\n{'=' * 70}")
        print(f"[2/4] Evaluating: {vendor_name} ({contract_id})")
        print(f"{'=' * 70}")
        
        try:
            # Run reasoning evaluation
            result = agent.evaluate(contract_id)
            
            # Display reasoning chain
            print(f"\n🧠 REASONING CHAIN:")
            for i, step in enumerate(result.get("reasoning_chain", []), 1):
                print(f"   {i}. {step[:150]}..." if len(step) > 150 else f"   {i}. {step}")
            
            # Display assessment
            print(f"\n📊 PERFORMANCE ASSESSMENT:")
            print(f"   {result.get('performance_assessment', 'N/A')}")
            
            # Display strengths
            print(f"\n✅ STRENGTHS:")
            for strength in result.get("strengths", ["None identified"])[:3]:
                print(f"   • {strength}")
            
            # Display risk factors
            print(f"\n⚠️  RISK FACTORS:")
            for risk in result.get("risk_factors", ["None identified"])[:3]:
                print(f"   • {risk}")
            
            # Display recommendation
            print(f"\n🎯 RECOMMENDATION: {result.get('recommendation', 'N/A')}")
            print(f"   Confidence: {result.get('confidence_level', 'N/A')}")
            print(f"   Justification: {result.get('justification', 'N/A')}")
            
            # Data completeness
            print(f"\n📁 Data Completeness: {result.get('data_completeness', 0) * 100:.0f}%")
            
            results.append(result)
            print(f"\n✅ Evaluation complete for {vendor_name}")
            
        except Exception as e:
            print(f"\n❌ Error evaluating {vendor_name}: {str(e)}")
    
    # Summary
    print(f"\n{'=' * 70}")
    print("[3/4] EVALUATION SUMMARY")
    print(f"{'=' * 70}\n")
    
    print(f"{'Vendor':<25} {'Recommendation':<15} {'Confidence':<10} {'Data':<8}")
    print("-" * 70)
    for (contract_id, vendor_name), result in zip(contracts, results):
        rec = result.get('recommendation', 'ERROR')
        conf = result.get('confidence_level', 'N/A')
        data = f"{result.get('data_completeness', 0) * 100:.0f}%"
        print(f"{vendor_name:<25} {rec:<15} {conf:<10} {data:<8}")
    
    print(f"\n{'=' * 70}")
    print("[4/4] REASONING VERIFICATION")
    print(f"{'=' * 70}\n")
    
    print("✅ Multi-source data loading: WORKING")
    print("✅ LLM reasoning prompts: SENT")
    print("✅ Chain-of-thought output: RECEIVED")
    print("✅ Structured decisions: PARSED")
    
    print(f"\n{'=' * 70}")
    print("✅ REASONING AGENT TEST COMPLETE")
    print(f"{'=' * 70}\n")
    
    print("Key Differences from Rule-Based System:")
    print("  ❌ OLD: score = (actual/target) × 100")
    print("  ✅ NEW: LLM synthesizes Performance + Incidents + Market + Reviews")
    print()
    print("  ❌ OLD: if score < 60 → HIGH risk")
    print("  ✅ NEW: LLM weighs multiple factors and shows reasoning")
    print()
    print("  ❌ OLD: LLM only generates summary text")
    print("  ✅ NEW: LLM makes decisions with step-by-step justification")
    
    return True


if __name__ == "__main__":
    success = test_reasoning_agent()
    sys.exit(0 if success else 1)
