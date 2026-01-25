# Daleel Petroleum: Contract Intelligence Hub 🚀

An advanced **Agentic AI** platform designed to automate and deepen contract performance evaluation. Moving beyond simple data visualization, this system utilizes Large Language Models (LLMs) to reason through disparate data sources, providing executive-level insights and actionable recommendations.

---

## 🌟 Overview

The Daleel Petroleum Contract Intelligence Hub is a next-generation vendor management system. It doesn't just show you metrics; it understands them. By synthesizing quantitative performance data with qualitative human feedback and market context, the system provides a comprehensive "Logic Pathway" for every contract decision.

### The "Agentic" Difference
Unlike traditional rule-based automation (e.g., "if score < 70 then terminate"), this system behaves as an **Autonomous Auditor**. It cross-references multiple files to identify root causes, weigh market conditions, and resolve contradictions in data (e.g., identifying that a metric dip was caused by an external ISP failure rather than vendor incompetence).

---

## 🏗️ 4-D Data Architecture

The system "thinks" across four distinct data dimensions for every contract:

1.  **📊 Performance Metrics (`.csv`)**: Historical monthly data (Uptime, Response Speed, Satisfaction).
2.  **📌 Incident logs (`.json`)**: Critical events, root causes, and resolution efficiency tracking.
3.  **💬 Human Intelligence (`.md`)**: Qualitative feedback and executive reviews from stakeholders.
4.  **🌍 Market Context (`.txt`)**: Industry-wide benchmarks and global supply chain trends.

---

## 🚀 Key Features

-   **On-Demand Deep Reasoning**: Real-time LLM synthesis triggered instantly upon vendor selection.
-   **Explainable AI (XAI)**: A transparent 5-step "Logic Pathway" showing the exact chain of thought.
-   **Data-Driven Citations**: Recommendations that quote exact figures, SLA variances, and historical facts.
-   **Surgical Extraction Engine**: Advanced JSON parsing with auto-repair to ensure high-fidelity reporting even with large datasets.
-   **Premium Visual Dashboard**: A modern, high-contrast interface designed for executive decision-making.

---

## 🛠️ Tech Stack

-   **Backend**: FastAPI (Python) - Multi-Agent Orchestration.
-   **Frontend**: React (Vite) - Real-time Data Visualization & Skeleton Loaders.
-   **Intelligence Core**: Google Gemini 2.0/3-Flash (via `google-genai` SDK).
-   **Styling**: Vanilla CSS with Glassmorphism aesthetics.
-   **Database**: Local CSV with "Upsert" logic for contract auditing records.

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

# Start the API server
python src/app.py
```

### 3. Frontend Installation
```powershell
cd frontend
npm install

# Start the development server
npm run dev
```
The dashboard will be available at `http://localhost:3000`.

---

## 📁 Repository Structure
```text
├── src/                # Agentic AI & Provider Logic
├── data/               # 4-D Contract Data Repository
├── frontend/           # React Application
├── config.yaml         # Project configuration (Models, Retries, Thresholds)
└── README.md           # Professional Documentation
```

---

## 📜 License
*Proprietary - Developed for Daleel Petroleum Corporation.*
