---
name: project-medsimplify-context
description: "Full context for the MedSimplify project — goals, decisions made, files created, and where the user left off as of 2026-08-18."
metadata: 
  node_type: memory
  type: project
  originSessionId: 7379ecf0-1dd8-4c3e-994f-6a6fefa9688a
  modified: 2026-08-18T21:21:48.656Z
---

# MedSimplify Project Context

**Project goal:** Build a medical explanation tool — users paste sanitized medical reports or describe symptoms, and the app explains them in plain English. Similar to WebMD but runs locally.

**Why:** User wants to simplify patient reports into plain language and provide symptom guidance. Educational use, not clinical diagnosis.

## Key Decisions Made (as of 2026-08-18)

### Decision 1: Two-track architecture
- **v1 plan (PROJECT_RECOMMENDATION_SUMMARY.md):** Cloud-based, paid APIs — Azure OpenAI GPT-4.1 Mini + RAG over MedlinePlus/PubMed. HIPAA-compliant via BAA.
- **v2 plan (PROJECT_RECOMMENDATION_SUMMARY_v2.md):** Local standalone app, open-source only, zero ongoing cost. This is the active direction.

### Decision 2: Open-source local stack chosen (v2)
User explicitly chose:
1. Open-source models only
2. Standalone local app (nothing leaves the machine)
3. Easiest/fastest/cheapest to build
4. Feasibility of explanation > clinical accuracy
5. User volunteers sanitized data — PHI stripping is a separate component the user will build themselves

**Why:** Reduces HIPAA risk (no data leaves machine), zero API cost, simpler architecture.

## Recommended Stack (v2 — the active plan)

| Component | Choice |
|---|---|
| Model runner | **Ollama** (localhost:11434) |
| Model (primary) | **MedGemma 4B** — Google open weights, medical-specific |
| Model (fallback) | **Llama 3.2 8B** — if MedGemma too slow on hardware |
| UI | **Streamlit** (~50 lines Python) — custom form with system prompt |
| Alt UI (zero code) | **Open WebUI** via Docker — ChatGPT-like, no coding needed |
| Cost | $0 ongoing |

**Time to build:** ~30–40 minutes (mostly model download).

## Files Created

| File | Purpose |
|---|---|
| `1_research.md` | Original research brief |
| `instructions.md` | Standing behavior instructions (cite sources, HIPAA warnings, don't assume) |
| `PROJECT_RECOMMENDATION_SUMMARY.md` | Cloud/paid path — GPT-4.1 Mini + RAG + Azure OpenAI |
| `PROJECT_RECOMMENDATION_SUMMARY_v2.md` | **Active plan** — Open source, local, Ollama + MedGemma + Streamlit |

## Ready-to-Use Code

A working `app.py` Streamlit snippet is documented inside `PROJECT_RECOMMENDATION_SUMMARY_v2.md`.
Steps to run: install Ollama → `ollama pull medgemma3:4b` → `pip install streamlit requests` → `streamlit run app.py`.

## What Is NOT Done Yet

- No code written to the project directory yet (only planning docs exist)
- Sanitization component: user will build this separately — it strips PHI before any LLM call
- Source citation / RAG: not in scope for v1; local models have no internet access
- UI has not been started yet

## Key Benchmarks Researched (for reference)

- GPT-5: 95.84% MedQA, HealthBench 88.0 (best paid)
- Gemini 3.1 Pro: 97.4% MedQA (highest raw score)
- Claude Sonnet 5: 5% unsafe response rate (safest outputs)
- MedGemma 4B: ~70–75% MedQA — acceptable given explanation-over-accuracy goal
- BioMistral 7B / MedAlpaca 13B: 44–60% — do NOT use, below safe threshold

## Important Standing Instructions (from instructions.md)

- Always cite sources
- Include reasoning
- HIPAA compliance warnings where relevant
- Be explicit when uncertain
- Do not assume or guess — ask user to clarify

**Why:** [[feedback-instructions]] — user set these as standing behavior rules in instructions.md.

## Memory Location

Memory files for this project live at:
```
C:\LEARNING\MedSimplify\.claude\memory\
```
At the start of every new session, read `MEMORY.md` and this file from that path to restore full context without the user needing to repeat it.
