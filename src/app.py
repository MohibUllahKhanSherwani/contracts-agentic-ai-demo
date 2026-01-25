"""
FastAPI Application
REST API for contract evaluation system
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import sys
from pathlib import Path

# Add project root to path to resolve 'src' imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import (
    OrchestratorAgent,
    DataIntakeAgent,
    PerformanceAnalysisAgent,
    RiskAssessmentAgent,
    ReasoningAgent
)
from src.utils import CSVOutputHandler

# Initialize FastAPI app
app = FastAPI(
    title="Daleel Petroleum Contract Evaluation API",
    description="Agentic AI system for automated contract performance evaluation",
    version="0.1.0"
)

# CORS middleware (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents (singleton pattern)
orchestrator = OrchestratorAgent()
data_intake = DataIntakeAgent()
performance = PerformanceAnalysisAgent()
risk = RiskAssessmentAgent()
reasoning_agent = ReasoningAgent()
csv_handler = CSVOutputHandler()

agents = {
    "data_intake": data_intake,
    "performance": performance,
    "risk": risk
}


# Request/Response models
class EvaluationRequest(BaseModel):
    """Contract evaluation request"""
    contract_id: str
    contract_file: Optional[str] = None  # Path to contract JSON
    contract_data: Optional[Dict] = None  # Or direct contract data


class EvaluationResponse(BaseModel):
    """Contract evaluation response"""
    contract_id: str
    vendor_name: str
    status: str
    performance_score: Optional[float] = None
    risk_level: Optional[str] = None
    recommendation: Optional[str] = None
    timestamp: str
    reasoning_chain: Optional[List[str]] = None
    justification: Optional[str] = None
    confidence_level: Optional[str] = None


@app.get("/")
def root():
    """API root endpoint"""
    return {
        "name": "Daleel Petroleum Contract Evaluation API",
        "version": "0.1.0",
        "status": "operational"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": {
            "orchestrator": "operational",
            "data_intake": "operational",
            "performance": "operational",
            "risk": "operational"
        }
    }


@app.post("/evaluate", response_model=EvaluationResponse, status_code=status.HTTP_200_OK)
def evaluate_contract(request: EvaluationRequest):
    """
    Evaluate a contract
    
    Args:
        request: Evaluation request with contract_id and contract data
        
    Returns:
        Evaluation result
    """
    # Load contract data
    if request.contract_data:
        contract = request.contract_data
    elif request.contract_file:
        contract_path = Path(request.contract_file)
        if not contract_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract file not found: {request.contract_file}"
            )
        with open(contract_path, 'r', encoding='utf-8') as f:
            contract = json.load(f)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide either contract_data or contract_file"
        )
    
    # Validate contract_id matches
    if contract.get("contract_id") != request.contract_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract ID mismatch"
        )
    
    # Run evaluation
    try:
        # Standard analytical evaluation
        result = orchestrator.evaluate_contract(contract, agents)
        
        # Deep reasoning evaluation (LLM synthesis across all sources)
        try:
            # Note: This will load additional files (CSV, JSON, TXT, MD) if they exist
            reasoning_result = reasoning_agent.evaluate(request.contract_id)
            
            # Merge reasoning into result
            result["reasoning_chain"] = reasoning_result.get("reasoning_chain", [])
            result["justification"] = reasoning_result.get("justification", "")
            result["confidence_level"] = reasoning_result.get("confidence_level", "LOW")
            
            # Optionally override recommendation and risk if reasoning is high confidence
            # For now, we prefer the reasoning recommendation as it's more "agentic"
            if reasoning_result.get("recommendation"):
                result["recommendation"] = reasoning_result["recommendation"]
        except Exception as reasoning_err:
            print(f"Reasoning evaluation failed (non-critical): {reasoning_err}")

        # Save to CSV
        csv_handler.save_result(result)
        
        # Return response
        return EvaluationResponse(
            contract_id=result["contract_id"],
            vendor_name=result["vendor_name"],
            status=result["status"],
            performance_score=result.get("performance_score"),
            risk_level=result.get("risk_level"),
            recommendation=result.get("recommendation"),
            timestamp=result["timestamp"],
            reasoning_chain=result.get("reasoning_chain"),
            justification=result.get("justification"),
            confidence_level=result.get("confidence_level")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}"
        )


@app.get("/results/{contract_id}")
def get_result(contract_id: str):
    """
    Get evaluation result by contract ID
    
    Args:
        contract_id: Contract ID
        
    Returns:
        Evaluation result from CSV
    """
    result = csv_handler.get_by_contract_id(contract_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No evaluation found for contract {contract_id}"
        )
    
    return result


@app.get("/results")
def list_results():
    """
    List all evaluation results
    
    Returns:
        List of all evaluations
    """
    results = csv_handler.read_results()
    return {
        "count": len(results),
        "results": results
    }


@app.get("/audit-log")
def get_audit_log(limit: int = 50):
    """
    Get audit log entries
    
    Args:
        limit: Maximum number of entries to return
        
    Returns:
        Audit log entries
    """
    audit_trail = orchestrator.get_audit_trail()
    
    # Return most recent entries
    recent = audit_trail[-limit:] if len(audit_trail) > limit else audit_trail
    recent.reverse()  # Most recent first
    
    return {
        "count": len(recent),
        "total": len(audit_trail),
        "entries": recent
    }


@app.post("/evaluate-sample/{sample_name}")
def evaluate_sample(sample_name: str):
    """
    Evaluate a sample contract by name
    
    Args:
        sample_name: Sample name (vendor_abc_it_solutions, vendor_xyz_tech, vendor_problematic_corp)
        
    Returns:
        Evaluation result
    """
    # Map sample names to files
    sample_files = {
        "vendor_abc_it_solutions": "data/samples/vendor_abc_it_solutions.json",
        "vendor_xyz_tech": "data/samples/vendor_xyz_tech.json",
        "vendor_problematic_corp": "data/samples/vendor_problematic_corp.json",
        "abc": "data/samples/vendor_abc_it_solutions.json",
        "xyz": "data/samples/vendor_xyz_tech.json",
        "problematic": "data/samples/vendor_problematic_corp.json"
    }
    
    contract_file = sample_files.get(sample_name.lower())
    
    if not contract_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown sample: {sample_name}. Available: {', '.join(sample_files.keys())}"
        )

    contract_file_path = Path(contract_file)
    
    # Resolve path relative to project root if not found in current directory
    if not contract_file_path.exists():
        root_path = Path(__file__).parent.parent
        contract_file_path = root_path / contract_file
        
    if not contract_file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract file not found: {contract_file_path}"
        )
    
    # Load and evaluate
    with open(contract_file_path, 'r', encoding='utf-8') as f:
        contract = json.load(f)
    
    request = EvaluationRequest(
        contract_id=contract["contract_id"],
        contract_data=contract
    )
    
    return evaluate_contract(request)


if __name__ == "__main__":
    import uvicorn
    print("Starting Daleel Petroleum Contract Evaluation API...")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
