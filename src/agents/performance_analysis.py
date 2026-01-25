"""
Performance Analysis Agent
Calculates KPI scores and generates justifications using LLM
"""
import json
from typing import Dict, List
from src.llm import get_llm_provider, get_llm_config


class PerformanceAnalysisAgent:
    """
    Analyzes contract KPIs and calculates objective performance scores
    Uses LLM for generating human-readable justifications
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize performance analysis agent
        
        Args:
            config_path: Path to configuration file
        """
        self.llm_provider = get_llm_provider(config_path)
        self.llm_config = get_llm_config(config_path)
    
    def evaluate(self, contract: Dict) -> Dict:
        """
        Evaluate contract performance
        
        Args:
            contract: Contract dictionary
            
        Returns:
            Performance evaluation result
        """
        kpis = contract.get("kpis", [])
        
        if not kpis:
            return {
                "overall_score": 0,
                "grade": "F",
                "kpi_scores": [],
                "justification": "No KPIs available for evaluation"
            }
        
        # Calculate individual KPI scores
        kpi_scores = []
        for kpi in kpis:
            kpi_score = self._score_kpi(kpi)
            kpi_scores.append(kpi_score)
        
        # Calculate overall score (weighted average)
        overall_score = sum(s["score"] for s in kpi_scores) / len(kpi_scores)
        grade = self._calculate_grade(overall_score)
        
        # Generate LLM justification
        justification = self._generate_justification(
            contract.get("vendor_name", "Unknown"),
            kpi_scores,
            overall_score
        )
        
        return {
            "overall_score": round(overall_score, 1),
            "grade": grade,
            "kpi_scores": kpi_scores,
            "justification": justification
        }
    
    def _score_kpi(self, kpi: Dict) -> Dict:
        """
        Score individual KPI
        
        Args:
            kpi: KPI dictionary with target and actual values
            
        Returns:
            KPI score dictionary
        """
        name = kpi.get("name", "Unknown KPI")
        target = kpi.get("target", 0)
        actual = kpi.get("actual", 0)
        unit = kpi.get("unit", "")
        
        # Determine if higher is better (default: yes)
        # Exception: response time (hours) - lower is better
        higher_is_better = "time" not in name.lower() or "satisfaction" in name.lower()
        
        # Calculate score (0-100)
        if target == 0:
            score = 0
        elif higher_is_better:
            score = min(100, (actual / target) * 100)
        else:
            # For metrics where lower is better (e.g., response time)
            score = max(0, min(100, (target / actual) * 100))
        
        # Determine compliance
        compliance = "PASS" if score >= 80 else "FAIL"
        
        # Generate simple justification
        if higher_is_better:
            diff = actual - target
            diff_pct = (diff / target) * 100 if target > 0 else 0
            if diff >= 0:
                reason = f"Exceeded target by {abs(diff_pct):.1f}% ({actual}{unit} vs {target}{unit})"
            else:
                reason = f"Below target by {abs(diff_pct):.1f}% ({actual}{unit} vs {target}{unit})"
        else:
            diff = target - actual
            if diff >= 0:
                reason = f"Better than target by {abs(diff):.1f}{unit} ({actual}{unit} vs {target}{unit})"
            else:
                reason = f"Worse than target by {abs(diff):.1f}{unit} ({actual}{unit} vs {target}{unit})"
        
        return {
            "kpi_name": name,
            "target": target,
            "actual": actual,
            "unit": unit,
            "score": round(score, 1),
            "compliance": compliance,
            "reason": reason
        }
    
    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from score"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _generate_justification(
        self,
        vendor_name: str,
        kpi_scores: List[Dict],
        overall_score: float
    ) -> str:
        """
        Generate human-readable justification using LLM
        
        Args:
            vendor_name: Vendor name
            kpi_scores: List of KPI scores
            overall_score: Overall performance score
            
        Returns:
            Justification text
        """
        # Build KPI summary for prompt
        kpi_summary = []
        for kpi in kpi_scores:
            kpi_summary.append(
                f"- {kpi['kpi_name']}: {kpi['score']:.0f}/100 ({kpi['compliance']}) - {kpi['reason']}"
            )
        kpi_text = "\n".join(kpi_summary)
        
        # Prompt for LLM (structured, concise, no hallucination risk)
        prompt = f"""Task: Generate a 1-2 sentence performance summary.

Vendor: {vendor_name}
Overall Score: {overall_score:.0f}/100

KPI Results:
{kpi_text}

Output Format: Write a brief summary explaining the overall performance in 1-2 sentences. Focus on the most important KPIs and whether the vendor met expectations.

Output:"""
        
        try:
            # Generate justification
            justification = self.llm_provider.generate(
                prompt=prompt,
                max_tokens=self.llm_config.get("max_tokens", 150),
                temperature=self.llm_config.get("temperature", 0.0)
            )
            
            # Fallback if empty response
            if not justification or len(justification.strip()) < 10:
                return self._fallback_justification(vendor_name, overall_score, kpi_scores)
            
            return justification.strip()
            
        except Exception as e:
            # Fallback on LLM error
            return self._fallback_justification(vendor_name, overall_score, kpi_scores)
    
    def _fallback_justification(
        self,
        vendor_name: str,
        overall_score: float,
        kpi_scores: List[Dict]
    ) -> str:
        """Generate fallback justification without LLM"""
        failed_kpis = [k for k in kpi_scores if k["compliance"] == "FAIL"]
        
        if overall_score >= 90:
            return f"{vendor_name} demonstrated excellent performance with an overall score of {overall_score:.0f}/100, meeting or exceeding all major KPIs."
        elif overall_score >= 70:
            return f"{vendor_name} showed satisfactory performance with an overall score of {overall_score:.0f}/100, though {len(failed_kpis)} KPI(s) fell below target."
        else:
            return f"{vendor_name} underperformed with an overall score of {overall_score:.0f}/100, failing to meet {len(failed_kpis)} out of {len(kpi_scores)} KPIs."
