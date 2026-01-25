"""
Reasoning Prompts for Contract Evaluation
Chain-of-thought prompts that require LLM to reason over multiple sources
"""

# Main reasoning prompt for contract evaluation
REASONING_PROMPT_TEMPLATE = """You are an expert contract analyst for Daleel Petroleum Corporation with 15 years of experience in vendor management, risk assessment, and strategic sourcing.

Your task is to analyze vendor performance by synthesizing information from MULTIPLE disparate data sources and providing a comprehensive, reasoned evaluation.

=================================================================
DATA SOURCES PROVIDED
=================================================================

**1. PERFORMANCE HISTORY (Time-Series Metrics)**
{performance_summary}

**2. INCIDENT LOG (Critical Events & Root Causes)**
{incidents_summary}

**3. INDUSTRY BENCHMARKS (Market Context)**
{market_context}

**4. PAST HUMAN REVIEWS (Stakeholder Perspectives)**
{past_reviews}

=================================================================
YOUR ANALYSIS TASK
=================================================================

Analyze ALL sources above comprehensively and think step-by-step through your reasoning:

### Step 1: Performance Trend Analysis
- Is performance improving, stable, or declining over time?
- Are there seasonal patterns or one-time anomalies?
- How does actual performance compare to industry benchmarks?
- What is the magnitude of any gaps?

### Step 2: Incident Pattern Assessment
- What types of incidents occurred (preventable vs external)?
- Is there a pattern indicating systemic issues?
- How did the vendor respond to incidents?
- Are there unresolved issues that indicate capability problems?

### Step 3: Contextual Factors
- How do market conditions affect this evaluation?
- Are industry-wide challenges impacting this vendor?
- What do past human reviews reveal about vendor relationship quality?
- Are there mitigating circumstances that explain performance gaps?

### Step 4: Trade-Off Analysis
- What are the vendor's key strengths?
- What are the primary concerns or weaknesses?
- How do quantitative metrics align with qualitative assessments?
- What is the cost vs value proposition?

### Step 5: Risk-Adjusted Recommendation
- What is the overall risk level (consider multiple dimensions)?
- What action best balances risk, cost, and operational needs?
- What would need to change for a different recommendation?
- How confident are you in this assessment given available data?

=================================================================
CRITICAL REQUIREMENTS
=================================================================

1. **SYNTHESIZE across sources** - Don't just summarize each source separately
2. **SHOW YOUR REASONING** - Explicitly state your thought process step-by-step
3. **CITE EXACT FIGURES** - Always quote specific data points (e.g., "99.2% uptime", "4.2h response", "3 preventable incidents")
4. **ACKNOWLEDGE TENSIONS** - If sources conflict, explain how you weighed them
5. **USE JUDGMENT** - Do NOT apply simple formulas; consider context and nuance
6. **STATE CONFIDENCE** - Be explicit about certainty level and what could change your mind
7. **MAKE A DECISION** - You MUST provide a recommendation; do not defer to "need more info"

=================================================================
OUTPUT FORMAT (JSON)
=================================================================

Provide your analysis as valid JSON. KEEP TEXT CONCISE BUT DATA-RICH (max 300 chars per string). Focus on quoting exact metrics:

{{
  "reasoning_chain": [
    "Step 1: [Performance analysis with uptime/speed metrics]",
    "Step 2: [Incident analysis listing specific failure counts]",
    "Step 3: [Contextual analysis vs benchmarks]",
    "Step 4: [Trade-off analysis cost vs quality]",
    "Step 5: [Final recommendation and summary conclusion]"
  ],
  "performance_assessment": "Summary quoting min/max/avg metrics (max 300 chars)",
  "risk_factors": ["Specific risk 1", "Specific risk 2"],
  "strengths": ["Strength 1", "Strength 2"],
  "recommendation": "RENEW | RENEGOTIATE | TERMINATE | MONITOR",
  "confidence_level": "HIGH | MEDIUM | LOW",
  "justification": "Evidence-based logic quoting critical metrics (max 300 chars)",
  "alternative_consideration": "Condition for change (max 200 chars)"
}}

=================================================================
IMPORTANT GUARDRAILS
=================================================================

- MANDATORY: Include every single key in the JSON structure. Do NOT omit "justification" or others.
- Do NOT use generic phrases like "performance was low" - use "performance was 96.2%"
- Do NOT skip incident counts or specific benchmark comparison values
- Do NOT ignore market context or past reviews - these provide critical perspective
- Do ACKNOWLEDGE uncertainty through confidence_level, not by refusing to decide
- Do EXPLAIN reasoning for each of the 5 steps explicitly with data

Now, analyze the vendor data provided above and generate your comprehensive data-driven evaluation.
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
