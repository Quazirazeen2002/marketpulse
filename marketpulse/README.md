# MARKETPULSE — Autonomous Strategic Business Intelligence & Opportunity Discovery

MARKETPULSE is an autonomous business research and strategic intelligence platform. It coordinates specialized autonomous agents orchestrated through LangGraph StateGraph to investigate industries, competitors, marketing strategies, and commercial monetization, autonomously discovering unexploited commercial opportunities with empirical evidence provenance.

---

## Architecture Overview

MARKETPULSE operates across two seamlessly integrated stages:

- **Stage 1 (Deep Research Engine)**: Investigates *what is happening*, *who the competitors are*, *what customers want*, and *what verified evidence exists*.
- **Stage 2 (Strategic Intelligence & Opportunity Discovery)**: Analyzes *why competitors succeed or fail*, *what they miss*, *which customer needs are underserved*, *which business opportunities exist*, *how commercially viable they are*, and *what financial scenarios/risks govern success*.

---

## Multi-Agent Architecture & Strict Model Allocation

MARKETPULSE features **eight specialized agents** with rigid model allocations:

1. **Chief Research Director**: **Meta Muse Wonder (`muse-wonder-1.0`)**
   - **Role**: Executive strategy, research objective decomposition, cross-agent evidence audit, contradiction resolution, hypothesis validation, opportunity assessment, and 10-section strategic executive report generation.
   - **Mandate**: Exclusively uses Muse Wonder. Never assigned to Spark 1.3.

2. **Specialist Agents (7 Total)**: **Meta Spark 1.3 (`spark-1.3`)**
   - **Market Intelligence Analyst**: Industry structure, CAGR, macro trends, regulatory/economic factors.
   - **Competitor Intelligence Analyst**: Competitor matrix, positioning, pricing, distribution, operational vulnerabilities.
   - **Customer Intelligence Analyst**: Customer segmentation, purchase drivers, friction points, recurring complaints, unmet needs.
   - **Marketing Intelligence Analyst**: Brand positioning, observable campaign rhythms, acquisition channels, marketing gap detection.
   - **Commercial Intelligence Analyst**: Public pricing tiers, delivery fees, monetization models, subscription options, commercial feasibility.
   - **Opportunity Discovery Analyst**: Autonomous identification of underserved segments, competitor blind spots, and structured business hypotheses.
   - **Risk & Industry Intelligence Analyst**: Scrutiny of business risks (operational, financial, adoption, retaliation) and industry threats.
   - **Mandate**: Exclusively use Spark 1.3. Never silently switch models.

### Central Model Factory (`app/models/gateway.py`)
All model access routes through `get_model_for_agent()`, enforcing strict separation between the Director and Specialists.

---

## Stage 2 Core Engines

### 1. Autonomous Hypothesis & Research-Gap Discovery Engine (`app/services/hypothesis_engine/`)
- Scans multi-agent findings, claims, and contradictions to detect missing commercial data and unverified assertions.
- Formulates falsifiable business hypotheses (`PROPOSED ➔ INVESTIGATING ➔ SUPPORTED / REJECTED`).
- Executes bounded autonomous research loops (`MAX_RESEARCH_ITERATIONS=3`, `MAX_FOLLOWUP_SEARCHES=4`, `MAX_FOLLOWUP_TASKS=8`).
- Enforces a shared Tavily search budget with dual-tier cache query deduplication.

### 2. Deterministic Opportunity Scoring Engine (`app/services/opportunity_scoring/`)
- Deterministic 6-dimension scoring formula:
  $$\text{Raw Score} = (D \times 0.25) + (C_{\text{gap}} \times 0.20) + (C_{\text{attr}} \times 0.20) + (F \times 0.15) + (G \times 0.10) + (S \times 0.10)$$
- Risk-adjusted assessments computed and presented independently without altering raw scores.

### 3. Business Scenario Simulator (`app/services/business_simulation/`)
- Deterministic Python financial arithmetic (zero LLM arithmetic).
- Calculates Net Revenue, COGS, Gross Margin, Contribution Margin, Operating Profit, Break-Even volume/revenue, and Estimated Cash Requirements.
- Generates Base, Best (+15% rev / -10% cost), and Worst (-20% rev / +15% cost) scenarios.
- 5-Dimension Sensitivity Analysis: Selling Price, Order Volume, Return Rate, Marketing Spend, Delivery Cost per Order.

### 4. MCP Server Architecture (`app/mcp_servers/`)
- **Academic Intelligence Server**: OpenAlex, Crossref, and arXiv literature retrieval.
- **Document Intelligence Server**: Document and PDF extraction, metadata inspection, and content search.
- **Customer Intelligence Server**: Review sentiment analysis, complaint extraction, and pain point clustering.
- **Business Analytics Server**: Unit economics, break-even analysis, contribution margins, and scenario comparison.

---

## Web Intelligence & Search Architecture

MARKETPULSE uses **Tavily Search API** (`tavily-python`) for targeted web retrieval:
- **Search Budget Ceiling**: Configurable run-level limit enforced across all concurrent specialist agents.
- **Dual-Tier Caching**:
  - **L1 In-Memory Cache**: Zero-latency deduplication within and across runs.
  - **L2 SQLite Cache**: Persistent storage with configurable 24-hour TTL (`search_cache` table).
- **Exact Excerpt Provenance**: Full-text acquisition via Trafilatura and PyMuPDF with atomic evidence IDs.

---

## Technology Stack

- **Frontend (Stage 3 Complete)**: Next.js 16 (App Router), React 19, TypeScript 5, Tailwind CSS 4, Framer Motion, Lucide React, Recharts, React Hook Form, Zod (Zero Jinja2, Zero Gradio).
- **Backend (Authoritative Core)**: FastAPI, LangGraph StateGraph, SQLModel, SQLite (`marketpulse.db`).
- **AI Models**: Meta AI Gateway (`muse-wonder-1.0` exclusively for Director, `spark-1.3` for all 7 Specialists).
- **Web Search**: Tavily Search API (`tavily-python`) with search budget ceilings & dual-tier L1/L2 caching.
- **MCP Servers**: Python MCP SDK JSON-RPC 2.0 (Academic, Document, Customer, Business Analytics).
- **Extraction**: Trafilatura, BeautifulSoup4, PyMuPDF (`fitz`).
- **Deduplication**: RapidFuzz Token-Set Clustering.

---

## Stage 3 Architecture & Routes

### 1. Public Marketing Website (`/app/(marketing)/`)
- `/` — High-impact Feastables-inspired landing page with 11 custom sections, oversized typography, and interactive agent fleet diagram.
- `/product` — Complete 6-pillar autonomous research product walkthrough and capability matrix.
- `/how-it-works` — Deep dive into Stage 1 evidence gathering, Stage 2 strategic intelligence, and LangGraph multi-agent orchestration.
- `/use-cases` — 6 enterprise intelligence scenarios (Fashion E-commerce, Telecom, Food Delivery, Retail, Manufacturing, Tech/Healthcare).
- `/about` — Origin, philosophy ("Evidence Before Opinion"), and core principles.
- `/contact` — Enterprise strategic consultation request form.

### 2. Application Workspace (`/app/(workspace)/app/`)
- `/app` — Intelligence Command Center with real-time KPI metrics, research volume charts, and recent dossiers.
- `/app/research/new` — Guided research investigation submission form with industry preset templates and depth selector.
- `/app/research/[id]` — Live research execution workspace with SSE event streaming, agent state audit, and live output feed.
- `/app/agents` — Autonomous Fleet Observatory with all 8 agents (Research Director + 7 Specialists) and structured inspection dossiers.
- `/app/intelligence` — Intelligence Domain Hub linking to Market, Competitor, Customer, Marketing, and Commercial modules.
- `/app/opportunities` & `/app/opportunities/[id]` — Scored commercial opportunities with raw vs. risk-adjusted scores and simulator links.
- `/app/hypotheses` — Autonomous hypothesis lifecycle pipeline (`PROPOSED ➔ INVESTIGATING ➔ SUPPORTED ➔ REJECTED`).
- `/app/risks` — Interactive 5x5 Likelihood vs. Impact Risk Matrix and systemic category breakdown.
- `/app/evidence` — Provenance database with Evidence Cards, Primary Sources table, and Claim Audits.
- `/app/reports` & `/app/reports/[id]` — Editorial executive report canvas with Table of Contents, citation popovers, and Markdown/JSON/PDF exports.
- `/app/simulator` — Interactive financial scenario simulator powered strictly by FastAPI's deterministic Python engine (Base/Best/Worst & 5D Sensitivity).
- `/app/history` — Research run archive and side-by-side run comparator.
- `/app/settings` — Diagnostic health monitors for FastAPI, SQLite, Meta AI models, and Tavily.

---

## Launch & Running Locally

### 1. Launch FastAPI Backend
```bash
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
- **Backend API Gateway**: `http://127.0.0.1:8000`
- **Interactive OpenAPI Docs**: `http://127.0.0.1:8000/docs`

### 2. Launch Next.js Frontend
```bash
cd frontend
npm install
npm run build
npm run start
```
- **Web Application**: `http://localhost:3000`

---

## Automated Verification & Testing

### Backend Regression Tests (Pytest)
```bash
source .venv/bin/activate
pytest tests/ -v
# 111 passed, 1 skipped in 20.87s
```

### Frontend End-to-End Tests (Playwright)
```bash
cd frontend
npx playwright test
# 13 passed in 2.2s
```



