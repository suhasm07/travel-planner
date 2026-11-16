# Multi-Agent Travel Planner

![CI](https://github.com/suhasm07/travel-planner/actions/workflows/ci.yml/badge.svg)

A multi-agent system that turns a free-text trip request into a complete itinerary, using specialized agents for flights, stays, activities, and budget checking, coordinated by a supervisor.

> **Status:** Early development (Stage 1: foundations).

## What it does

Given a request like:

> "week in tokyo mid-april, 2 of us, around 3k, we love ramen and temples"

the system will return flights, stays, a day-by-day activity plan, and a budget breakdown.

## Tech stack

- Python 3.13, managed with [uv](https://docs.astral.sh/uv/)
- Pydantic v2 for typed schemas
- Gemini API (free tier) via `google-genai`
- Ruff, pytest, pre-commit
- Planned: LangGraph, FastAPI, Streamlit, Docker

## Quickstart

```bash
git clone https://github.com/suhasm07/travel-planner.git
cd travel-planner
uv sync
cp .env.example .env   # then add your GEMINI_API_KEY
uv run pytest
```

## Project status

- [ ] Stage 1: Foundations (schemas, LLM parser, parse eval)
- [ ] Stage 2: Tools and single agents
- [ ] Stage 3: Multi-agent orchestration
- [ ] Stage 4: Critic / revision loop
- [ ] Stage 5: Evaluation and observability
- [ ] Stage 6: Frontend
- [ ] Stage 7: Deployment

## Design decisions

- **Model name is configuration, not code.** The Gemini model is set via the `GEMINI_MODEL` environment variable, because model names get retired often.

## Limitations

- Work in progress; most features are not built yet.
