"""
Risk Assessment Agent
Classifies vendor risk and recommends contract actions
"""
from typing import Dict
from src.llm import get_llm_provider, get_llm_config


class RiskAssessmentAgent:
    """
    Assesses vendor risk based on performance, incidents, and budget
    Provides actionable recommendations
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize risk assessment agent
        
        Args:
            config_path: Path to configuration file
        """
        self.llm_provider = get_llm_provider(config_path)
        self.llm_config = get_llm_config(config_path)
    
    def assess(self, evaluation_data: Dict) -> Dict:
        """
        Assess vendor risk
        
        Args:
            evaluation_data: Dictionary with contract and performance_score
            
        Returns:
            Risk assessment result
        """
        contract = evaluation_data.get("contract", {})
        performance_score = evaluation_data.get("performance_score", 0)
        
        # Extract risk factors
        incidents = contract.get("incidents", [])
        budget = contract.get("budget", {})
        
        critical_incidents = sum(1 for inc in incidents if inc.get("severity") == "critical")
        total_incidents = len(incidents)
        unresolved_incidents = sum(1 for inc in incidents if not inc.get("resolved", True))
        
        budget_overrun_pct = budget.get("overrun__percentage", 0)
        
        # Rule-based risk classification
        risk_level, risk_factors = self._classify_risk(
            performance_score=performance_score,
            critical_incidents=critical_incidents,
            total_incidents=total_incidents,
            unresolved_incidents=unresolved_incidents,
            budget_overrun_pct=budget_overrun_pct
        )
        
        # Determine recommendation
        recommendation = self._get_recommendation(
            risk_level=risk_level,
            performance_score=performance_score,
            critical_incidents=critical_incidents,
            unresolved_incidents=unresolved_incidents
        )
        
        # Generate LLM-based justification
        reason = self._generate_reason(
            vendor_name=contract.get("vendor_name", "Unknown"),
            risk_level=risk_level,
            performance_score=performance_score,
            risk_factors=risk_factors
        )
        
        return {
            "risk_level": risk_level,
            "recommendation": recommendation,
            "reason": reason,
            "risk_factors": risk_factors,
            "metrics": {
                "performance_score": performance_score,
                "critical_incidents": critical_incidents,
                "total_incidents": total_incidents,
                "unresolved_incidents": unresolved_incidents,
                "budget_overrun_pct": budget_overrun_pct
            }
        }
    
    def _classify_risk(
        self,
        performance_score: float,
        critical_incidents: int,
        total_incidents: int,
        unresolved_incidents: int,
        budget_overrun_pct: float
    ) -> tuple:
        """
        Classify risk level using rule-based logic
        
        Returns:
            Tuple of (risk_level, risk_factors)
        """
        risk_factors = []
        
        # Collect risk factors
        if performance_score < 60:
            risk_factors.append(f"Low performance score ({performance_score:.0f}/100)")
        elif performance_score < 80:
            risk_factors.append(f"Below-target performance ({performance_score:.0f}/100)")
        
        if critical_incidents > 2:
            risk_factors.append(f"High number of critical incidents ({critical_incidents})")
        elif critical_incidents > 0:
            risk_factors.append(f"{critical_incidents} critical incident(s)")
        
        if unresolved_incidents > 0:
            risk_factors.append(f"{unresolved_incidents} unresolved incident(s)")
        
        if budget_overrun_pct > 15:
            risk_factors.append(f"Significant budget overrun ({budget_overrun_pct:.1f}%)")
        elif budget_overrun_pct > 5:
            risk_factors.append(f"Budget overrun ({budget_overrun_pct:.1f}%)")
        
        # Apply classification rules
        # HIGH RISK: score < 60 OR critical incidents > 2 OR budget overrun > 15%
        if (
            performance_score < 60 or
            critical_incidents > 2 or
            budget_overrun_pct > 15 or
            unresolved_incidents > 1
        ):
            return "HIGH", risk_factors
        
        # MEDIUM RISK: score 60-79 OR critical incidents 1-2 OR budget overrun 5-15%
        elif (
            (60 <= performance_score < 80) or
            (1 <= critical_incidents <= 2) or
            (5 < budget_overrun_pct <= 15) or
            unresolved_incidents == 1
        ):
            return "MEDIUM", risk_factors
        
        # LOW RISK: score >= 80 AND no critical issues
        else:
            if not risk_factors:
                risk_factors.append("No significant risk factors identified")
            return "LOW", risk_factors
    
    def _get_recommendation(
        self,
        risk_level: str,
        performance_score: float,
        critical_incidents: int,
        unresolved_incidents: int
    ) -> str:
        """
        Get contract recommendation based on risk
        
        Returns:
            Recommendation (RENEW, RENEGOTIATE, TERMINATE, MONITOR)
        """
        if risk_level == "HIGH":
            # Terminate if severe issues
            if performance_score < 50 or critical_incidents >= 3:
                return "TERMINATE"
            else:
                return "RENEGOTIATE"
        
        elif risk_level == "MEDIUM":
            # Renegotiate or monitor
            if unresolved_incidents > 0 or performance_score < 70:
                return "RENEGOTIATE"
            else:
                return "MONITOR"
        
        else:  # LOW risk
            return "RENEW"
    
    def _generate_reason(
        self,
        vendor_name: str,
        risk_level: str,
        performance_score: float,
        risk_factors: list
    ) -> str:
        """
        Generate risk assessment reason using LLM
        
        Args:
            vendor_name: Vendor name
            risk_level: Risk level (LOW/MEDIUM/HIGH)
            performance_score: Performance score
            risk_factors: List of risk factors
            
        Returns:
            Reason text
        """
        risk_text = "\n".join(f"- {factor}" for factor in risk_factors)
        
        prompt = f"""Task: Explain why this vendor is classified as {risk_level} risk in 1 sentence.

Vendor: {vendor_name}
Risk Level: {risk_level}
Performance Score: {performance_score:.0f}/100

Risk Factors:
{risk_text}

Output Format: Write a single sentence explaining the risk classification.

Output:"""
        
        try:
            reason = self.llm_provider.generate(
                prompt=prompt,
                max_tokens=self.llm_config.get("max_tokens", 100),
                temperature=self.llm_config.get("temperature", 0.0)
            )
            
            if not reason or len(reason.strip()) < 10:
                return self._fallback_reason(vendor_name, risk_level, risk_factors)
            
            return reason.strip()
            
        except Exception:
            return self._fallback_reason(vendor_name, risk_level, risk_factors)
    
    def _fallback_reason(self, vendor_name: str, risk_level: str, risk_factors: list) -> str:
        """Generate fallback reason without LLM"""
        if risk_level == "HIGH":
            return f"{vendor_name} is classified as HIGH risk due to: {'; '.join(risk_factors[:2])}."
        elif risk_level == "MEDIUM":
            return f"{vendor_name} presents MEDIUM risk with {len(risk_factors)} concern(s) requiring monitoring."
        else:
            return f"{vendor_name} is LOW risk with strong performance and no significant issues."
