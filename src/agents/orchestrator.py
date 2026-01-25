"""
Orchestrator Agent
Coordinates agent workflow, manages state, and enforces audit compliance
"""
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class OrchestratorAgent:
    """
    Orchestrates multi-agent workflow for contract evaluation
    Manages routing, state, retry logic, and audit logging
    """
    
    def __init__(self, audit_log_path: str = "data/audit_logs.jsonl", max_retries: int = 3):
        """
        Initialize orchestrator
        
        Args:
            audit_log_path: Path to audit log file
            max_retries: Maximum retry attempts for failed operations
        """
        self.audit_log_path = Path(audit_log_path)
        self.max_retries = max_retries
        self.workflow_state = {}
        
        # Ensure audit log directory exists
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log_action(
        self,
        agent_name: str,
        action: str,
        input_data: Dict,
        output_data: Dict,
        confidence: float = 1.0,
        human_override: bool = False
    ) -> None:
        """
        Log agent action to immutable audit trail
        
        Args:
            agent_name: Name of the agent
            action: Action performed
            input_data: Input data dictionary
            output_data: Output data dictionary
            confidence: Confidence score (0.0-1.0)
            human_override: Whether human overrode the decision
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": agent_name,
            "action": action,
            "input_hash": self._hash_data(input_data),
            "output_hash": self._hash_data(output_data),
            "confidence": round(confidence, 3),
            "human_override": human_override
        }
        
        # Append to JSONL file (append-only, immutable)
        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def _hash_data(self, data: Dict) -> str:
        """Generate SHA256 hash of data for audit trail"""
        data_str = json.dumps(data, sort_keys=True)
        return "sha256:" + hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def handle_escalation(
        self,
        agent_name: str,
        reason: str,
        context: Dict,
        escalation_type: str = "review"
    ) -> Dict:
        """
        Handle agent escalation to human
        
        Args:
            agent_name: Agent requesting escalation
            reason: Reason for escalation
            context: Context data for human review
            escalation_type: Type of escalation (review, clarification, approval)
            
        Returns:
            Escalation record
        """
        escalation = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": agent_name,
            "type": escalation_type,
            "reason": reason,
            "context": context,
            "status": "pending"
        }
        
        # Log escalation
        self.log_action(
            agent_name=agent_name,
            action="escalate_to_human",
            input_data=context,
            output_data=escalation,
            confidence=0.0  # Escalation means low confidence
        )
        
        return escalation
    
    def get_audit_trail(self, contract_id: Optional[str] = None) -> List[Dict]:
        """
        Retrieve audit trail entries
        
        Args:
            contract_id: Optional filter by contract ID
            
        Returns:
            List of audit log entries
        """
        if not self.audit_log_path.exists():
            return []
        
        entries = []
        with open(self.audit_log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    entries.append(entry)
        
        return entries
    
    def evaluate_contract(
        self,
        contract: Dict,
        agents: Dict[str, Any]
    ) -> Dict:
        """
        Orchestrate full contract evaluation workflow
        
        Args:
            contract: Contract data dictionary
            agents: Dictionary of initialized agents
                Expected keys: 'data_intake', 'performance', 'risk'
        
        Returns:
            Evaluation result dictionary
        """
        contract_id = contract.get("contract_id", "unknown")
        vendor_name = contract.get("vendor_name", "unknown")
        
        result = {
            "contract_id": contract_id,
            "vendor_name": vendor_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "in_progress",
            "steps": []
        }
        
        try:
            # Step 1: Data Intake (validate contract)
            data_intake_agent = agents.get("data_intake")
            if data_intake_agent:
                intake_result = data_intake_agent.process(contract)
                result["steps"].append({
                    "agent": "data_intake",
                    "status": "completed",
                    "output": intake_result
                })
                
                # Check if validation failed
                if not intake_result.get("valid", True):
                    result["status"] = "failed"
                    result["error"] = "Data validation failed"
                    return result
            
            # Step 2: Performance Analysis
            performance_agent = agents.get("performance")
            if performance_agent:
                performance_result = performance_agent.evaluate(contract)
                result["steps"].append({
                    "agent": "performance_analysis",
                    "status": "completed",
                    "output": performance_result
                })
                result["performance_score"] = performance_result.get("overall_score", 0)
            
            # Step 3: Risk Assessment
            risk_agent = agents.get("risk")
            if risk_agent:
                # Pass performance results to risk agent
                risk_input = {
                    "contract": contract,
                    "performance_score": result.get("performance_score", 0)
                }
                risk_result = risk_agent.assess(risk_input)
                result["steps"].append({
                    "agent": "risk_assessment",
                    "status": "completed",
                    "output": risk_result
                })
                result["risk_level"] = risk_result.get("risk_level", "UNKNOWN")
                result["recommendation"] = risk_result.get("recommendation", "REVIEW")
            
            result["status"] = "completed"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            
            # Log error
            self.log_action(
                agent_name="orchestrator",
                action="evaluate_contract_error",
                input_data={"contract_id": contract_id},
                output_data={"error": str(e)},
                confidence=0.0
            )
        
        # Log final result
        self.log_action(
            agent_name="orchestrator",
            action="evaluate_contract",
            input_data={"contract_id": contract_id, "vendor_name": vendor_name},
            output_data=result,
            confidence=1.0 if result["status"] == "completed" else 0.5
        )
        
        return result
