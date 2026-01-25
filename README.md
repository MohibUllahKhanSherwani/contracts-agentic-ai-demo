# Agentic AI Contracts Specialist: Intelligence Hub 🚀

An advanced **Agentic AI** platform designed to automate and deepen contract performance evaluation. Moving beyond simple data visualization, this system functions as an **Autonomous Contracts Agent**, utilizing Large Language Models (LLMs) to reason through complex, multi-source data to provide executive-level insights and audit-ready recommendations.

---

## 🌟 Overview

The **Intelligence Hub** is a next-generation vendor management system that scales the expertise of a Senior Contracts Specialist. It doesn't just show you metrics; it understands the "Why" behind them. By synthesizing quantitative performance data with qualitative human feedback and market context, the system provides a comprehensive **Logic Pathway** for every contract decision—functioning effectively as a 24/7 digital auditor.

### The "Agentic" Advantage
While traditional automation is trapped by rigid "if/then" rules, this system behaves like a human specialist. It cross-references disparate files to identify root causes, weigh market conditions, and resolve contradictions in data (e.g., distinguishing between a vendor's internal failure and an external market anomaly).

---

## 🏗️ 4-D Data Architecture

The AI Agent "thinks" across four distinct data dimensions for every contract:

1.  **📊 Performance Metrics (`.csv`)**: Historical monthly trends (SLA Compliance, Speed, Satisfaction).
2.  **📌 Incident Logs (`.json`)**: Deep-dive tracking of critical events, root causes, and resolution efficiency.
3.  **💬 Human Intelligence (`.md`)**: Qualitative sentiment, stakeholder reviews, and qualitative pain points.
4.  **🌍 Market Context (`.txt`)**: Industry-wide benchmarks, supply chain trends, and global standards.

---

## 🚀 Key Features

-   **Autonomous Audit Logic**: Real-time LLM reasoning triggered instantly upon vendor selection.
-   **Explainable AI (XAI)**: A transparent 5-step "Logic Pathway" revealing the Agent's specific reasoning process.
-   **Data-Backed Citations**: Judgments that quote exact figures, variance percentages, and historical facts.
-   **Surgical Extraction & Repair**: Advanced JSON engines ensure high-fidelity reporting even with massive data payloads.
-   **Executive Dashboard**: A premium, high-contrast interface designed for rapid decision-making.

---

## 🛠️ Tech Stack

-   **Backend**: FastAPI (Python) - Multi-Agent Orchestration.
-   **Frontend**: React (Vite) - Real-time Visualization & Logic Mapping.
-   **Intelligence Core**: Google Gemini 2.0/3-Flash (via `google-genai` SDK).
-   **Styling**: Modern Glassmorphism using Vanilla CSS.
-   **Data Layer**: Persistence-enabled CSV storage with intelligent "Upsert" logic.

---

## 🏁 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- [Google Gemini API Key](https://aistudio.google.com/)

### 1. Set up Environment
Clone the repository and create a `.env` file in the root:
```env
GEMINI_API_KEY=your_api_key_here
```

### 2. Backend Installation
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start the AI Agent Service
python src/app.py
```

### 3. Frontend Installation
```powershell
cd frontend
npm install

# Start the Intelligence Dashboard
npm run dev
```
The dashboard will be available at `http://localhost:3000`.

---

## 📁 Repository Structure
```text
├── src/                # Agentic AI & Reasoning Logic
├── data/               # 4-D Data Repository (Samples Included)
├── frontend/           # React Application & UI Components
├── config.yaml         # Configuration (Models, Thresholds, Retries)
└── README.md           # Documentation
```

---

## 📜 License
*Open Source - Distributed for professional contract evaluation use.*
