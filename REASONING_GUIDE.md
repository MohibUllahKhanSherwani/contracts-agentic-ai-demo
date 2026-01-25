# Reasoning Architecture - User Guide

## 🧠 What Changed: Rule-Based → True Reasoning

### Before (Phases 1-4): Automation with LLM Summaries ❌

```python
# Old Performance Agent
score = (actual / target) * 100  # Formula
if score < 60:
    risk = "HIGH"  # Hardcoded rule
    
llm_text = generate_summary(score)  # LLM only for text
```

**Problem**: This is **automation**, not **reasoning**.  
The LLM didn't make decisions - it just generated text.

---

### After (Reasoning Upgrade): True Agentic Reasoning ✅

```python
# New Reasoning Agent
data_sources = load_all_sources(contract_id)  # CSV + JSON + TXT + MD
llm_decision = llm.analyze(data_sources)  # LLM makes decision
# NO formulas, NO rules - pure reasoning
```

**Key Difference**:  
✅ LLM reads 4-5 different file types  
✅ LLM synthesizes across sources  
✅ LLM shows step-by-step reasoning (chain-of-thought)  
✅ LLM makes the final decision  

---

## 📁 New Data Architecture

### Multi-Source Data for Each Contract

```
data/
├── performance/
│   └── CNT-2024-001_history.csv     # Time-series metrics (6 months)
├── incidents/
│   └── CNT-2024-001_incidents.json  #  Detailed incident logs with context
├── market/
│   └── industry_benchmarks.txt      # Industry context (shared)
└── reviews/
    └── CNT-2024-001_reviews.md      # Past human evaluations
```

### Example: ABC IT Solutions Data

**Performance CSV** (data/performance/CNT-2024-001_history.csv):
```csv
month,uptime_pct,avg_response_hours,incidents_count,critical_incidents,user_satisfaction
2024-01,99.2,1.8,5,1,4.3
2024-02,98.8,2.3,8,2,3.9
2024-03,99.6,1.2,3,0,4.8
...
```

**Incidents JSON** (data/incidents/CNT-2024-001_incidents.json):
```json
[
  {
    "incident_id": "INC-2024-042",
    "date": "2024-02-15",
    "severity": "critical",
    "description": "Database cluster failure...",
    "root_cause": "Configuration error after upgrade",
    "preventable": true,
    "vendor_response_quality": "excellent"
  }
]
```

**Market Context** (data/market/industry_benchmarks.txt):
```
Industry Average SLA: 99.0% - 99.5%
2024 Trend: Average uptime declined 0.3% due to supply chain...
Typical Critical Incident Rate: 1-2 per quarter
```

**Past Reviews** (data/reviews/CNT-2024-001_reviews.md):
```markdown
# Q1 2024 Review
Reviewer: Sarah Ahmed, Senior IT Manager

Strengths:
- Responsive 24/7 support
- Strong technical competence

Concerns:
- February incident was preventable
- Uptime trending below 99% target

Recommendation: MONITOR - Continue but increase oversight
```

---

## 🔬 How Reasoning Works

### Step 1: Document Loader

```python
from src.ingestion import DocumentLoader

loader = DocumentLoader()
bundle = loader.load_contract_bundle("CNT-2024-001")

# Returns:
{
  "performance_history": DataFrame,  # from CSV
  "incidents": List[Dict],           # from JSON
  "market_context": str,             # from TXT
  "past_reviews": str                # from MD
}
```

### Step 2: Reasoning Prompt

The agent builds a comprehensive prompt:

```
You are an expert contract analyst.

DATA SOURCES:
1. Performance History: [CSV data as text]
2. Incident Log: [JSON incidents as text]
3. Industry Benchmarks: [Market context]
4. Past Human Reviews: [Review markdown]

ANALYZE step-by-step:
Step 1: Performance trend analysis
Step 2: Incident pattern assessment
Step 3: Contextual factors
Step 4: Trade-off analysis
Step 5: Risk-adjusted recommendation

OUTPUT: JSON with reasoning_chain, recommendation, confidence
```

### Step 3: LLM Reasoning

```python
from src.agents import ReasoningAgent

agent = ReasoningAgent()
result = agent.evaluate("CNT-2024-001")

# Returns:
{
  "reasoning_chain": [
    "Step 1: Performance shows 99.2% avg, slightly below 99% target but...",
    "Step 2: One critical incident in Feb, but vendor response was excellent...",
    "Step 3: Industry avg is 99.0% due to supply chain issues, vendor is above...",
    "Step 4: Strengths: responsive support. Concerns: minor SLA miss...",
    "Step 5: Given improving trend and strong response, recommend RENEW"
  ],
  "recommendation": "RENEW",
  "confidence_level": "HIGH",
  "justification": "Vendor performance is solid despite one incident..."
}
```

---

## 🧪 Testing the Reasoning Agent

### Run the Test Script

```bash
cd d:\Projects\daleel-petro-contracts-agent
python tests\test_reasoning_agent.py
```

### Expected Output

```
======================================================================
REASONING AGENT TEST - Multi-Source LLM Analysis
======================================================================

[2/4] Evaluating: ABC IT Solutions (CNT-2024-001)
======================================================================

🧠 REASONING CHAIN:
   1. Analyzing performance: Uptime averages 99.2% over 6 months, slightly...
   2. Incident assessment: One critical incident in February was preventable...
   3. Market context: Industry average is 99.0%, vendor performing above...
   4. Trade-offs: Strong vendor response and improvement trend outweigh...
   5. Final recommendation: RENEW with continued monitoring

📊 PERFORMANCE ASSESSMENT:
   ABC IT Solutions demonstrates above-average performance with...

✅ STRENGTHS:
   • Excellent incident response and post-mortem documentation
   • Performance trending positively after February recovery
   • Above industry benchmarks given 2024 market challenges

⚠️  RISK FACTORS:
   • One preventable configuration error in February
   • Uptime occasionally dips below 99% SLA target

🎯 RECOMMENDATION: RENEW
   Confidence: HIGH
   Justification: Vendor's strong response to incidents and above-market...
```

---

## 🎛️ Configuration

### Update LLM Model (When Ready)

**File**: `config.yaml`

```yaml
llm:
  provider: ollama
  ollama:
    model: llama3.1:8b  # Changed from llama3.2:1b
    temperature: 0.3     # Slightly creative for reasoning
    max_tokens: 2048     # Longer for reasoning chains
```

**Pull the model**:
```bash
ollama pull llama3.1:8b  # ~8GB, better reasoning
```

---

## 📊 Comparing Old vs New

### Scenario: XYZ Tech Services

**Old System (Rule-Based)**:
```
Uptime: 96.5% → Score: (96.5/99)*100 = 97.5
Critical incidents: 3 → if > 2: risk = HIGH
Budget overrun: 5% → if > 5%: flag

Result: HIGH risk, TERMINATE
```

**New System (Reasoning)**:
```
LLM reads:
- Performance CSV: Declining trend, 96.5% current
- Incidents JSON: 3 critical, but 2 were during staff shortage
- Market TXT: Industry hiring crisis (18% vacancy rate)
- Review MD: "Vendor attempting to improve, hired new staff"

LLM reasoning:
"While metrics are below target, the root cause analysis shows
external factors (talent shortage) are improving. Vendor hired
a security specialist in May. Given market context and vendor
responsiveness, recommend RENEGOTIATE with 90-day performance
targets rather than immediate termination."

Result: MEDIUM risk, RENEGOTIATE (60-day trial)
```

**Key Difference**: Context and nuance vs rigid rules.

---

## 🚨 Ambiguous Scenarios (Showcase Reasoning)

### Scenario 1: "The Improving Underperformer"

**Data**:
- Performance: Currently 94% (target 99%), but up from 88% 3 months ago
- Incidents: 3 critical in Q1, 0 in Q2
- Market: Industry avg 96% due to supply issues
- Review: "Vendor acknowledged issues, hired new team lead"

**No Clear Answer**:
- Terminate? They're improving and industry is struggling
- Renew? Still 5% below target
- **LLM Must Reason**: Weigh improvement trajectory vs current gap

### Scenario 2: "High Cost, High Quality"

**Data**:
- Performance: 99.8% uptime (excellent)
- Incidents: Zero in 12 months
- Cost: $300k/year vs market rate $220k
- Review: "Outstanding but CFO questioning cost"

**Tension**: Pay premium for reliability or switch to save $80k/year?

---

## 🛡️ Guardrails (Anti-Bypass)

### Problem: LLM Says "I Can't Decide"

**Solution**: Prompt explicitly forbids bypass

```python
# In reasoning_prompts.py
"""
CRITICAL: You MUST provide a recommendation. Do not say
"I cannot decide" or "insufficient data". Use your best
judgment based on available information. State confidence
level if uncertain, but always decide.
```

### Validation

```python
def validate_reasoning(result):
    # Check 1: Has recommendation
    assert result["recommendation"] in ["RENEW", "RENEGOTIATE", "TERMINATE", "MONITOR"]
    
    # Check 2: Has reasoning chain
    assert len(result["reasoning_chain"]) >= 3
    
    # Check 3: No bypass phrases
    forbidden = ["cannot decide", "insufficient information"]
    assert not any(phrase in str(result).lower() for phrase in forbidden)
```

---

## 📈 Next Steps

### Phase A: Test Current System ✅ (You're Here)
1. Run `python tests\test_reasoning_agent.py`
2. Review reasoning chains for quality
3. Verify LLM makes decisions (not just summaries)

### Phase B: Upgrade LLM Model 🔄 (Your Task)
```bash
ollama pull llama3.1:8b
# Then update config.yaml
```

### Phase C: Frontend Integration (Future)
- Show reasoning chain in dashboard
- Display confidence levels
- Highlight which data sources influenced decision

---

## 🔍 Debugging

### Issue: "No module named 'pandas'"
```bash
pip install -r requirements-reasoning.txt
```

### Issue: LLM Response Parsing Fails
- Check `raw_llm_response` field in result
- LLM might not be powerful enough (upgrade model)
- Adjust temperature in config (try 0.1-0.5 range)

### Issue: Reasoning Quality Poor
- **Root Cause**: Model too small (llama3.2:1b insufficient)
- **Solution**: Upgrade to llama3.1:8b or larger
- **Verify**: Check reasoning_chain for depth and specificity

---

## 📚 File Reference

### New Files Created
```
src/
├── ingestion/
│   ├── __init__.py
│   └── document_loader.py      # Multi-source data loading
├── prompts/
│   ├── __init__.py
│   └── reasoning_prompts.py    # Chain-of-thought prompts
└── agents/
    └── reasoning_agent.py      # LLM-driven reasoning

data/
├── performance/
│   ├── CNT-2024-001_history.csv
│   ├── CNT-2024-002_history.csv
│   └── CNT-2023-015_history.csv
├── incidents/
│   ├── CNT-2024-001_incidents.json
│   ├── CNT-2024-002_incidents.json
│   └── CNT-2023-015_incidents.json
├── market/
│   └── industry_benchmarks.txt
└── reviews/
    ├── CNT-2024-001_reviews.md
    ├── CNT-2024-002_reviews.md
    └── CNT-2023-015_reviews.md

tests/
└── test_reasoning_agent.py     # Reasoning test script

requirements-reasoning.txt       # Additional dependencies
```

---

## ✅ Success Criteria

You've successfully implemented true reasoning if:

- [ ] LLM reads multiple file types (CSV, JSON, TXT, MD)
- [ ] LLM shows step-by-step reasoning (5-step chain)
- [ ] LLM makes final recommendation (not just summaries)
- [ ] System handles ambiguous scenarios (no clear pass/fail)
- [ ] Reasoning incorporates market context and human reviews
- [ ] Different data sources lead to different recommendations

**Test**: Try changing one data source (e.g., past review) and see if LLM's recommendation changes. If yes, true reasoning! If no, still rule-based.

---

## 🎓 Key Concepts

**Agentic AI** = System makes decisions autonomously using reasoning  
**Chain-of-Thought** = LLM shows step-by-step thought process  
**Multi-Source Synthesis** = Combining disparate data types  
**Confidence Scoring** = LLM states certainty level  
**Anti-Bypass** = Preventing LLM from refusing to decide  

---

## 💡 Future Enhancements

- [ ] Add actual PDF contract parsing (pypdf)
- [ ] Include financial data from Excel (openpyxl)
- [ ] Implement prompt A/B testing
- [ ] Add reasoning visualization in dashboard
- [ ] Create prompt engineering UI
- [ ] Compare recommendations across different LLM models

---

**Next**: Run the test script and upgrade your LLM model! 🚀
