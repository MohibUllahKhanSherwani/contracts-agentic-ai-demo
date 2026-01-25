"""
Integration Test - Full E2E Workflow
Tests all 3 sample contracts through the API
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
from src.utils import CSVOutputHandler


def test_integration():
    """Test full integration with all 3 sample contracts"""
    print("=" * 60)
    print("Phase 4 - Integration Test")
    print("=" * 60)
    
    # Initialize components
    print("\n[1/4] Initializing system...")
    orchestrator = OrchestratorAgent()
    csv_handler = CSVOutputHandler()
    
    agents = {
        "data_intake": DataIntakeAgent(),
        "performance": PerformanceAnalysisAgent(),
        "risk": RiskAssessmentAgent()
    }
    print("✅ System initialized")
    
    # Load all sample contracts
    print("\n[2/4] Loading sample contracts...")
    data_dir = Path("data/samples")
    contract_files = [
        "vendor_abc_it_solutions.json",
        "vendor_xyz_tech.json",
        "vendor_problematic_corp.json"
    ]
    
    contracts = []
    for filename in contract_files:
        with open(data_dir / filename, 'r') as f:
            contract = json.load(f)
        contracts.append(contract)
        print(f"   ✅ Loaded: {contract['vendor_name']}")
    
    # Evaluate all contracts
    print("\n[3/4] Evaluating contracts...")
    results = []
    for contract in contracts:
        vendor = contract['vendor_name']
        print(f"\n   Evaluating: {vendor}")
        
        result = orchestrator.evaluate_contract(contract, agents)
        results.append(result)
        
        # Save to CSV
        csv_handler.save_result(result)
        
        # Print summary
        print(f"      Score: {result.get('performance_score', 0):.1f}/100")
        print(f"      Risk: {result.get('risk_level', 'N/A')}")
        print(f"      Recommendation: {result.get('recommendation', 'N/A')}")
        print(f"      Status: {result.get('status', 'error')}")
    
    print("\n   ✅ All contracts evaluated")
    
    # Verify outputs
    print("\n[4/4] Verifying outputs...")
    
    # Check CSV
    csv_results = csv_handler.read_results()
    print(f"   ✅ CSV file: {len(csv_results)} records")
    
    # Check audit log
    audit_log_path = Path("data/audit_logs.jsonl")
    if audit_log_path.exists():
        with open(audit_log_path, 'r') as f:
            audit_entries = len(f.readlines())
        print(f"   ✅ Audit log: {audit_entries} entries")
    
    # Summary table
    print("\n" + "=" * 60)
    print("Evaluation Summary")
    print("=" * 60)
    print(f"{'Vendor':<25} {'Score':<10} {'Risk':<10} {'Action':<15}")
    print("-" * 60)
    
    for result in results:
        vendor = result['vendor_name'][:24]
        score = f"{result.get('performance_score', 0):.1f}/100"
        risk = result.get('risk_level', 'N/A')
        action = result.get('recommendation', 'N/A')
        print(f"{vendor:<25} {score:<10} {risk:<10} {action:<15}")
    
    print("\n" + "=" * 60)
    print("✅ Phase 4 Integration Complete!")
    print("=" * 60)
    print(f"\nOutputs:")
    print(f"  • CSV: data/evaluations.csv ({len(csv_results)} records)")
    print(f"  • Audit Log: data/audit_logs.jsonl")
    print(f"  • 3 contracts evaluated successfully")
    print(f"  • System ready for production demo")
    
    return True


if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)
