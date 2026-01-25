# Daleel Petroleum - Agentic AI Contract Evaluation System

Enterprise-grade AI agent system for automated contract performance evaluation.

## Overview

This system replaces manual, meeting-based contract evaluations with an autonomous multi-agent workflow that:
- ✅ Objectively assesses contractor performance using structured data
- ✅ Provides full audit trails for compliance
- ✅ Runs locally with no cloud dependency (Ollama)
- ✅ Can switch to Azure OpenAI with 1 config change

## Architecture

**5 Specialized Agents**:
1. **Data Intake Agent** - Validates and structures contract data
2. **Performance Analysis Agent** - Calculates KPI scores
3. **Risk Assessment Agent** - Flags issues and recommends actions
4. **Reporting Agent** - Generates visual reports and audit trails
5. **Orchestrator Agent** - Coordinates workflow and escalations

## Quick Start

### Prerequisites

- Python 3.11+
- Ollama installed and running
- Model: `llama3.2:1b`

### Installation

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull Ollama model
ollama pull llama3.2:1b

# 4. Setup environment
copy .env.example .env
# Edit .env if needed
```

### Running

```bash
# Start Ollama server (if not running)
ollama serve

# Run the application (when implemented)
python src/app.py
```

## Configuration

Edit `config.yaml` to switch between LLM providers:

```yaml
llm:
  provider: ollama  # Change to 'azure' for Azure OpenAI
```

## Project Structure

```
daleel-petro-contracts-agent/
├── src/
│   ├── llm/              # LLM abstraction layer
│   ├── agents/           # Agent implementations (TBD)
│   ├── validators/       # Input/output validation (TBD)
│   └── app.py           # FastAPI application (TBD)
├── data/
│   ├── samples/         # Sample contracts
│   ├── evaluations.csv  # Results tracking
│   └── audit_logs.jsonl # Immutable audit trail
├── tests/               # Unit and integration tests (TBD)
├── config.yaml          # Configuration
├── requirements.txt     # Python dependencies
└── README.md
```

## Development Status

**Phase 1: Foundation** ✅ (Current)
- [x] Project structure
- [x] LLM abstraction layer
- [x] Configuration management

**Phase 2: Data Layer** (Next)
- [ ] Data directory structure
- [ ] Sample contract files
- [ ] Validation module

## Documentation

- [Architecture Design](../../.gemini/antigravity/brain/6b274d81-b9be-48dd-9a81-7f3885b4988c/architecture.md)
- [Implementation Tasks](../../.gemini/antigravity/brain/6b274d81-b9be-48dd-9a81-7f3885b4988c/implementation_tasks.md)

## License

Proprietary - Daleel Petroleum Internal Use Only
