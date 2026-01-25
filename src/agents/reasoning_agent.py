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
        Parse LLM's JSON response with robust extraction and repair
        """
        import re
        
        # 1. Clean response (remove markdown and find JSON block)
        # Find the FIRST '{' and the LAST '}' to extract the core JSON object
        first_brace = response.find('{')
        last_brace = response.rfind('}')
        
        if first_brace != -1:
            if last_brace != -1 and last_brace > first_brace:
                # We have a potentially complete JSON block
                response_clean = response[first_brace:last_brace+1].strip()
            else:
                # Potentially truncated JSON (missing closing brace)
                response_clean = response[first_brace:].strip()
        else:
            response_clean = response.strip()
        
        # 2. Advanced JSON repair for truncation
        if not response_clean.endswith("}"):
            print("[ReasoningAgent] Detected truncated JSON, performing deep repair...")
            
            # Remove trailing commas, colons, or incomplete keys/values
            # e.g., '{"key": "val", ' -> '{"key": "val"'
            response_clean = re.sub(r'[,\s:]+$', '', response_clean)
            
            # If we ended inside a string, close the quote
            if response_clean.count('"') % 2 != 0:
                response_clean += '"'
                
            # Balance brackets by adding missing closing ones
            open_braces = response_clean.count('{')
            close_braces = response_clean.count('}')
            if open_braces > close_braces:
                # If we are inside an array at the end, close it first
                open_brackets = response_clean.count('[')
                close_brackets = response_clean.count(']')
                if open_brackets > close_brackets:
                    response_clean += ']' * (open_brackets - close_brackets)
                
                # Close the main object(s)
                response_clean += '}' * (open_braces - close_braces)

        try:
            parsed = json.loads(response_clean)
            
            # Map LLM variations to standard keys if necessary
            # (e.g., "reasoning" -> "reasoning_chain")
            if "reasoning" in parsed and "reasoning_chain" not in parsed:
                parsed["reasoning_chain"] = [parsed["reasoning"]] if isinstance(parsed["reasoning"], str) else parsed["reasoning"]

            # Ensure all required fields exist with defaults
            if "justification" not in parsed or not parsed["justification"]:
                parsed["justification"] = "Recommendation based on synthesis of multi-source performance and risk data."
            
            if "strengths" not in parsed:
                parsed["strengths"] = []
            if "risk_factors" not in parsed:
                parsed["risk_factors"] = []

            # Normalize recommendation and confidence
            if "recommendation" in parsed:
                parsed["recommendation"] = parsed["recommendation"].upper()
                if "RENEW" in parsed["recommendation"]: parsed["recommendation"] = "RENEW"
                elif "TERMINATE" in parsed["recommendation"]: parsed["recommendation"] = "TERMINATE"
                elif "RENEGOTIATE" in parsed["recommendation"]: parsed["recommendation"] = "RENEGOTIATE"
                elif "MONITOR" in parsed["recommendation"]: parsed["recommendation"] = "MONITOR"
            else:
                parsed["recommendation"] = "MONITOR"
            
            if "confidence_level" in parsed:
                parsed["confidence_level"] = parsed["confidence_level"].upper()
                if "HIGH" in parsed["confidence_level"]: parsed["confidence_level"] = "HIGH"
                elif "MEDIUM" in parsed["confidence_level"]: parsed["confidence_level"] = "MEDIUM"
                elif "LOW" in parsed["confidence_level"]: parsed["confidence_level"] = "LOW"
            else:
                parsed["confidence_level"] = "MEDIUM"

            return parsed
            
        except json.JSONDecodeError as e:
            # 3. Handle 'Extra data' error by trimming at the exact error position
            if "Extra data" in str(e):
                print(f"[ReasoningAgent] Extra data detected at pos {e.pos}, trimming...")
                try:
                    # Attempt to parse the string up to the error position
                    parsed = json.loads(response_clean[:e.pos].strip())
                    # If successful, proceed with the rest of the parsing logic
                    if "reasoning" in parsed and "reasoning_chain" not in parsed:
                        parsed["reasoning_chain"] = [parsed["reasoning"]] if isinstance(parsed["reasoning"], str) else parsed["reasoning"]
                    if "justification" not in parsed or not parsed["justification"]:
                        parsed["justification"] = "Recommendation based on synthesis of multi-source performance and risk data."
                    if "strengths" not in parsed:
                        parsed["strengths"] = []
                    if "risk_factors" not in parsed:
                        parsed["risk_factors"] = []
                    if "recommendation" in parsed:
                        parsed["recommendation"] = parsed["recommendation"].upper()
                        if "RENEW" in parsed["recommendation"]: parsed["recommendation"] = "RENEW"
                        elif "TERMINATE" in parsed["recommendation"]: parsed["recommendation"] = "TERMINATE"
                        elif "RENEGOTIATE" in parsed["recommendation"]: parsed["recommendation"] = "RENEGOTIATE"
                        elif "MONITOR" in parsed["recommendation"]: parsed["recommendation"] = "MONITOR"
                    else:
                        parsed["recommendation"] = "MONITOR"
                    if "confidence_level" in parsed:
                        parsed["confidence_level"] = parsed["confidence_level"].upper()
                        if "HIGH" in parsed["confidence_level"]: parsed["confidence_level"] = "HIGH"
                        elif "MEDIUM" in parsed["confidence_level"]: parsed["confidence_level"] = "MEDIUM"
                        elif "LOW" in parsed["confidence_level"]: parsed["confidence_level"] = "LOW"
                    else:
                        parsed["confidence_level"] = "MEDIUM"
                    return parsed
                except:
                    # If trimming and re-parsing fails, fall through to general error handling
                    pass
            
            print(f"[ReasoningAgent] JSON parsing still failed after repair: {str(e)}")
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
