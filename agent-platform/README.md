# Agent Platform for Glue Job Terraform Generation

A chat-first LangGraph-powered agent system for creating, validating, and deploying AWS Glue (Talaria) ingestion job Terraform configurations into a Lakehouse (Iceberg).

## Quick Start

- **Backend**: `backend/` (FastAPI + LangGraph + PostgreSQL)
- **Frontend**: `frontend/` (React + Vite + TypeScript + Redux)
- **Documentation**: See `docs/ARCHITECTURE.md` for frozen architecture reference

## Architecture Overview

This project is designed per frozen architecture specifications (Steps 1-8):

- **Orchestration**: LangGraph-first agent system
- **API**: Single primary endpoint: `POST /agent/message` (conversational)
- **Database**: PostgreSQL (users, sessions, drafts, changes, snapshots)
- **Cache**: Redis (session state, ephemeral context)
- **Auth**: GitHub OAuth

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed specifications.

## Project Structure

```
agent-platform/
├── frontend/          # React + Vite + TypeScript
├── backend/           # FastAPI + LangGraph
├── docs/              # Frozen architecture specifications
├── infra/             # Infrastructure decisions
├── tests/             # Integration test harness
└── scripts/           # Developer utilities
```

## Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Redis 6+

### Backend Setup

```bash
cd backend
pip install -r requirements.txt  # or use pyproject.toml
```

### Frontend Setup

```bash
cd frontend
npm install
```

## Documentation

- **Frozen Architecture**: See `docs/ARCHITECTURE.md`
- **Implementation Plan**: See frozen Step-7 and Step-8 specifications
- **Development Workflow**: See `CONTRIBUTING.md` (when available)

## Status

- **Architecture**: LOCKED (Steps 1-8 frozen)
- **Database Design**: LOCKED
- **Project Structure**: LOCKED
- **Implementation**: Beginning Phase 1 (bootstrap)

## License

(To be determined)
