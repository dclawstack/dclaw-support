---
tags: [meta, prd, revised, swarm]
version: 2.3
date: 2026-05-16
app_id: support
app_name: DClaw Support
category: Support
status: Future
---

# 📘 DClaw Support — Revised PRD v2.3

> **The single document every agent must read before writing code for this app.**
> Generated from DClaw Master PRD v2.2. Read the Master PRD first: https://raw.githubusercontent.com/dclawstack/dclaw-prd/main/DClaw-Master-PRD.md

---

## 1. Product Identity

| Field | Value |
|-------|-------|
| **App ID** | `support` |
| **Name** | DClaw Support |
| **Category** | Support |
| **Tagline** | Ticket resolution |
| **Color** | #3B82F6 |
| **Phase** | Future |
| **Port (Frontend Dev)** | 3012 (TBD — assign before build) |
| **Port (Backend Dev)** | 18082 (TBD — assign before build) |
| **Maturity Tier** | 🟢 Tier 1 — Mature |

---

## 2. Current State Assessment

### 2.1 Scaffold Status
| Component | Status | Notes |
|-----------|--------|-------|
| `frontend/` | ✅ | Next.js 14+ app |
| `backend/` | ✅ | FastAPI + SQLAlchemy 2.0 |
| `docs/` | ❌ | getting-started, guides, reference, releases |
| `helm/` | ✅ | K8s deployment manifests |
| `.github/workflows/` | ✅ | CI/CD + Claude integration |
| `AGENTS.md` | ✅ | Per-repo agent instructions |
| `PLAN-v1.2.md` | ✅ | Feature roadmap |
| `docker-compose.yml` | ✅ | Local dev stack |
| `tests/` | ✅ | pytest + pytest-asyncio |
| `alembic/` | ✅ | Database migrations |
| `dclaw-manifest.json` | ❌ | DPanel registration |

### 2.2 Code Maturity
| Metric | Value |
|--------|-------|
| Python source files (backend) | ~1832 |
| TypeScript/TSX files (frontend) | ~19 |
| Total source files | ~1851 |
| Tests | ✅ Present |
| Alembic migrations | ✅ Present |
| DPanel manifest | ❌ Missing |

### 2.3 Feature Maturity
- **P0 Foundation:** Partially implemented
- **P1 Platform:** Not yet started
- **P2 Vertical:** Not yet started

---

## 3. Gap Analysis

| # | Gap | Severity | Fix |
|---|-----|----------|-----|
| 1 | Missing `docs/` directory | 🟡 | Create docs/ with getting-started, guides, reference, releases |
| 2 | Missing `dclaw-manifest.json` | 🔴 | Create frontend/public/dclaw-manifest.json for DPanel |

---

## 4. Sacred Architecture & Tech Stack

> **NON-NEGOTIABLE. Every DClaw product MUST use this exact stack.**

| Layer | Technology | Version |
|-------|------------|---------|
| **Frontend** | Next.js 14+ | App Router, Tailwind CSS, shadcn/ui |
| **Backend** | FastAPI | Pydantic v2, SQLAlchemy 2.0, asyncpg |
| **Database** | PostgreSQL 16 | CloudNativePG operator in K8s |
| **Vector DB** | Qdrant / pgvector | Only if RAG / semantic search |
| **Cache / Bus** | Redis | 7.x |
| **Object Storage** | MinIO | Latest |
| **Workflow** | Temporal.io | Only if automation/orchestration |
| **Auth** | Logto | JWT validation on all protected routes |
| **Billing** | Stripe | Metered or per-seat |
| **K8s Operator** | Go + controller-runtime | 0.18 |
| **LLM Local** | Ollama | Apple Silicon |
| **LLM Cloud** | OpenRouter + Kimi K2.5 | Fallback |
| **Monitoring** | Prometheus + Grafana | Latest |

### 4.1 Python Rules
- `ruff` formatting enforced
- Type hints on ALL public APIs
- `pydantic` v2 for schemas
- `sqlalchemy` 2.0 style (`Mapped`, `mapped_column`)
- `pytest` + `pytest-asyncio` for tests
- Functions < 50 lines
- No `print()` — use `structlog`

### 4.2 TypeScript / Next.js Rules
- Strict TypeScript (`strict: true`)
- Tailwind for ALL styling
- `cn()` utility for conditional classes
- No `any` without `// @ts-ignore`

### 4.3 Docker Standards
- Port mappings MUST match container listen port
- Healthchecks MUST use binaries present in base image
- `docker compose config` must pass before shipping
- Service type MUST be `ClusterIP`
- TLS required on all ingress

---

## 5. P0 Foundation Features (Must Have — Demo Ready)

> **Every P0 MUST include an AI Copilot per YC S25/W26 RFS.**

| # | Feature | Description | AI Component | Acceptance Criteria |
|---|---------|-------------|--------------|---------------------|
| P0.1 | **AI Support Copilot** | Auto-suggest solutions, draft responses, and escalate smartly. | RAG over knowledge base + LLM response generation | Suggest answer in <3s; resolve 40% without human touch |
| P0.2 | **Ticket Management** | Create, route, and track support tickets across channels. | AI routing + priority-scoring + sentiment analysis | Route to correct team in <1s; auto-prioritize; detect urgency |
| P0.3 | **Knowledge Base** | Self-service articles with AI-powered search and generation. | AI article-generation from tickets + semantic search | Generate article from 10 tickets; search 1K articles in <1s |
| P0.4 | **Live Chat** | Real-time chat with AI co-pilot for agents. | AI response suggestion + macro recommendation | Sub-second response time; suggest 3 replies; auto-translate |

---

## 6. P1 Platform Features (Should Have — v1.1–1.2)

| # | Feature | Description | AI Component | Acceptance Criteria |
|---|---------|-------------|--------------|---------------------|
| P1.1 | **SLA Management** | Track and enforce SLA compliance with predictive alerts. | AI SLA-breach prediction + escalation recommendation | Track 10 SLA types; predict breach 2hrs ahead; auto-escalate |
| P1.2 | **Customer Satisfaction** | Collect and analyze CSAT, NPS, and CES scores. | AI sentiment analysis + driver identification | Auto-send surveys; analyze 1000 responses; identify top 3 drivers |
| P1.3 | **Agent Performance** | Score and coach support agents with AI insights. | AI performance-scoring + coaching-moment detection | Track 15 metrics; identify 3 coaching opportunities per agent |
| P1.4 | **Integration with Products** | Link tickets to bugs, features, and releases. | AI ticket-to-issue mapping + duplicate detection | Auto-link to Jira; suggest related issues; track fix status |

---

## 7. P2 Vertical / Scale Features (Could Have — v1.3+)

| # | Feature | Description | AI Component | Acceptance Criteria |
|---|---------|-------------|--------------|---------------------|
| P2.1 | **Proactive Support** | Identify at-risk customers before they contact support. | AI churn-risk prediction + proactive-outreach suggestion | Predict churn >75% accuracy; auto-create outreach task |
| P2.2 | **Video Support** | Screen sharing and video calls for complex issues. | AI session-summary + solution-documentation | One-click video; co-browse; auto-generate case notes |
| P2.3 | **Community Forum** | Customer community with AI-powered moderation and answers. | AI moderation + auto-answer + expert-routing | Auto-answer 30% of posts; flag spam; route to experts |
| P2.4 | **Multi-Language Support** | Auto-translate tickets and responses for global teams. | AI translation + cultural-adaptation | Support 30 languages; preserve technical terms; localize tone |

---

## 8. Scaffold Checklist

Before marking this app "shipped", confirm:

- [ ] `frontend/` with Next.js 14+, Tailwind, shadcn/ui
- [ ] `backend/` with FastAPI, Pydantic v2, SQLAlchemy 2.0, asyncpg
- [ ] `docs/` with getting-started, guides, reference, releases, troubleshooting
- [ ] `helm/` with Chart.yaml, values.yaml, templates (deployment, service, ingress, cloudnativepg)
- [ ] `.github/workflows/` with build-backend.yml, build-frontend.yml, deploy.yml, claude.yml
- [ ] `frontend/public/dclaw-manifest.json` for DPanel registration
- [ ] `backend/tests/` with pytest + pytest-asyncio
- [ ] `backend/alembic/` with initial migration
- [ ] `Dockerfile` + `docker-compose.yml` with correct healthchecks
- [ ] Health endpoint at `/health` returning `{"status":"ok"}`
- [ ] `AGENTS.md` with per-repo instructions
- [ ] `PLAN-v1.2.md` with feature roadmap
- [ ] Port assigned from registry and documented
- [ ] No hardcoded secrets — use `.env.example` + K8s Secrets
- [ ] Non-root containers in Dockerfile

---

## 9. AI Copilot Mandate (YC S25/W26 Requirement)

Every DClaw app MUST have an AI Copilot as its first P0 feature. The copilot must:
1. Be contextually aware of the app's domain data
2. Use RAG over the app's knowledge base where applicable
3. Suggest next actions, not just answer questions
4. Be accessible from every page via floating chat or sidebar
5. Fall back to local Ollama when cloud is unavailable

---

## 10. Next Tasks for Vibe Coders

1. **Audit current state**: Verify all P0 features are complete and documented.
2. **Implement P1 features**: Build the 4 P1 features to reach v1.1 platform readiness.
3. **Add advanced features**: Begin P2 features for competitive differentiation.
4. **Optimize and scale**: Improve test coverage, add performance monitoring, and refine UX.

---

## 11. Domain Research Notes

Inspired by Zendesk, Intercom, Freshdesk, Kustomer. Support AI reduces cost-per-ticket by 50%+.

---

## 12. Links & Resources

| Resource | URL |
|----------|-----|
| **Master PRD** | https://raw.githubusercontent.com/dclawstack/dclaw-prd/main/DClaw-Master-PRD.md |
| **GitHub Org** | https://github.com/dclawstack |
| **DPanel** | https://dpanel.dclawstack.io |
| **Port Registry** | See `dclaw-platform/PORT_REGISTRY.md` |
| **App PRD Template** | Obsidian Vault → `00-META/📐 App PRD Template.md` |
| **Scaffold Source** | `dclaw-scaffold/` in DClaw-Stack |

---

*Revised PRD version: 2.3*
*Generated: 2026-05-16 by DClaw Stack Generator*
*Next review: When P0 features are complete or architecture changes*
