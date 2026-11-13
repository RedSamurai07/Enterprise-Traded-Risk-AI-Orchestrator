# AegisRisk - Enterprise Traded Risk AI Orchestrator

An End-to-End Capstone Project Covering All HSBC AI Engineer (Traded Risk) JD Requirements.

## Project Overview & Architecture

This project implements a full production-grade AI pipeline for a banking environment. It connects all the core competencies required for a modern Traded Risk AI Engineer:

*   **LangGraph:** Multi-agent state orchestration with Human-in-the-Loop (HITL) capabilities for escalation.
*   **MCP (FastAPI):** A Model Context Protocol server exposing internal risk data securely (mocking legacy quantitative risk systems).
*   **RAG (pgvector):** Retrieval-Augmented Generation pipeline for querying Market Risk policies (SR 11-7).
*   **Guardrails (Presidio):** PII masking (e.g., account numbers, names) before data hits the LLM to ensure Responsible AI.
*   **Asyncio & Pandas:** High-throughput async batch processing of End-of-Day (EOD) incident logs.

*Note: For further internal architectural context, refer to the document named `AegisRisk_Project_Code_Execution.docx`.*

## Directory Structure

```text
AegisRisk/
├── mcp_server.py           # FastAPI MCP server for Tool Calling
├── guardrails.py           # PII Filtering & Input Validation
├── rag_pipeline.py         # pgvector RAG implementation
├── langgraph_agent.py      # Core agent orchestration
├── batch_processor.py      # Asyncio + Pandas for EOD logs
├── requirements.txt        # Dependencies
└── run_pipeline.sh         # Execution script
```

## End-to-End Execution Steps

Follow these instructions to set up the environment and execute the pipeline step-by-step.

### 1. Environment Setup
Create a virtual environment and install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn presidio-analyzer presidio-anonymizer langchain-openai langchain-community langgraph pandas psycopg2-binary pgvector
```

### 2. Database Setup (Docker)
Start the PostgreSQL database with the `pgvector` extension for the RAG pipeline:
```bash
docker run --name pgvector-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=risk_db -p 5432:5432 -d pgvector/pgvector:pg16
```

### 3. Start the MCP Server
In **Terminal 1**, start the FastAPI server to simulate internal banking APIs (VaR and Greeks calculation):
```bash
python mcp_server.py
```
*The server will run on `http://0.0.0.0:8000`, waiting for LLM tool calls.*

### 4. Test Guardrails
In **Terminal 2**, verify that the Presidio PII masking is correctly downloading models and anonymizing data:
```bash
python guardrails.py
```

### 5. Execute the Full Agentic Batch Pipeline
In **Terminal 2**, trigger the asyncio batch processor to run the End-of-Day logs through the entire AI orchestration pipeline:
```bash
python batch_processor.py
```
*This process will trigger asyncio tasks, route them through the LangGraph agent, apply PII Guardrails, fetch context via RAG, and ultimately output a Pandas-aggregated CSV report (`eod_risk_report.csv`).*