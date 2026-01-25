"""
Reasoning Agent - True LLM-Driven Decision Making
NO formulas, NO hardcoded rules - pure reasoning over multiple data sources
"""
import json
from typing import Dict, Optional
from src.ingestion.document_loader import DocumentLoader
from src.llm import get_llm_provider, get_llm_config
from src.prompts.reasoning_prompts import REASONING_PROMPT_TEMPLATE


class ReasoningAgent:
    """
    Analyzes contracts using LLM reasoning over multiple disparate data sources
    
    This agent does NOT use formulas or rules. Instead, it:
    1. Loads data from multiple sources (CSV, JSON, TXT, MD)
    2. Synthesizes information into a comprehensive prompt
    3. Asks LLM to reason step-by-step
    4. Returns the LLM's decision with reasoning chain
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize reasoning agent
        
        Args:
            config_path: Path to configuration file
        """
        self.loader = DocumentLoader()
        self.llm = get_llm_provider(config_path)
        self.llm_config = get_llm_config(config_path)
    
    def evaluate(self, contract_id: str) -> Dict:
        """
        Evaluate contract using pure LLM reasoning over multiple sources
        
        Args:
            contract_id: Contract ID to evaluate
            
        Returns:
            {
                "contract_id": str,
                "reasoning_chain": List[str],
                "performance_assessment": str,
                "risk_factors": List[str],
                "strengths": List[str],
                "recommendation": str,
                "confidence_level": str,
                "justification": str,
                "alternative_consideration": str,
                "data_completeness": float,
                "raw_llm_response": str
            }
        """
        # 1. Load ALL data sources
        print(f"[ReasoningAgent] Loading data for {contract_id}...")
        bundle = self.loader.load_contract_bundle(contract_id)
        
        # 2. Convert data to text summaries for LLM
        performance_summary = self.loader.summarize_performance(
            bundle.get("performance_history")
        )
        
        incidents_summary = self.loader.summarize_incidents(
            bundle.get("incidents", [])
        )
        
        market_context = bundle.get("market_context", "No market data available")[:2000]  # Limit length
        
        past_reviews = self.loader.extract_review_summary(
            bundle.get("past_reviews")
        )
        
        # 3. Build comprehensive reasoning prompt
        prompt = REASONING_PROMPT_TEMPLATE.format(
            performance_summary=performance_summary,
            incidents_summary=incidents_summary,
            market_context=market_context,
            past_reviews=past_reviews
        )
        
        print(f"[ReasoningAgent] Sending to LLM for reasoning (prompt length: {len(prompt)} chars)...")
        
        # 4. LLM reasoning (slightly higher temperature for nuanced reasoning)
        try:
            llm_response = self.llm.generate(
                prompt=prompt,
                max_tokens=self.llm_config.get("max_tokens", 2048),
                temperature=0.3  # Slight creativity for reasoning
            )
            
            print(f"[ReasoningAgent] Received LLM response (length: {len(llm_response)} chars)")
            
            # 5. Parse structured JSON response
            result = self._parse_llm_response(llm_response)
            
            # 6. Add metadata
            result["contract_id"] = contract_id
            result["data_completeness"] = bundle.get("data_completeness", 0.0)
            result["raw_llm_response"] = llm_response
            
            return result
            
        except Exception as e:
            print(f"[ReasoningAgent] Error during LLM reasoning: {str(e)}")
            return self._fallback_response(contract_id, str(e))
    
    def _parse_llm_response(self, response: str) -> Dict:
        """
        Parse LLM's JSON response
        
        Args:
            response: Raw LLM text response
            
        Returns:
            Parsed dictionary with reasoning
        """
        # Try to extract JSON from response
        # LLM might wrap JSON in markdown code blocks
        response_clean = response.strip()
        
        # Remove markdown code blocks if present
        if response_clean.startswith("```json"):
            response_clean = response_clean[7:]  # Remove ```json
        if response_clean.startswith("```"):
            response_clean = response_clean[3:]  # Remove ```
        if response_clean.endswith("```"):
            response_clean = response_clean[:-3]  # Remove trailing ```
        
        response_clean = response_clean.strip()
        
        try:
            parsed = json.loads(response_clean)
            
            # Validate required fields
            required_fields = [
                "reasoning_chain",
                "recommendation",
                "confidence_level",
                "justification"
            ]
            
            for field in required_fields:
                if field not in parsed:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate recommendation value
            valid_recommendations = ["RENEW", "RENEGOTIATE", "TERMINATE", "MONITOR"]
            if parsed["recommendation"] not in valid_recommendations:
                raise ValueError(f"Invalid recommendation: {parsed['recommendation']}")
            
            # Validate confidence level
            valid_confidence = ["HIGH", "MEDIUM", "LOW"]
            if parsed["confidence_level"] not in valid_confidence:
                raise ValueError(f"Invalid confidence_level: {parsed['confidence_level']}")
            
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"[ReasoningAgent] JSON parsing failed: {str(e)}")
            print(f"[ReasoningAgent] Response preview: {response_clean[:500]}...")
            
            # Fallback: try to extract key information with regex/heuristics
            return self._extract_structured_fallback(response)
    
    def _extract_structured_fallback(self, response: str) -> Dict:
        """
        Fallback parser if JSON fails - extract key info from free text
        
        Args:
            response: Raw LLM response
            
        Returns:
            Best-effort structured dictionary
        """
        # Simple heuristic extraction
        result = {
            "reasoning_chain": ["LLM response could not be parsed as JSON - see raw response"],
            "performance_assessment": response[:500],  # First 500 chars
            "risk_factors": ["Unable to extract - see raw response"],
            "strengths": ["Unable to extract - see raw response"],
            "recommendation": "MONITOR",  # Safe default
            "confidence_level": "LOW",  # Low confidence due to parsing failure
            "justification": "Parsing error - manual review recommended",
            "alternative_consideration": "Review raw LLM response for details"
        }
        
        # Try to find recommendation keywords
        response_upper = response.upper()
        if "TERMINATE" in response_upper:
            result["recommendation"] = "TERMINATE"
        elif "RENEGOTIATE" in response_upper:
            result["recommendation"] = "RENEGOTIATE"
        elif "RENEW" in response_upper:
            result["recommendation"] = "RENEW"
        
        return result
    
    def _fallback_response(self, contract_id: str, error: str) -> Dict:
        """
        Generate fallback response if LLM fails completely
        
        Args:
            contract_id: Contract ID
            error: Error message
            
        Returns:
            Error response dictionary
        """
        return {
            "contract_id": contract_id,
            "reasoning_chain": [f"ERROR: {error}"],
            "performance_assessment": "Unable to assess - LLM evaluation failed",
            "risk_factors": ["System error during assessment"],
            "strengths": ["Unable to determine"],
            "recommendation": "MONITOR",
            "confidence_level": "LOW",
            "justification": f"Evaluation failed: {error}. Manual review required.",
            "alternative_consideration": "System error - cannot provide alternative analysis",
            "data_completeness": 0.0,
            "error": error
        }
