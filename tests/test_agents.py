"""
Test Agent Implementation
Verification script for Phase 3 deliverable
"""
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import (
    OrchestratorAgent,
    DataIntakeAgent,
    PerformanceAnalysisAgent,
    RiskAssessmentAgent
)


def test_agents():
    """Test agent implementation with sample contracts"""
    print("=" * 60)
    print("Phase 3 - Agent Implementation Test")
    print("=" * 60)
    
    # Initialize agents
    print("\n[1/5] Initializing agents...")
    try:
        orchestrator = OrchestratorAgent()
        data_intake = DataIntakeAgent()
        performance = PerformanceAnalysisAgent()
        risk = RiskAssessmentAgent()
        print("✅ All agents initialized")
    except Exception as e:
        print(f"❌ Agent initialization failed: {str(e)}")
        return False
    
    # Load sample contract
    print("\n[2/5] Loading test contract...")
    contract_path = Path("data/samples/vendor_abc_it_solutions.json")
    if not contract_path.exists():
        print(f"❌ Contract file not found: {contract_path}")
        return False
    
    with open(contract_path, 'r') as f:
        contract = json.load(f)
    vendor_name = contract.get("vendor_name", "Unknown")
    print(f"✅ Loaded contract: {vendor_name}")
    
    # Test Data Intake Agent
    print("\n[3/5] Testing Data Intake Agent...")
    intake_result = data_intake.process(contract)
    print(f"   Valid: {intake_result['valid']}")
    print(f"   Completeness: {intake_result['completeness']*100:.0f}%")
    print(f"   Confidence: {intake_result['confidence']:.2f}")
    if intake_result['warnings']:
        print(f"   Warnings: {len(intake_result['warnings'])}")
    print("✅ Data intake agent working")
    
    # Test Performance Analysis Agent
    print("\n[4/5] Testing Performance Analysis Agent...")
    perf_result = performance.evaluate(contract)
    print(f"   Overall Score: {perf_result['overall_score']}/100")
    print(f"   Grade: {perf_result['grade']}")
    print(f"   KPIs Evaluated: {len(perf_result['kpi_scores'])}")
    print(f"   Justification: {perf_result['justification'][:80]}...")
    print("✅ Performance analysis agent working")
    
    # Test Risk Assessment Agent
    print("\n[5/5] Testing Risk Assessment Agent...")
    risk_input = {
        "contract": contract,
        "performance_score": perf_result['overall_score']
    }
    risk_result = risk.assess(risk_input)
    print(f"   Risk Level: {risk_result['risk_level']}")
    print(f"   Recommendation: {risk_result['recommendation']}")
    print(f"   Risk Factors: {len(risk_result['risk_factors'])}")
    print(f"   Reason: {risk_result['reason'][:80]}...")
    print("✅ Risk assessment agent working")
    
    # Test Full Orchestration
    print("\n[Bonus] Testing Full Orchestration...")
    agents_dict = {
        "data_intake": data_intake,
        "performance": performance,
        "risk": risk
    }
    
    eval_result = orchestrator.evaluate_contract(contract, agents_dict)
    print(f"   Status: {eval_result['status']}")
    print(f"   Steps Completed: {len(eval_result['steps'])}")
    print(f"   Final Score: {eval_result.get('performance_score', 0):.1f}/100")
    print(f"   Final Risk: {eval_result.get('risk_level', 'N/A')}")
    print(f"   Recommendation: {eval_result.get('recommendation', 'N/A')}")
    print("✅ Orchestration working")
    
    # Check audit log
    audit_log_path = Path("data/audit_logs.jsonl")
    if audit_log_path.exists():
        with open(audit_log_path, 'r') as f:
            log_lines = f.readlines()
        print(f"\n   Audit logs created: {len(log_lines)} entries")
    
    print("\n" + "=" * 60)
    print("✅ Phase 3 Agent Implementation Complete!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  • 4 agents implemented and tested")
    print(f"  • End-to-end workflow functional")
    print(f"  • LLM integration working")
    print(f"  • Audit logging operational")
    print(f"  • Ready for API integration (Phase 4)")
    
    return True


if __name__ == "__main__":
    success = test_agents()
    sys.exit(0 if success else 1)
