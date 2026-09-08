# MedSimplify v2 — Local Standalone App Recommendation

> **Scope:** Open-source only. Local app. No cloud APIs. User pastes sanitized report → gets plain-language explanation. Feasibility and speed-to-build matter more than clinical accuracy.
> **Instructions applied:** Sources cited, reasoning shown, HIPAA notes included where relevant.

---

## HIPAA Note (Abbreviated for This Scope)

Since:
- Data is sanitized before it reaches the LLM (your separate component)
- The model runs 100% locally (nothing leaves your machine)
- No PHI is transmitted to any external server

**→ HIPAA risk is minimal for this local architecture.** There is no BAA requirement when no data leaves your machine.
Still, document that your sanitization layer removes all PHI before any LLM call — this protects you if the app is ever audited or shared.

---

## The Fastest Path (Recommended)

### Option A — Zero-Code Local App (10 minutes)

**Stack:** `Ollama` + `Open WebUI` + `Llama 3.2 3B` or `MedGemma`

```
Install Ollama  →  pull model  →  run Open WebUI via Docker  →  Done
```

You get a local, browser-based interface that looks and works like ChatGPT — completely offline, no API keys, no accounts.

**Commands:**
```bash
# 1. Install Ollama (Windows/Mac/Linux installer at ollama.com)

# 2. Pull a model (choose one — see table below)
ollama pull llama3.2:3b          # fastest, lowest RAM
ollama pull medgemma3:4b         # medical-specific, Google open release

# 3. Run Open WebUI (requires Docker)
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui ghcr.io/open-webui/open-webui:main

# 4. Open browser at http://localhost:3000
```

**Time to working app:** ~10–30 minutes (mostly download time for the model).
**Cost:** $0 ongoing. One-time hardware use.

---

### Option B — Custom Python App (~2 hours)

**Stack:** `Ollama` + `Streamlit` + system prompt

Best when you want a custom UI, a fixed system prompt (e.g., "always explain in plain language"), and control over the input form.

```python
# app.py — ~50 lines total
import streamlit as st
import requests

SYSTEM_PROMPT = """You are MedSimplify, a plain-language medical explainer.
The user will paste a sanitized medical report or describe symptoms.
Your job is to explain what it means in simple, clear language a non-doctor can understand.
Always:
- Use plain English, no medical jargon.
- Explain what key terms mean.
- Mention what the findings typically indicate (general education only).
- End with: 'This explanation is for educational purposes only. Please consult your doctor.'
Never diagnose. Never recommend specific treatments or medications."""

st.title("MedSimplify — Local Medical Explainer")
st.caption("Your report stays on your machine. Nothing is sent to the internet.")

report = st.text_area("Paste your medical report or describe your symptoms:", height=200)

if st.button("Explain") and report:
    with st.spinner("Thinking..."):
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:3b",   # or "medgemma3:4b"
            "system": SYSTEM_PROMPT,
            "prompt": report,
            "stream": False
        })
        st.markdown(response.json()["response"])
        st.warning("This explanation is for educational purposes only. It is not medical advice.")
```

```bash
pip install streamlit requests
streamlit run app.py
```

---

## Open-Source Model Comparison (Local, 2026)

| Model | Size | RAM Required | Medical Knowledge | Explanation Quality | Speed | Ease of Setup | Best For |
|---|---|---|---|---|---|---|---|
| **Llama 3.2 3B** | 3B | ~4 GB RAM | Good (general) | Good | Very fast | `ollama pull llama3.2:3b` — 1 command | Lowest-spec machines, fastest iteration |
| **Llama 3.2 8B** | 8B | ~8 GB RAM | Very Good | Very Good | Fast | `ollama pull llama3.2` — 1 command | **Recommended default** — best balance |
| **MedGemma 4B** ⭐ | 4B | ~6 GB RAM | Excellent (medical-specific) | Excellent for reports | Fast | `ollama pull medgemma3:4b` | Medical reports, X-ray descriptions, lab results |
| **Mistral Small 3 7B** | 7B | ~5–8 GB RAM | Good | Good, fast output | Very fast | `ollama pull mistral` | Speed-first; good for symptom Q&A |
| **Llama 3.3 70B** | 70B | ~40 GB RAM | Excellent | Excellent | Slow (GPU needed) | `ollama pull llama3.3:70b` | High-accuracy needs; requires strong hardware |
| **Gemma 3 27B** | 27B | ~18 GB RAM | Very Good | Very Good | Moderate | `ollama pull gemma3:27b` | Mid-tier hardware with good output quality |

### Recommendation by Hardware

| Your Hardware | Best Model | Why |
|---|---|---|
| Laptop, 8–16 GB RAM (no GPU) | **Llama 3.2 8B** or **MedGemma 4B** | Runs in CPU mode via Ollama; acceptable speed |
| Desktop with GPU 8–12 GB VRAM | **MedGemma 4B** or **Mistral Small 7B** | GPU-accelerated; fast inference |
| Desktop with GPU 16–24 GB VRAM | **Gemma 3 27B** or **Llama 3.3 70B Q4** | Best quality you can run locally |

---

## Why MedGemma for This Use Case

> "Google's MedGemma is the only major open release purpose-built for medicine, with the January 2026 v1.5 release making it genuinely multimodal for clinical work." — [SiliconFlow Healthcare LLM Guide](https://www.siliconflow.com/articles/en/best-open-source-LLM-for-healthcare)

- Trained on medical literature, clinical notes, and radiology reports
- Understands medical terminology and can explain it in lay language
- Open weights — runs fully offline via Ollama
- 4B size means it fits on most modern laptops

For your use case (explain a report in plain language), MedGemma 4B outperforms larger general models because it was trained on exactly this type of content.

---

## What NOT to Use (and Why)

| Model | Problem |
|---|---|
| **BioMistral 7B** | Only 44.4% on MedQA — unreliable for explanation tasks; outdated (2024) |
| **MedAlpaca 13B** | 47–60% USMLE — below safe threshold; 2023 vintage; not updated |
| **DeepSeek (any)** | Data leaves to China-hosted servers if using API; not local-native |
| **Any model >70B** | Requires server-grade hardware; defeats the purpose of a simple local app |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│              User's Local Machine               │
│                                                 │
│  ┌──────────────┐    ┌────────────────────────┐ │
│  │  Streamlit   │───►│   Ollama (localhost)   │ │
│  │  Web UI      │    │   :11434               │ │
│  │  (browser)   │◄───│   MedGemma 4B or       │ │
│  └──────────────┘    │   Llama 3.2 8B         │ │
│                      └────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────┐              │
│  │  Your Sanitization Component  │              │
│  │  (strips PHI before input)    │              │
│  └───────────────────────────────┘              │
│                                                 │
│  No data leaves this machine.                   │
└─────────────────────────────────────────────────┘
```

---

## Recommended Build Plan (Fastest Path to Working App)

| Step | Action | Time |
|---|---|---|
| 1 | Install Ollama from [ollama.com](https://ollama.com) | 5 min |
| 2 | `ollama pull medgemma3:4b` | 10–20 min (download) |
| 3 | `pip install streamlit requests` | 2 min |
| 4 | Copy the `app.py` above, run `streamlit run app.py` | 2 min |
| 5 | Test with a sample sanitized lab report | 10 min |
| **Total** | | **~30–40 min** |

---

## Limitations to be Honest About

- **Accuracy is not guaranteed.** This is explicitly noted as an acceptable tradeoff per your requirements. MedGemma 4B is ~70–75% on MedQA — it will make mistakes on rare conditions.
- **No source citation.** Local models do not have internet access and cannot cite PubMed or MedlinePlus automatically. You would need to add a static reference list in your system prompt, or build a separate offline RAG layer later.
- **Not a diagnostic tool.** The system prompt and UI disclaimer must make this clear to users.
- **Speed on CPU.** Without a GPU, a 4–8B model on CPU may take 10–30 seconds per response on a typical laptop.

---

## Required Disclaimer (Must Appear in the UI)

> This tool provides plain-language explanations for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider with questions about your health.

---

## Sources

- [Run AI Locally 2026: Ollama & LM Studio Guide — YUV.AI](https://yuv.ai/learn/local-ai)
- [Best Local LLM Models 2026 — SitePoint](https://www.sitepoint.com/best-local-llm-models-2026/)
- [Best Ollama & Local LLM Frontends 2026 — PromptQuorum](https://www.promptquorum.com/local-llms/best-local-llm-frontends)
- [Open Source Chatbots for Local Deployment — IntuitionLabs](https://intuitionlabs.ai/articles/open-source-chatbots-local-deployment)
- [Best Open-Source LLMs for Medical Diagnosis 2026 — SofTx](https://www.softx.ca/resources/best-open-source-llms-for-medical-diagnosis)
- [Best Open Source LLM for Healthcare 2026 — SiliconFlow](https://www.siliconflow.com/articles/en/best-open-source-LLM-for-healthcare)
- [Medical Language Models Enterprise Guide 2026 — Picovoice](https://picovoice.ai/blog/medical-language-models-guide/)
- [med-gemma GitHub project — Ollama + Chainlit](https://github.com/peterruler/med-gemma)
- [Local LLM Hardware Requirements 2026 — AI Hub](https://overchat.ai/ai-hub/llm-hardware-requirements)
- [Gemma 4 vs Llama 4 vs Mistral Small 4 Comparison — DigitalApplied](https://www.digitalapplied.com/blog/gemma-4-vs-llama-4-vs-mistral-small-4-comparison)
- [Performance of Open-Source LLM in Extracting from Radiology Reports — NCBI/PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11294959/)

---

Created: 2026-08-18
