"""
Reasoning Prompts for Contract Evaluation
Chain-of-thought prompts that require LLM to reason over multiple sources
"""

# Main reasoning prompt for contract evaluation (OPTIMIZED for token efficiency)
REASONING_PROMPT_TEMPLATE = """You are a contract analyst for Daleel Petroleum with 15+ years in vendor management and risk assessment.

Analyze vendor performance by synthesizing these data sources:

**1. PERFORMANCE HISTORY**
{performance_summary}

**2. INCIDENT LOG**
{incidents_summary}

**3. INDUSTRY BENCHMARKS**
{market_context}

**4. PAST REVIEWS**
{past_reviews}

ANALYSIS STEPS (think step-by-step):
1. Performance Trends: Compare metrics vs benchmarks, identify patterns (improving/stable/declining)
2. Incident Patterns: Assess preventability, vendor response quality, systemic issues
3. Context: Market conditions, past reviews, mitigating circumstances
4. Trade-offs: Key strengths vs weaknesses, cost vs value proposition
5. Recommendation: Risk-adjusted action based on synthesis above

CRITICAL REQUIREMENTS:
- SYNTHESIZE across all sources (don't just list each separately)
- CITE EXACT FIGURES (e.g., "99.2% uptime", "3 preventable incidents")
- SHOW REASONING for each step explicitly
- ACKNOWLEDGE conflicts/tensions if sources disagree
- USE JUDGMENT (not formulas) considering full context
- STATE CONFIDENCE level based on data quality
- MAKE A DECISION (must recommend action, no deferring)

OUTPUT (valid JSON only):
{{
  "reasoning_chain": [
    "Step 1: [Performance with specific metrics]",
    "Step 2: [Incident analysis with counts]",
    "Step 3: [Context vs benchmarks]",
    "Step 4: [Trade-offs analysis]",
    "Step 5: [Final recommendation justification]"
  ],
  "performance_assessment": "Summary with min/max/avg metrics (max 300 chars)",
  "risk_factors": ["Specific risk 1", "Specific risk 2"],
  "strengths": ["Strength 1", "Strength 2"],
  "recommendation": "RENEW | RENEGOTIATE | TERMINATE | MONITOR",
  "confidence_level": "HIGH | MEDIUM | LOW",
  "justification": "Evidence-based reasoning citing key metrics (max 300 chars)",
  "alternative_consideration": "What would change recommendation (max 200 chars)"
}}

GUARDRAILS:
- Include ALL JSON keys (especially "justification")
- Quote specific numbers, not vague terms ("96.2%" not "low performance")
- Consider ALL 4 data sources
- Express uncertainty via confidence_level, not by refusing to decide

Generate comprehensive data-driven evaluation now.
"""

# Fallback prompt if main fails
SIMPLE_REASONING_PROMPT = """Analyze this vendor's performance data and provide recommendations.

Performance Data:
{performance_summary}

Incidents:
{incidents_summary}

Provide a JSON response with:
- recommendation (RENEW/RENEGOTIATE/TERMINATE/MONITOR)
- reasoning (your analysis)
- confidence (HIGH/MEDIUM/LOW)
"""
