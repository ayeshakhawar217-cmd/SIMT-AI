<div align="center">

# SIMT AI

### Intelligent Opportunity Matching for Pakistan

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Supabase](https://img.shields.io/badge/Supabase-Auth%20%26%20DB-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](#license)

*The government has programs. Citizens have needs. The missing layer is intelligent matching.*

</div>

---

## Overview

SIMT AI is an intelligent opportunity-matching platform that connects people in Pakistan with scholarships, jobs, training programs, business support, loans, grants, and other opportunities relevant to their circumstances. Instead of searching across scattered platforms and figuring out eligibility program by program, users simply describe their situation in plain language, and SIMT AI understands their needs, builds a structured profile, checks eligibility, and uses semantic AI to surface and rank the opportunities that are the best fit.

<div align="center">

<img src="docs/architecture.png" alt="SIMT AI Architecture" width="900">

</div>

## How It Works

```
User describes their situation
              │
              ▼
     AI Profile Extraction
              │
              ▼
    Structured User Profile
              │
              ▼
    Deterministic Eligibility
              │
              ▼
      Semantic RAG Search
              │
              ▼
        Hybrid Ranking
              │
              ▼
     Top Opportunity Matches
```

**Example input:**

> "I'm 21, unemployed, from Punjab, and I want to start an online clothing business. I need around 12 lakh rupees."

SIMT AI extracts attributes such as age, location, employment status, business goal, sector, and funding requirement, then matches them against eligible programs.

## Key Features

| Feature | Description |
|---|---|
| Natural-language input | Conversational, no forms to fill |
| AI profile extraction | Structures unstructured user descriptions |
| Deterministic eligibility | Rule-based filtering for accuracy |
| Semantic RAG search | Understands relevance beyond keywords |
| Hybrid ranking | Combines eligibility and relevance scores |
| API access | FastAPI backend with interactive Swagger docs |

## Tech Stack

**Frontend** — React · Vite · Supabase Auth
**Backend** — Python · FastAPI · Pydantic · Groq LLM
**AI / Matching** — LLM-based profile extraction · Sentence Transformers embeddings · PostgreSQL + pgvector · Deterministic eligibility engine
**Deployment** — Vercel (frontend) · Render (backend)

## Project Structure

```
SIMT-AI/
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RAG.md
│   ├── ELIGIBILITY.md
│   ├── AI_PIPELINE.md
│   ├── DEPLOYMENT.md
│   └── API.md
│
├── simt-backend/
│   ├── main.py
│   ├── eligibility.py
│   ├── extract_profile.py
│   ├── rag.py
│   ├── seed_rag.py
│   ├── programs.json
│   └── requirements.txt
│
└── simt-frontend/
    ├── src/
    ├── package.json
    └── ...
```


## Why SIMT AI

Opportunity discovery today is fragmented across government portals, universities, NGOs, banks, and individual program websites. SIMT AI is not another directory — it is the intelligence layer that connects people to the opportunities they already qualify for.

**Understand the person → determine eligibility → understand relevance → rank the opportunities.**

---

<div align="center">

Built for a mid-program hackathon submission.

</div>