# Home Buyer Intelligence Engine

An AI-powered document analysis and bidding advisor for Dutch home buyers. Upload property documents (purchase agreements, inspection reports, energy labels, HOA documents) and get structured risk assessments, market intelligence, and data-driven bidding strategies.

---

## Features

- **Document Analysis** — Upload PDFs and let Gemini AI extract structured property data, identify risks, and surface strengths/weaknesses
- **Risk Scoring** — Multi-category risk assessment (structural, legal, financial, market) with severity levels and an overall 0–100 score
- **Market Intelligence** — Enriches analysis with real Dutch data sources: BAG (cadastral register), EP Online (energy labels), and CBS StatLine (market statistics)
- **Bidding Strategy** — Three context-aware bidding approaches (Conservative, Competitive, Aggressive) with price adjustments based on risk and market conditions
- **GDPR Compliance** — Session-scoped data isolation, right-to-erasure endpoint, and data portability export
- **Audit Logging** — All actions logged with timestamps, IPs, and resource references

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite, TanStack Query, Recharts, Tailwind CSS |
| Backend | Python 3.11, FastAPI, SQLAlchemy (async), Pydantic v2, Alembic |
| AI | Google Gemini 2.0 Flash via `google-genai` |
| PDF | pdfplumber, PyMuPDF |
| Database | SQLite (dev) / PostgreSQL 16 (prod) |
| Storage | Local filesystem (dev) / Azure Blob Storage (prod) |
| Monorepo | NX, pnpm workspaces |
| Infra | Docker Compose, Azurite (Azure Storage emulator) |

---

## Project Structure

```
home-buyer-intelligence-claude/
├── apps/
│   ├── backend/                  # Python FastAPI application
│   │   ├── src/
│   │   │   ├── main.py           # App entrypoint
│   │   │   ├── config.py         # Settings (env vars via Pydantic)
│   │   │   ├── api/v1/           # HTTP endpoints (documents, analysis, market, gdpr)
│   │   │   ├── application/      # Services & DTOs (business logic)
│   │   │   ├── domain/           # Models, enums, interfaces
│   │   │   └── infrastructure/   # DB, AI gateway, external APIs, storage, PDF
│   │   ├── alembic/              # Database migrations
│   │   ├── tests/
│   │   └── pyproject.toml
│   │
│   └── frontend/                 # React + TypeScript application
│       └── src/
│           ├── pages/            # HomePage, UploadPage, AnalysisPage, PrivacyPage
│           ├── components/       # upload/, analysis/, bidding/, market/, layout/
│           ├── hooks/            # useAnalysis (React Query hooks)
│           ├── api/client.ts     # Fetch wrapper
│           └── types/
│
├── libs/shared-types/            # Shared TypeScript type definitions
├── infra/scripts/                # DB migration & type generation scripts
├── docker-compose.yml            # PostgreSQL + Azurite for local dev
├── nx.json
├── package.json
└── pyproject.toml
```

---

## Prerequisites

- **Node.js** 18+ with [pnpm](https://pnpm.io/)
- **Python** 3.11+
- **uv** — Python package manager (`pip install uv`)
- **Docker & Docker Compose** (optional, for PostgreSQL/Azurite)

---

## Getting Started

### 1. Clone and install dependencies

```bash
git clone https://github.com/your-username/home-buyer-intelligence-claude.git
cd home-buyer-intelligence-claude

# Install Node dependencies (frontend + NX)
pnpm install

# Install Python dependencies
cd apps/backend && uv sync && cd ../..
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your API keys (see [Environment Variables](#environment-variables)).

### 3. Start infrastructure (optional)

```bash
# Starts PostgreSQL and Azurite (Azure Storage emulator)
docker-compose up -d
```

Skip this step to use SQLite and local file storage (default for development).

### 4. Run database migrations

```bash
cd apps/backend
uv run alembic upgrade head
cd ../..
```

### 5. Start the development servers

```bash
# Frontend — http://localhost:5173
pnpm dev:frontend

# Backend — http://localhost:8000
pnpm dev:backend
```

API documentation is available at `http://localhost:8000/docs`.

---

## Environment Variables

Create a `.env` file in the project root:

```env
# Required
GOOGLE_API_KEY=your-gemini-api-key

# Database (defaults to SQLite for local dev)
DATABASE_URL=sqlite+aiosqlite:///./data/app.db
# PostgreSQL: postgresql+asyncpg://user:password@localhost/homebuyer

# Document storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=25
MAX_SESSION_SIZE_MB=100

# External APIs (optional, enriches analysis)
EP_ONLINE_API_KEY=your-ep-online-api-key

# CORS
CORS_ORIGINS=http://localhost:5173

# Session
SESSION_SECRET=change-me-in-production

# Environment
ENVIRONMENT=development
```

Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).

---

## API Reference

All endpoints are prefixed with `/api/v1`.

### Sessions
| Method | Path | Description |
|---|---|---|
| `POST` | `/sessions` | Create a new analysis session |
| `GET` | `/sessions/{id}` | Get session details |
| `DELETE` | `/sessions/{id}` | Delete session and all data (GDPR erasure) |
| `GET` | `/sessions/{id}/export` | Export all session data as JSON (GDPR portability) |

### Documents
| Method | Path | Description |
|---|---|---|
| `POST` | `/sessions/{id}/documents` | Upload a PDF document (max 25 MB) |
| `GET` | `/sessions/{id}/documents` | List documents in session |
| `GET` | `/sessions/{id}/documents/{doc_id}` | Download a document |
| `DELETE` | `/sessions/{id}/documents/{doc_id}` | Delete a document |

### Analysis
| Method | Path | Description |
|---|---|---|
| `POST` | `/sessions/{id}/analyze` | Trigger background analysis (returns `202`) |
| `GET` | `/sessions/{id}/analysis/status` | Poll analysis progress |
| `GET` | `/sessions/{id}/analysis` | Retrieve complete results |

### Market Data
| Method | Path | Description |
|---|---|---|
| `GET` | `/sessions/{id}/market` | Get market intelligence for the property |

### Health
| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Service health check |

---

## Analysis Pipeline

When analysis is triggered, the backend runs a multi-stage background pipeline:

```
Upload PDFs
    ↓
Text Extraction + PII Redaction
    ↓
Gemini AI Analysis
  • Document classification
  • Property data extraction
  • Risk detection (structural / legal / financial / market)
  • Strengths & weaknesses
    ↓
Market Intelligence Enrichment
  • BAG (Dutch cadastral register) lookup
  • EP Online energy label data
  • CBS StatLine market statistics
    ↓
Risk Re-scoring (market-adjusted)
    ↓
Bidding Strategy Generation
  • Conservative | Competitive | Aggressive
```

The frontend polls `/analysis/status` every 2 seconds until `status: complete`.

---

## Development Scripts

```bash
pnpm dev:frontend       # Start Vite dev server
pnpm dev:backend        # Start uvicorn with hot reload
pnpm build:frontend     # Production build
pnpm lint               # Lint all projects
pnpm generate:types     # Generate TypeScript types from Python models
```

### Backend-specific

```bash
cd apps/backend

uv run alembic upgrade head     # Apply all migrations
uv run alembic downgrade -1     # Roll back one migration
uv run pytest                   # Run tests
uv run ruff check .             # Lint Python code
```

---

## Supported Document Types

| Type | Description |
|---|---|
| Purchase Agreement | _Koopovereenkomst_ |
| Energy Label | _Energielabel_ |
| Inspection Report | _Bouwkundig rapport_ |
| HOA Documents | _VvE documenten_ |
| Property Listing | _Verkoopbrochure_ |
| Other | Catch-all for additional documents |

---

## License

MIT
