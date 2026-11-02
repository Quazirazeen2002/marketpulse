# MARKETPULSE Architecture Specification

## 1. System Overview

MARKETPULSE is an autonomous business intelligence and strategic decision engine that coordinates specialized autonomous agents orchestrated through LangGraph StateGraph. The system guarantees that every strategic finding, market assertion, and commercial opportunity is backed by verified empirical citations.

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 Chief Research Director                │
                  │              Model: Meta Muse Wonder (1.0)             │
                  └───────────────────────────┬────────────────────────────┘
                                              │ Strategic Planning & Task Dispatch
        ┌───────────────────┬─────────────────┼───────────────────┬───────────────────┐
        ▼                   ▼                 ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐ ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Market Intel  │   │Competitor     │ │ Customer Intel│   │Marketing Intel│   │Commercial     │
│ Analyst       │   │Intel Analyst  │ │ Analyst       │   │Analyst        │   │Intel Analyst  │
│ Spark 1.3     │   │ Spark 1.3     │ │ Spark 1.3     │   │ Spark 1.3     │   │ Spark 1.3     │
└───────┬───────┘   └───────┬───────┘ └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                 │                   │                   │
        └───────────────────┼─────────────────┴───────────────────┴───────────────────┘
                            ▼
        ┌────────────────────────────────────────────────────────┐
        │              Opportunity Discovery Analyst             │
        │              Model: Meta Spark 1.3 (spark-1.3)         │
        └───────────────────────────┬────────────────────────────┘
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │          Risk & Industry Intelligence Analyst          │
        │              Model: Meta Spark 1.3 (spark-1.3)         │
        └───────────────────────────┬────────────────────────────┘
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │       Autonomous Research-Gap & Hypothesis Engine      │
        │       - Gaps ➔ Hypotheses ➔ Follow-up Research Loop    │
        │       - Shared Bounded Tavily Search Budget            │
        └───────────────────────────┬────────────────────────────┘
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │       Deterministic Opportunity Scoring Engine         │
        │       - 6-Dimension Weighted Scoring (0-100)           │
        │       - Separate Risk-Adjusted Assessment              │
        └───────────────────────────┬────────────────────────────┘
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │             Business Scenario Simulator                │
        │             - Deterministic Python Financial Engine    │
        │             - Base, Best, Worst + 5D Sensitivity       │
        └───────────────────────────┬────────────────────────────┘
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │                 Chief Research Director                │
        │             Model: Meta Muse Wonder (1.0)              │
        │     Final Executive Report (Sections A through J)      │
        └───────────────────────────┬────────────────────────────┘
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │        FastAPI + SQLite Persistence (SQLModel)         │
        └────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Model Architecture & Strict Model Allocation

MARKETPULSE enforces strict separation between executive synthesis and factual research:

| Agent Role | Model Name | Provider | Core Responsibilities |
| :--- | :--- | :--- | :--- |
| **Research Director** | `muse-wonder-1.0` | Meta AI | Strategic research planning, question decomposition, contradiction resolution, hypothesis challenge, opportunity assessment, 10-section report synthesis. |
| **Market Intelligence Analyst** | `spark-1.3` | Meta AI | Industry trends, market sizing/CAGR verification, regulatory dynamics, emerging business models. |
| **Competitor Intelligence Analyst** | `spark-1.3` | Meta AI | Competitor mapping, product/pricing benchmarking, distribution channel analysis, competitive vulnerabilities. |
| **Customer Intelligence Analyst** | `spark-1.3` | Meta AI | Customer segmentation, purchasing motivation, customer complaints, unmet demand and pain points. |
| **Marketing Intelligence Analyst** | `spark-1.3` | Meta AI | Brand positioning, observable campaign rhythms, acquisition channels, marketing gap detection. |
| **Commercial Intelligence Analyst** | `spark-1.3` | Meta AI | Public pricing tiers, delivery fees, monetization models, subscription options, commercial feasibility. |
| **Opportunity Discovery Analyst** | `spark-1.3` | Meta AI | Autonomous identification of underserved segments, competitor blind spots, and structured business hypotheses. |
| **Risk & Industry Intelligence Analyst** | `spark-1.3` | Meta AI | Scrutiny of business risks (operational, financial, adoption, retaliation) and industry threats. |

### Model Gateway

Model resolution is handled centrally in [`app/models/gateway.py`](file:///Users/quazirazeenjubair/Desktop/projects/Deep-research/marketpulse/app/models/gateway.py):
- `get_director_model()`: Initialized with `META_MUSE_WONDER_MODEL` (`muse-wonder-1.0`).
- `get_specialist_model()`: Initialized with `META_SPARK_MODEL` (`spark-1.3`).
- `get_model_for_agent(agent_name)`: Enforces that Director strictly uses Muse Wonder and all 7 specialists strictly use Spark 1.3.

---

## 3. Web Intelligence & Shared Search Budget

The web search layer in [`app/services/web_search/`](file:///Users/quazirazeenjubair/Desktop/projects/Deep-research/marketpulse/app/services/web_search/) and [`app/services/hypothesis_engine/research_budget.py`](file:///Users/quazirazeenjubair/Desktop/projects/Deep-research/marketpulse/app/services/hypothesis_engine/research_budget.py) handles external intelligence gathering:
- **Tavily Client Wrapper**: Normalizes results with deterministic SHA-256 evidence IDs, publishers, excerpts, and timestamps.
- **Shared Budget Ceiling**: Enforced across Stage 1 and Stage 2 follow-up investigations (`MAX_RESEARCH_ITERATIONS=3`, `MAX_FOLLOWUP_SEARCHES=4`, `MAX_FOLLOWUP_TASKS=8`).
- **Dual-Tier Caching**:
  - `L1 In-Memory`: Sub-millisecond lookup and deduplication of repeated queries in the same research run.
  - `L2 SQLite`: `search_cache` table preserves cached search results across server restarts with a 24-hour TTL.

---

## 4. LangGraph Strategic Orchestration Workflow

The strategic workflow in [`app/graph/strategic_workflow.py`](file:///Users/quazirazeenjubair/Desktop/projects/Deep-research/marketpulse/app/graph/strategic_workflow.py) coordinates the following nodes:
1. `load_stage1_research`: Ingests verified Stage 1 findings, evidence IDs, claims, and contradictions.
2. `strategic_planning`: Research Director formulates strategic inquiry directives on Muse Wonder.
3. `parallel_specialists`: Executes Marketing, Commercial, Opportunity Discovery, and Risk Analysts on Spark 1.3.
4. `strategic_synthesis`: Director synthesizes reports, detects research gaps, and formulates testable hypotheses.
5. `should_execute_followup` (Conditional Routing): Directs to `followup_investigation` or `opportunity_scoring`.
6. `followup_investigation`: Bounded research loop executing targeted specialist investigations on under-investigated hypotheses.
7. `opportunity_scoring`: Deterministic 6-dimension scoring and risk adjustment.
8. `business_scenario_preparation`: Runs baseline financial modeling and unit economics.
9. `strategic_executive_report`: Research Director compiles the comprehensive 10-section intelligence dossier.
10. `persist_strategic_analysis`: Records all entities to SQLite with foreign-key referential integrity.

---

## 5. Deterministic Opportunity Scoring Engine

Implemented in [`app/services/opportunity_scoring/`](file:///Users/quazirazeenjubair/Desktop/projects/Deep-research/marketpulse/app/services/opportunity_scoring/):

$$\text{Raw Score} = (D \times 0.25) + (C_{\text{gap}} \times 0.20) + (C_{\text{attr}} \times 0.20) + (F \times 0.15) + (G \times 0.10) + (S \times 0.10)$$

Risk is evaluated separately and presented as a transparent risk penalty without artificially altering the raw opportunity score.

---

## 6. Business Scenario Simulator

Implemented in [`app/services/business_simulation/`](file:///Users/quazirazeenjubair/Desktop/projects/Deep-research/marketpulse/app/services/business_simulation/):
- **100% Deterministic Python Calculations**: Revenue, COGS, Gross Profit, Gross Margin %, Contribution Margin, Operating Profit, Break-Even orders/revenue, and Estimated Cash Requirement.
- **Scenario Comparison Suite**: Base Case, Best Case (+15% revenue / -10% costs), Worst Case (-20% revenue / +15% costs).
- **5-Dimension Sensitivity Analysis**: Price, Volume, Return Rate, Marketing Spend, Delivery Cost per Order.

---

## 7. Open-Source MCP Servers

Implemented in [`app/mcp_servers/`](file:///Users/quazirazeenjubair/Desktop/projects/Deep-research/marketpulse/app/mcp_servers/):
1. **Academic Intelligence Server**: OpenAlex, Crossref, and arXiv literature search.
2. **Document Intelligence Server**: Document and PDF extraction, metadata inspection, keyword search.
3. **Customer Intelligence Server**: Sentiment analysis, complaint extraction, pain point clustering.
4. **Business Analytics Server**: Unit economics, break-even analysis, contribution margins, scenario comparison.

---

## 8. Database Schema (`marketpulse.db`)

Preserves all 7 Stage 1 tables and introduces 13 Stage 2 tables:
- `strategic_analyses`
- `marketing_intelligence`
- `commercial_intelligence`
- `opportunity_records`
- `opportunity_evidence`
- `research_hypotheses`
- `followup_research_tasks`
- `risk_assessments`
- `opportunity_scores`
- `scenario_models`
- `scenario_inputs`
- `strategic_recommendations`
- `strategic_execution_events`
