"""
Contract Validation Module
Validates contract data against JSON schema and business rules
"""
import json
from typing import Dict, List, Tuple
from datetime import datetime
from jsonschema import validate, ValidationError, Draft7Validator


# JSON Schema for contract structure
CONTRACT_SCHEMA = {
    "type": "object",
    "required": [
        "contract_id",
        "vendor_name",
        "vendor_id",
        "start_date",
        "end_date",
        "value_usd",
        "department",
        "kpis"
    ],
    "properties": {
        "contract_id": {
            "type": "string",
            "pattern": "^CNT-[0-9]{4}-[0-9]{3}$"
        },
        "vendor_name": {
            "type": "string",
            "minLength": 1
        },
        "vendor_id": {
            "type": "string",
            "pattern": "^VEN-[0-9]{3}$"
        },
        "start_date": {
            "type": "string",
            "format": "date"
        },
        "end_date": {
            "type": "string",
            "format": "date"
        },
        "value_usd": {
            "type": "number",
            "minimum": 0
        },
        "department": {
            "type": "string"
        },
        "contract_type": {
            "type": "string"
        },
        "kpis": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["name", "target", "actual", "unit"],
                "properties": {
                    "name": {"type": "string"},
                    "target": {"type": "number"},
                    "actual": {"type": "number"},
                    "unit": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        },
        "incidents": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "date", "severity", "description", "resolved"],
                "properties": {
                    "id": {"type": "string"},
                    "date": {"type": "string", "format": "date"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                    "description": {"type": "string"},
                    "resolved": {"type": "boolean"},
                    "resolution_time_hours": {"type": ["number", "null"]}
                }
            }
        },
        "budget": {
            "type": "object",
            "required": ["allocated", "spent", "overrun_percentage"],
            "properties": {
                "allocated": {"type": "number", "minimum": 0},
                "spent": {"type": "number", "minimum": 0},
                "overrun_percentage": {"type": "number"}
            }
        },
        "notes": {
            "type": "string"
        }
    }
}


class ValidationResult:
    """Container for validation results"""
    
    def __init__(self, valid: bool = True, errors: List[str] = None, warnings: List[str] = None):
        self.valid = valid
        self.errors = errors or []
        self.warnings = warnings or []
        self.error_count = len(self.errors)
        self.warning_count = len(self.warnings)
        self.has_critical_error = any("critical" in e.lower() for e in self.errors)
    
    def __bool__(self):
        return self.valid
    
    def __repr__(self):
        return f"ValidationResult(valid={self.valid}, errors={self.error_count}, warnings={self.warning_count})"


class ContractValidator:
    """Validates contract data against schema and business rules"""
    
    REQUIRED_FIELDS = [
        "contract_id",
        "vendor_name",
        "vendor_id",
        "start_date",
        "end_date",
        "value_usd",
        "kpis"
    ]
    
    def __init__(self):
        self.validator = Draft7Validator(CONTRACT_SCHEMA)
    
    def validate(self, contract_data: Dict) -> ValidationResult:
        """
        Validate contract data
        
        Args:
            contract_data: Contract dictionary
            
        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []
        
        # 1. Schema validation
        schema_errors = self._validate_schema(contract_data)
        errors.extend(schema_errors)
        
        # 2. Business rule validation (only if schema is valid)
        if not schema_errors:
            business_errors, business_warnings = self._validate_business_rules(contract_data)
            errors.extend(business_errors)
            warnings.extend(business_warnings)
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_schema(self, contract_data: Dict) -> List[str]:
        """Validate against JSON schema"""
        errors = []
        
        # Check required fields first
        missing = [f for f in self.REQUIRED_FIELDS if f not in contract_data]
        if missing:
            errors.append(f"Missing required fields: {', '.join(missing)}")
            return errors  # Can't continue without required fields
        
        # Validate against schema
        for error in self.validator.iter_errors(contract_data):
            errors.append(f"Schema error at {'.'.join(str(p) for p in error.path)}: {error.message}")
        
        return errors
    
    def _validate_business_rules(self, contract_data: Dict) -> Tuple[List[str], List[str]]:
        """Validate business logic rules"""
        errors = []
        warnings = []
        
        # Date logic validation
        try:
            start_date = datetime.fromisoformat(contract_data["start_date"])
            end_date = datetime.fromisoformat(contract_data["end_date"])
            
            if end_date <= start_date:
                errors.append("End date must be after start date")
            
            # Contract duration check
            duration_days = (end_date - start_date).days
            if duration_days > 1825:  # 5 years
                warnings.append(f"Contract duration ({duration_days} days) exceeds 5 years")
                
        except ValueError as e:
            errors.append(f"Invalid date format: {str(e)}")
        
        # Value validation
        value = contract_data.get("value_usd", 0)
        if value < 0:
            errors.append("Contract value cannot be negative")
        elif value == 0:
            warnings.append("Contract value is zero")
        elif value > 10000000:  # 10 million
            warnings.append(f"High contract value: ${value:,.0f}")
        
        # KPI validation
        kpis = contract_data.get("kpis", [])
        if len(kpis) == 0:
            errors.append("Contract must have at least one KPI")
        
        for i, kpi in enumerate(kpis):
            if kpi.get("target", 0) < 0 or kpi.get("actual", 0) < 0:
                errors.append(f"KPI '{kpi.get('name')}' has negative values")
        
        # Budget validation
        if "budget" in contract_data:
            budget = contract_data["budget"]
            allocated = budget.get("allocated", 0)
            spent = budget.get("spent", 0)
            
            if spent > allocated:
                overrun = ((spent - allocated) / allocated) * 100
                warnings.append(f"Budget overrun: {overrun:.1f}%")
        
        # Incident validation
        incidents = contract_data.get("incidents", [])
        critical_count = sum(1 for inc in incidents if inc.get("severity") == "critical")
        if critical_count > 2:
            warnings.append(f"High number of critical incidents: {critical_count}")
        
        unresolved = sum(1 for inc in incidents if not inc.get("resolved", True))
        if unresolved > 0:
            warnings.append(f"Unresolved incidents: {unresolved}")
        
        return errors, warnings
    
    def calculate_completeness(self, contract_data: Dict) -> float:
        """
        Calculate data completeness score (0.0 to 1.0)
        
        Args:
            contract_data: Contract dictionary
            
        Returns:
            Completeness score
        """
        total_fields = len(CONTRACT_SCHEMA["properties"])
        present_fields = sum(1 for field in CONTRACT_SCHEMA["properties"] if field in contract_data)
        
        return present_fields / total_fields if total_fields > 0 else 0.0
