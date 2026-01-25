# Daleel Petroleum: Technical Data Flow & Logic Pathway

This document explains the "Agentic Journey" of our three sample vendors. It details how disparate data sources are synthesized to form high-level executive judgments.

---

## 🏗️ The 4-D Data Architecture
For every vendor, the system "listens" to four distinct data vectors before forming an opinion:

1.  **Metric History (.csv)**: Quantitative time-series data (Uptime, Response Time).
2.  **Incident Logs (.json)**: Critical events, root causes, and resolution efficiency.
3.  **Human Feedback (.md)**: Qualitative sentiment from end-users and managers.
4.  **Market Context (.txt)**: Industry-wide benchmarks (Global SLAs).

---

## 📊 Vendor Case Studies

### 1. ABC IT Solutions (CNT-2024-001) - "The Resilient Partner"
*   **The Data Story**: 
    *   **CSV**: Shows a dip in February (98.8% uptime).
    *   **MD (Reviews)**: Explains the February dip was due to a region-wide ISP failure, not the vendor's hardware.
    *   **LLM Synthesis**: The Agent correlates the "Anomaly" in the CSV with the "Explanation" in the Reviews. 
*   **Final Judgment**: **RENEW**. The AI recognizes that performance is actually 99.4% when adjusted for external factors.

### 2. XYZ Tech Services (CNT-2024-002) - "The Low-Cost Trap"
*   **The Data Story**:
    *   **TXT (Market)**: Shows industry average for response is 2.5 hours.
    *   **CSV**: Shows XYZ takes 4.2 hours.
    *   **JSON (Incidents)**: Highlights that 3 out of 4 incidents were "Preventable" capacity issues.
    *   **LLM Synthesis**: The Agent identifies a "Pattern of Neglect." It reasons that the low price (found in reviews) suggests the vendor is understaffed, leading to high response times and preventable failures.
*   **Final Judgment**: **TERMINATE**. The AI realizes that the $5k savings are erased by the high operational risk of downtime.

### 3. Problematic IT Corp (CNT-2023-015) - "The Systemic Failure"
*   **The Data Story**:
    *   **CSV**: Shows a clear downward trend (97% -> 96.5% -> 96%).
    *   **MD (Reviews)**: Contains aggressive negative feedback ("Never answer the phone," "Constant rebooting").
    *   **LLM Synthesis**: The Agent identifies "Irreparable Relationship Damage." It notes that the vendor has failed to improve despite multiple warnings (tracked in the reasoning chain). 
*   **Final Judgment**: **TERMINATE**. The Agent identifies that "Renegotiation" is high-risk because the core capability is missing.

---

## 🧠 How the Agents Work

### Step 1: Data Orchestration (DataIntakeAgent)
When you click a vendor, this agent "hunts" for files based on the `contract_id`. It reads them into memory and cleans the data:
- Converts CSV rows into a summary string.
- Extracts "Root Causes" from JSON incidents.
- Strips Markdown formatting from reviews into plain text.

### Step 2: Prompt Construction (ReasoningAgent)
The system builds a massive prompt (approx 12,000 characters) following this structure:
```markdown
[System Role]: Expert Auditor for Daleel Petroleum.
[Performance Data]: {performance_summary}
[Incident Data]: {incidents_summary}
[Market Context]: {market_context}
[Reviews]: {past_reviews}
[Instruction]: Analyze step-by-step: Trend -> Pattern -> Context -> Trade-off -> Judgment.
```

### Step 3: LLM Synthesis (Gemini 2.5 Flash)
The formatted "Bundle" of information is sent to Gemini. Because the model has a large "Context Window," it can see all these files simultaneously. 
- It isn't just "predicting text"; it is **verifying claims**. 
- e.g., If the CSV says uptime is 100% but the JSON shows 3 crashes, the AI is instructed to **flag the contradiction**.

### Step 4: Final Output (The Agentic Package)
The AI returns a structured JSON object containing:
- The **Logic Pathway** (What it thought).
- The **Judgment** (Final decision).
- The **Confidence Score** (How sure it is, given the data clarity).
