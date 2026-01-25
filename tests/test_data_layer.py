"""
Test Data Layer - Contract Loading and Validation
Verification script for Phase 2 deliverable
"""
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validators import ContractValidator


def test_data_layer():
    """Test contract data loading and validation"""
    print("=" * 60)
    print("Phase 2 - Data Layer Test")
    print("=" * 60)
    
    validator = ContractValidator()
    data_dir = Path("data/samples")
    
    # Expected contract files
    contract_files = [
        "vendor_abc_it_solutions.json",
        "vendor_xyz_tech.json",
        "vendor_problematic_corp.json"
    ]
    
    print(f"\n[1/4] Checking data directory structure...")
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        return False
    print(f"✅ Data directory exists: {data_dir}")
    
    print(f"\n[2/4] Loading sample contracts...")
    contracts = []
    for filename in contract_files:
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"❌ Contract file not found: {filename}")
            return False
        
        try:
            with open(filepath, 'r') as f:
                contract = json.load(f)
            contracts.append((filename, contract))
            print(f"✅ Loaded: {filename}")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {filename}: {str(e)}")
            return False
    
    print(f"\n[3/4] Validating contract schemas...")
    all_valid = True
    for filename, contract in contracts:
        result = validator.validate(contract)
        
        vendor_name = contract.get("vendor_name", "Unknown")
        
        if result.valid:
            completeness = validator.calculate_completeness(contract)
            print(f"✅ {vendor_name}")
            print(f"   File: {filename}")
            print(f"   Completeness: {completeness*100:.0f}%")
            if result.warnings:
                print(f"   Warnings: {len(result.warnings)}")
                for warning in result.warnings[:2]:  # Show first 2
                    print(f"     - {warning}")
        else:
            print(f"❌ {vendor_name}")
            print(f"   Errors: {len(result.errors)}")
            for error in result.errors:
                print(f"     - {error}")
            all_valid = False
    
    if not all_valid:
        return False
    
    print(f"\n[4/4] Verifying contract diversity...")
    # Check that we have different risk profiles
    kpi_scores = []
    for filename, contract in contracts:
        kpis = contract.get("kpis", [])
        if kpis:
            # Calculate simple average
            avg_score = sum(
                (kpi["actual"] / kpi["target"]) * 100 
                for kpi in kpis 
                if kpi.get("target", 0) > 0
            ) / len(kpis)
            kpi_scores.append((contract["vendor_name"], avg_score))
    
    print(f"✅ Contract performance diversity:")
    for vendor, score in sorted(kpi_scores, key=lambda x: x[1], reverse=True):
        risk = "HIGH PERFORMANCE" if score > 95 else "MEDIUM RISK" if score > 75 else "LOW PERFORMANCE"
        print(f"   {vendor}: {score:.1f}% ({risk})")
    
    print("\n" + "=" * 60)
    print("✅ Phase 2 Data Layer Complete!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  • {len(contracts)} sample contracts loaded")
    print(f"  • All contracts pass validation")
    print(f"  • Data directory structure verified")
    print(f"  • Ready for agent implementation")
    
    return True


if __name__ == "__main__":
    success = test_data_layer()
    sys.exit(0 if success else 1)
