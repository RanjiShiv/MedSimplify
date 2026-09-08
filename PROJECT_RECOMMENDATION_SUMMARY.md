# MedSimplify Project Recommendation Summary

> **Instructions applied:** Sources cited, reasoning shown, HIPAA compliance warnings included, uncertainty flagged explicitly.

---

## Research Question (from 1_research.md)

Find the best LLM for:
- Answering generic medical questions
- Reading symptoms and suggesting diagnosis
- Citing sources, accuracy, and confidence
- Goal: cheapest, most capable, most knowledgeable option

---

## HIPAA Compliance Warning

> **CRITICAL — Read before building anything.**
> If your application processes any Protected Health Information (PHI) — including symptoms, diagnoses, patient names, dates, or any data that could identify a person — you are subject to HIPAA.
> - You **must** sign a **Business Associate Agreement (BAA)** with your LLM vendor before using their API with PHI.
> - BAAs are available from: **Microsoft Azure OpenAI**, **Google Cloud Vertex AI (Gemini)**, **AWS Bedrock (Claude, Llama)**.
> - Calling the OpenAI, Anthropic, or Google APIs *directly* (not via their cloud/enterprise services) does **not** include a BAA by default.
> - Unauthorized disclosure of PHI carries fines from **$141 to $2.1M+ per violation** (2026 penalty schedule).
> - Source: [HIPAA Compliant LLM Guide — TechMagic](https://www.techmagic.co/blog/hipaa-compliant-llms), [Sanoworks FDA/HIPAA Guide](https://www.sanoworks.com/blog/llms-clinical-settings-fda-hipaa-hospital-requirements/)

---

## LLM Comparison Table (August 2026)

### Paid / Closed Models

| Model | MedQA Score | HealthBench | Unsafe Response Rate | Input Cost ($/MTok) | Output Cost ($/MTok) | BAA Available | Best For | Limitations |
|---|---|---|---|---|---|---|---|---|
| **GPT-4.1 (OpenAI)** | ~94% | 88.0 (best) | ~13% | $5.00 | $15.00 | Yes (Azure) | Highest reasoning quality, complex diagnosis | Most expensive closed model |
| **GPT-4.1 Mini** | ~88% | ~82 | ~12% | $0.40 | $1.60 | Yes (Azure) | Cost/accuracy sweet spot | Less capable than full GPT-4.1 |
| **GPT-4.1 Nano** | ~80% | ~75 | ~14% | $0.10 | $0.40 | Yes (Azure) | High-volume triage, cheap Q&A | Not suitable for complex diagnosis |
| **GPT-5 (OpenAI)** | **95.84%** | **88.0** | ~11% | Higher than GPT-4.1 | Higher | Yes (Azure) | State-of-the-art, USMLE 95.22% avg | Expensive; may be overkill for v1 |
| **Claude Sonnet 5 (Anthropic)** | ~90% | 77.0 | **5% (lowest unsafe)** | $2.00 | $8.00 | Yes (AWS Bedrock) | Safest outputs, best for patient-facing text, long documents | Lower MedQA than GPT-5/Gemini |
| **Claude Opus 4.8** | ~92% | ~80 | **5% (lowest unsafe)** | $5.00 | $25.00 | Yes (AWS Bedrock) | Best Claude for medical reasoning | Very expensive |
| **Gemini 3.1 Pro (Google)** | **97.4% (highest)** | 79.3 | ~10% | $2.00 | $12.00 | Yes (Google Cloud) | Highest MedQA accuracy; multimodal (images/labs) | HealthBench lower than GPT; privacy concerns |
| **Gemini 2.5 Flash** | ~85% | ~72 | ~11% | $0.15 | $0.60 | Yes (Google Cloud) | Cheapest high-quality option with 1M token context | Less accurate than Pro |
| **Med-Gemini (Google DeepMind)** | **91.1%** (uncertainty-guided) | ~80 | Research only | Not publicly priced | Not publicly priced | Research only | Clinical reasoning specialist | Not generally available via API yet |

### Open-Source Models

| Model | MedQA Score | Parameters | Cost | BAA | Best For | Limitations |
|---|---|---|---|---|---|---|
| **Llama 3.3 70B Instruct (Meta)** | ~75-80% (general) | 70B | Self-host or via Bedrock/Groq | Yes (Bedrock) | Privacy-first on-prem deployment, no API cost | Needs prompt tuning, safety guardrails; lower accuracy than frontier |
| **Llama 4 Scout/Maverick** | ~82% (est.) | MoE | Groq/Fireworks free tier | Via Bedrock | Latest Meta model, competitive on benchmarks | Still being evaluated clinically |
| **BioMistral 7B** | 44.4% | 7B | Free (self-host) | Self-managed | Biomedical pre-training on PubMed | Significantly below frontier models; not production-ready for diagnosis |
| **MedAlpaca 13B** | 47-60% (USMLE) | 13B | Free (self-host) | Self-managed | Research/prototyping | Below passing threshold for clinical use; 2023 vintage |
| **Aloe (HPAI)** | ~70% | 7B-70B | Free (self-host) | Self-managed | Specialized healthcare fine-tune; RAG-ready | Less tested in production |
| **DeepSeek V4 Flash** | ~72% | MoE | $0.14/$0.28 per MTok | No BAA | Cheapest API option overall | Data residency in China — not HIPAA suitable |

---

## Benchmark Key (Sources)

- **MedQA**: 4-option USMLE-style questions — tests textbook medical knowledge.
- **HealthBench**: OpenAI, May 2025 — 5,000 physician-written multi-turn health conversations; measures real-world safe, complete, context-aware answers. This is now the more clinically relevant benchmark.
- **Unsafe Response Rate**: % of responses flagged as potentially harmful in medical context (Nature npj Digital Medicine study, 2026).

> **Important caveat:** Even the best model (GPT-5 ~95.84% MedQA) shows only ~52% diagnostic accuracy on real-world ambiguous clinical cases (NYU Langone study, 100 real clinical queries). Benchmarks test knowledge recall, not clinical judgment.
>
> Source: [Nature npj Digital Medicine — unsafe LLM answers](https://www.nature.com/articles/s41746-026-02428-5), [PMC comparative study GPT-4o/Claude/Gemini](https://pmc.ncbi.nlm.nih.gov/articles/PMC12474969/)

---

## Reasoning: How I Derived the Recommendation

**Step 1 — Eliminate non-HIPAA options for PHI use:**
DeepSeek (China residency) and direct API calls without BAA are eliminated for any production health app handling patient data.

**Step 2 — Rank by accuracy on relevant benchmarks:**
HealthBench (real clinical dialogue) is more predictive than MedQA (test-taking) for a patient-facing app.
GPT-5 / GPT-4.1 leads HealthBench (88.0) > Gemini 3.1 Pro (79.3) > Claude Sonnet 5 (77.0).

**Step 3 — Weight safety (critical for medical):**
Claude has the lowest unsafe response rate (5% vs 13% for GPT/Llama). This matters enormously for a patient-facing tool.

**Step 4 — Factor in cost:**
GPT-4.1 Mini ($0.40/$1.60) delivers ~88% MedQA at 12× lower cost than GPT-4.1. For a v1 that uses RAG to ground answers in trusted sources, this accuracy gap is acceptable.

**Step 5 — RAG closes the gap:**
When combined with a retrieval layer (MedlinePlus, PubMed, CDC/NIH content), any frontier model can cite verified sources — reducing hallucination risk and making the underlying model's raw benchmark score less decisive.

---

## Updated Recommendation

### Recommended Stack for MedSimplify v1

| Component | Choice | Reason |
|---|---|---|
| **LLM (primary)** | **GPT-4.1 Mini via Azure OpenAI** | Best cost/accuracy balance; HIPAA BAA available; HealthBench-proven |
| **LLM (upgrade path)** | **GPT-4.1 or Claude Sonnet 5** | Upgrade for complex reasoning (GPT) or highest safety (Claude) |
| **Retrieval (RAG)** | MedlinePlus + PubMed abstracts + CDC | Grounds answers in verified, citable sources |
| **Deployment** | Azure (for BAA + GPT) or AWS Bedrock (for Claude) | Legally required if touching PHI |
| **Open-source fallback** | Llama 3.3 70B via AWS Bedrock | If zero API cost is required and on-prem is an option |

### Why Not Med-Gemini?
Highest MedQA score (97.4%) but not yet generally available via public API. Gemini 3.1 Pro is the usable equivalent, and its HealthBench score (79.3) trails GPT-4.1 meaningfully.

### Why Not Claude as Primary?
Claude Sonnet 5's safety profile is the best. However, its HealthBench score (77.0) is 11 points below GPT-4.1. Use Claude when the primary concern is patient safety language and long document summarization (e.g., simplifying a radiology report). Use GPT-4.1 when accuracy on clinical Q&A is paramount.

### Cheapest Capable Option
**GPT-4.1 Mini** ($0.40 input / $1.60 output per million tokens) — delivers ~88% MedQA accuracy at a fraction of frontier model pricing. With a good RAG layer, this is production-viable for symptom guidance and general Q&A.

---

## Architecture (Updated)

```
User Prompt
    │
    ▼
Intent Router (classify: simplification / symptom Q&A / general medical Q)
    │
    ├──► Simplification flow → Claude Sonnet 5 (best long-doc + safe language)
    │
    └──► Q&A / Symptom flow
              │
              ▼
         RAG Layer (MedlinePlus, PubMed, CDC/NIH)
              │
              ▼
         GPT-4.1 Mini (with retrieved context)
              │
              ▼
         Safety Layer (disclaimer + red-flag escalation)
              │
              ▼
         Response (plain language + bullet points + cited sources)
```

---

## Required Disclaimer (Mandatory on Every Response)

> This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. If you are experiencing severe, worsening, or urgent symptoms — including chest pain, difficulty breathing, stroke-like signs, or suicidal thoughts — seek immediate emergency care. Do not delay treatment based on AI-generated content.

---

## Open-Source-Only Path (If Avoiding All Paid APIs)

Use **Llama 3.3 70B Instruct** self-hosted or via AWS Bedrock.

- Tradeoffs: ~75-80% MedQA (vs 88%+ for frontier); requires significant prompt engineering and manual safety guardrail work; no built-in citation mechanism.
- Do **not** use BioMistral or MedAlpaca for production — their scores (44-60% MedQA) are below safe clinical thresholds.

---

## Sources

- [Best Open-Source LLMs for Medical Diagnosis (2026) — SofTx](https://www.softx.ca/resources/best-open-source-llms-for-medical-diagnosis)
- [ChatGPT vs Claude for Healthcare 2026 — IntuitionLabs](https://intuitionlabs.ai/articles/chatgpt-vs-claude-for-healthcare)
- [Best LLM for Medical Advice: GPT-5 vs Gemini vs Med-PaLM — CipherNutz](https://ciphernutz.com/blog/which-llm-is-best-for-medical-advice)
- [Large language models provide unsafe answers to patient-posed medical questions — Nature npj Digital Medicine](https://www.nature.com/articles/s41746-026-02428-5)
- [Comparing GPT, Gemini, Claude on medical exams (English/Polish) — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12474969/)
- [Multimodal Diagnostic Accuracy of GPT-4.o, Claude 3.7, Gemini 2.5 on Retina Cases — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12960270/)
- [LLM Benchmarks in Life Sciences — IntuitionLabs](https://intuitionlabs.ai/articles/large-language-model-benchmarks-life-sciences-overview)
- [BioMistral: Open-Source Pretrained LLMs for Medical Domains — arXiv](https://arxiv.org/html/2402.10373)
- [Aloe Family Recipe for Open Healthcare LLMs — arXiv](https://arxiv.org/pdf/2505.04388)
- [LLM API Pricing Comparison 2026 — Spheron Blog](https://www.spheron.network/blog/llm-api-pricing-comparison-gpt-claude-gemini-deepseek-2026/)
- [LLM API Providers 2026: 12 APIs Compared — MorphLLM](https://www.morphllm.com/llm-api)
- [HIPAA Compliant LLM Guide — TechMagic](https://www.techmagic.co/blog/hipaa-compliant-llms)
- [LLMs in Clinical Settings: FDA, HIPAA Guide 2026 — Sanoworks](https://www.sanoworks.com/blog/llms-clinical-settings-fda-hipaa-hospital-requirements/)
- [End-to-End Agentic RAG for Traceable Diagnostic Reasoning — arXiv (Aug 2026)](https://arxiv.org/pdf/2508.15746)
- [Dr. GPT Will See You Now — Crowdsourced Clinical Cases Study — arXiv](https://arxiv.org/pdf/2506.13805)

---

Updated: 2026-08-18
