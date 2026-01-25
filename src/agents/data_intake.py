"""
Data Intake Agent
Loads and validates contract data
"""
import json
from pathlib import Path
from typing import Dict, Optional
from src.validators import ContractValidator


class DataIntakeAgent:
    """
    Validates contract data and flags issues for human review
    """
    
    def __init__(self, confidence_threshold: float = 0.7):
        """
        Initialize data intake agent
        
        Args:
            confidence_threshold: Minimum confidence to proceed (0.0-1.0)
        """
        self.validator = ContractValidator()
        self.confidence_threshold = confidence_threshold
    
    def load_contract(self, filepath: str) -> Dict:
        """
        Load contract from JSON file
        
        Args:
            filepath: Path to contract JSON file
            
        Returns:
            Contract dictionary
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def process(self, contract: Dict) -> Dict:
        """
        Process and validate contract data
        
        Args:
            contract: Contract dictionary
            
        Returns:
            Processing result with validation status
        """
        # Validate contract
        validation_result = self.validator.validate(contract)
        completeness = self.validator.calculate_completeness(contract)
        
        # Calculate confidence based on validation and completeness
        confidence = completeness if validation_result.valid else 0.3
        
        # Determine if we should escalate
        should_escalate = (
            not validation_result.valid or
            confidence < self.confidence_threshold or
            validation_result.error_count > 3
        )
        
        result = {
            "contract_id": contract.get("contract_id", "unknown"),
            "vendor_name": contract.get("vendor_name", "unknown"),
            "valid": validation_result.valid,
            "completeness": completeness,
            "confidence": confidence,
            "errors": validation_result.errors,
            "warnings": validation_result.warnings,
            "should_escalate": should_escalate,
            "escalation_reason": None
        }
        
        # Set escalation reason if needed
        if should_escalate:
            reasons = []
            if not validation_result.valid:
                reasons.append(f"Validation failed with {validation_result.error_count} errors")
            if completeness < self.confidence_threshold:
                reasons.append(f"Low data completeness ({completeness*100:.0f}%)")
            if validation_result.error_count > 3:
                reasons.append("Too many validation errors")
            
            result["escalation_reason"] = "; ".join(reasons)
        
        return result
