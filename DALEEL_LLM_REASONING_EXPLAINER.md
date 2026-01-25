# LLM Reasoning Explainer: The AI "Auditor" Philosophy

This document provides a deep dive into the "Brain" of the Daleel Petroleum Contract Intelligence Hub. It explains how the system transitions from raw data to sophisticated executive recommendations.

---

## 1. The Reasoning Architecture (Agentic vs. Rule-Based)

### Rules (Old Way):
-   **Logic**: `IF uptime < 98% THEN "Bad Vendor"`
-   **Failure**: Fails to see that the uptime was caused by a region-wide earthquake or ISP failure. It has no "Common Sense."

### Agents (The Intelligence Hub Way):
-   **Logic**: `Analyze [Uptime Dip] against [End-User Feedback] and [Market Context].`
-   **Success**: Recognizes that "Vendor had 97% uptime but the IT team says they worked 48 hours straight to fix an ISP issue outside their control. Market average is also down this month. Judgment: High Resilience."

---

## 2. From Files to Prompt: The "Brain Bundle"

When you click a vendor, the `DataIntakeAgent` and `ReasoningAgent` perform a three-step orchestration:

### A. Data Liquification
The system reads multiple formats into unified plain text:
- **CSV (Performance)**: Summarized into trends (e.g., "Uptime trending DOWN from Jan to June").
- **JSON (Incidents)**: Categorized by severity and "Root Cause" patterns.
- **MD (Reviews)**: Scanned for emotional keywords (e.g., "Frustrated," "Exceptional Service").
- **TXT (Benchmarks)**: Loaded as the "Moral Compass" for what a good vendor should be.

### B. The Context Injection
These summaries are injected into the **Reasoning Prompt Template**. This template isn't just a question; it's a **Persona Assignment**:
> *"You are an expert contract analyst with 15 years experience. Synthesis across sources. Acknowledge tensions. Do NOT use simple formulas. Show your reasoning steps."*

### C. The 5-Step Logic Pathway
The LLM is strictly instructed to think in this order:
1.  **Step 1: Trend Analysis** (Is performance stable?)
2.  **Step 2: Pattern ID** (Are incidents preventable or bad luck?)
3.  **Step 3: Nuance & Context** (Do market factors explain the gaps?)
4.  **Step 4: Trade-Off** (Is the low price worth the high risk?)
5.  **Step 5: Final Judgment** (The definitive RENEW/TERMINATE decision).

---

## 3. The "Silent Auditor" Guardrails

To ensure the AI doesn't "hallucinate" or provide generic advice, we use **Verification Guardrails**:

- **No Deferation**: The AI is banned from saying "I need more info." It must make a decision based on available data, stating low confidence if necessary.
- **Tension Resolution**: If the metrics look good but the Human Reviews are angry, the AI is forced to explain why it chose one over the other.
- **Conciseness Constraints**: We limit reasoning steps to ~250 characters to ensure the "Logic Pathway" is readable for busy executives.

---

## 🛠️ Implementation Specs (For Tech Review)
- **Model**: Gemini-2.5-Flash-Lite (Optimized for JSON extraction & long-context reasoning).
- **Temperature**: 0.3 (Low variability to ensure consistent auditor-style reports).
- **Prompt Length**: ~12,000 characters of rich context per analysis.
- **Format**: Structured JSON output ensures 100% compatibility with our high-fidelity frontend.
