# DPDP Compliance Guidance Generator
## Phase 1 — Project Overview & Technical Documentation

**Product:** DPDP Compliance Guidance Generator  
**Version:** 1.0 (Phase 1 MVP)  
**Document type:** Executive & technical overview  
**Date:** July 2026  
**Classification:** For external sharing

---

## Table of contents

1. Executive summary  
2. Problem statement  
3. Solution overview  
4. End-to-end user workflow  
5. System architecture  
6. Technical workflow (backend processing)  
7. Regulatory context  
8. Product scope  
9. Target users and sectors  
10. Questionnaire and obligation engine  
11. Legal knowledge base  
12. Report output  
13. Technology stack  
14. Deployment model  
15. Security and privacy  
16. Limitations and disclaimers  
17. Product roadmap  

---

## 1. Executive summary

The **DPDP Compliance Guidance Generator** is a web application that helps Indian small and medium enterprises (SMEs) understand their obligations under the **Digital Personal Data Protection Act, 2023** and **DPDP Rules, 2025**.

A business completes a structured questionnaire about its data practices and receives a **personalized compliance gap report** — identifying which obligations apply, where gaps exist, and a prioritized action plan aligned to regulatory deadlines (November 2026 and May 2027).

The system uses **deterministic rule-based scoring** grounded in official legal source documents that users can download and verify. Compliance status is **not** decided by an AI language model, ensuring reproducible and auditable results.

---

## 2. Problem statement

### The problem

Indian businesses — particularly SMEs in hospitality, retail, healthcare, D2C, and related sectors — are subject to the DPDP Act and Rules, with a hard compliance deadline of **May 13, 2027**. However:

- Most are **unaware** the law applies to them  
- Even when aware, they lack **legal expertise, time, or budget** to interpret dense legal text  
- Generic blog content does not tell them what **they specifically** need to do  
- Hiring lawyers or consultants is **expensive and slow** relative to business scale  
- Doing nothing exposes them to **penalties and breach risk**  

### What Phase 1 solves

A business answers a structured questionnaire and receives a **personalized, legally-grounded compliance gap report** — without reading the Act themselves or hiring a consultant for initial orientation.

### Success criterion

A business owner with **zero prior DPDP awareness** (e.g. a hotel operator) can, in a few minutes, understand:

- What applies to them  
- Where they fall short today  
- What to fix first and by when  

### Phase 1 vs Phase 2

| Phase | Question answered |
|-------|-------------------|
| **Phase 1** (this product) | *What do I need to do and why?* |
| **Phase 2** (planned) | *How do I actually do it every day?* (consent management, data inventory, breach workflows) |

---

## 3. Solution overview

The application combines three layers:

1. **Structured intake** — 33 questions across 9 sections about data practices  
2. **Rules engine** — 39 DPDP obligations scored as Met / Partially met / Not met / Not applicable  
3. **Legal grounding** — Official Act and Rules PDFs with keyword-based citation retrieval  

**Design principle:** Scoring is deterministic and auditable. Legal PDFs are the source of truth. Users can download sources to verify any recommendation.

---

## 4. End-to-end user workflow

This is the complete journey from a business user's perspective:

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────┐
│  1. Open app │───▶│ 2. Review legal │───▶│ 3. Complete      │───▶│ 4. Generate │
│              │    │    sources      │    │  questionnaire   │    │    report   │
└──────────────┘    │  (sidebar)      │    │  (33 questions)  │    └──────┬──────┘
                    └─────────────────┘    └──────────────────┘           │
                                                                          ▼
                    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────┐
                    │ 7. Download PDF │◀───│ 6. Review gaps,  │◀───│ 5. View on- │
                    │    report       │    │  action plan,    │    │  screen     │
                    └─────────────────┘    │  citations       │    │  summary    │
                                           └──────────────────┘    └─────────────┘
```

### Step-by-step

| Step | User action | System response |
|------|-------------|-----------------|
| 1 | Opens the web application | Landing page with legal sources sidebar |
| 2 | Optionally downloads source PDFs | Official DPDP Act, Rules, and reference documents |
| 3 | Enters company name, sector, answers questionnaire | Questions grouped by topic (data collection, consent, security, etc.) |
| 4 | Clicks "Generate gap report" | Backend scores all 39 obligations |
| 5 | Reviews on-screen report | Summary, timeline, action plan, obligation details with citations |
| 6 | Verifies citations against source PDFs | Download links per obligation |
| 7 | Downloads PDF report | Professional PDF for printing, email, or internal sharing |

**Typical duration:** 15–25 minutes for a first-time user.

---

## 5. System architecture

### High-level architecture diagram

```
                    ┌─────────────────────────────────────────┐
                    │           USER BROWSER                   │
                    │  ┌─────────────────────────────────────┐ │
                    │  │     React Web Application           │ │
                    │  │  • Questionnaire wizard             │ │
                    │  │  • Report viewer                    │ │
                    │  │  • Legal sources sidebar            │ │
                    │  └──────────────┬──────────────────────┘ │
                    └─────────────────┼────────────────────────┘
                                      │ HTTPS
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │              NGINX                       │
                    │  • Serves React static files             │
                    │  • Proxies /api/* to backend             │
                    └──────────────┬──────────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────────┐
                    │         FASTAPI BACKEND                  │
                    │  ┌────────────┐  ┌────────────────────┐ │
                    │  │ API Layer  │  │ Questionnaire      │ │
                    │  └─────┬──────┘  │ Module             │ │
                    │        │         └────────────────────┘ │
                    │        ▼                                  │
                    │  ┌────────────┐  ┌────────────────────┐ │
                    │  │ Rules      │  │ Report Generator   │ │
                    │  │ Engine     │──│ + PDF Export       │ │
                    │  │(39 rules)  │  └────────────────────┘ │
                    │  └─────┬──────┘                          │
                    │        ▼                                  │
                    │  ┌────────────┐                          │
                    │  │ Keyword    │                          │
                    │  │ Retrieval  │                          │
                    │  └─────┬──────┘                          │
                    └────────┼────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐ ┌──────────┐ ┌──────────────┐
        │ Source   │ │ Text     │ │ Source       │
        │ PDFs     │ │ Corpus   │ │ Manifest     │
        │(Act,     │ │(search-  │ │(metadata)    │
        │ Rules)   │ │ able)    │ │              │
        └──────────┘ └──────────┘ └──────────────┘
```

### Component responsibilities

| Component | Responsibility |
|-----------|----------------|
| **React frontend** | Questionnaire wizard, report view, legal sources sidebar, PDF download |
| **nginx** | Single entry point; serves UI and proxies API requests |
| **FastAPI backend** | REST API, request validation, orchestration |
| **Rules engine** | Maps questionnaire answers to obligation statuses (deterministic) |
| **Retrieval layer** | Keyword search over legal text corpus for citations |
| **PDF export** | Professional gap report generation |
| **Legal data store** | Official DPDP Act and Rules PDFs with metadata catalog |

### Deployment topology (Docker)

```
┌──────────────── docker compose ────────────────┐
│                                                 │
│  ┌─────────────────┐    ┌──────────────────┐  │
│  │ Frontend        │    │ Backend          │  │
│  │ (nginx + React) │───▶│ (FastAPI)        │  │
│  │ Port: 8888      │    │ Port: 8000       │  │
│  └─────────────────┘    └────────┬─────────┘  │
│                                 │             │
│                        ┌────────▼─────────┐  │
│                        │ Legal data volume │  │
│                        │ (PDFs + corpus)   │  │
│                        └──────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 6. Technical workflow (backend processing)

When a user submits the questionnaire, the following processing occurs:

```
INPUT: company_name, sector, answers{33 fields}
                │
                ▼
┌───────────────────────────────────┐
│ 1. VALIDATE submission (schema)   │
└───────────────┬───────────────────┘
                ▼
┌───────────────────────────────────┐
│ 2. RULES ENGINE                     │
│    For each of 39 obligations:    │
│    • Check applicability          │
│    • score_obligation(answers)      │
│    • → status, gap, action          │
└───────────────┬───────────────────┘
                ▼
┌───────────────────────────────────┐
│ 3. CITATION RETRIEVAL             │
│    For each obligation:           │
│    • Build search query           │
│    • Keyword match in corpus      │
│    • Attach top legal excerpts    │
└───────────────┬───────────────────┘
                ▼
┌───────────────────────────────────┐
│ 4. REPORT ASSEMBLY                │
│    • Summary statistics           │
│    • Regulatory timeline          │
│    • Prioritized action plan      │
│    • Obligations by category      │
│    • Legal source references      │
└───────────────┬───────────────────┘
                ▼
OUTPUT: JSON report → Screen display / PDF download
```

### Scoring approach

| Approach | Used for | Rationale |
|----------|----------|-----------|
| **Rule-based logic** | Met / Partial / Not met decisions | Reproducible, auditable, no hallucination |
| **Keyword retrieval** | Legal excerpts and citations | Grounded in actual Act/Rules text |
| **LLM (not used)** | — | Avoided for compliance decisions in Phase 1 |

---

## 7. Regulatory context

### DPDP Act, 2023

India's standalone data protection law (Act No. 22 of 2023), published August 11, 2023.

**Key roles:**

- **Data Principal** — individual whose data is processed  
- **Data Fiduciary** — entity deciding purpose and means of processing  
- **Data Processor** — processes on fiduciary's behalf  
- **Significant Data Fiduciary (SDF)** — designated by government for enhanced obligations  

### DPDP Rules, 2025

Notified November 13, 2025 (G.S.R. 846(E)).

### Implementation timeline

| Phase | Effective date | What kicks in |
|-------|----------------|---------------|
| Phase I | Nov 13, 2025 | Data Protection Board established |
| Phase II | Nov 13, 2026 | Consent Manager provisions |
| Phase III | **May 13, 2027** | All substantive compliance obligations |

### Primary legal sources (embedded in application)

| Document | Role |
|----------|------|
| DPDP Act, 2023 (MeitY) | Primary legal text |
| DPDP Rules, 2025 (G.S.R. 846(E)) | Operational rules |
| PIB notification summary | Implementation timeline |
| DSCI Rule-to-Section index | Cross-reference |
| DLA Piper India guide | Secondary interpretation reference |

All primary sources are downloadable from within the application for instant verification.

---

## 8. Product scope

### In scope (Phase 1)

- Structured questionnaire (33 questions, 9 sections)  
- Assessment of **39 Data Fiduciary obligations**  
- Status per obligation: Met / Partially met / Not met / Not applicable  
- Keyword-based legal excerpt retrieval for citations  
- Downloadable primary source PDFs from the application  
- Prioritized action plan (Nov 2026 vs May 2027 deadlines)  
- Professional PDF gap report download  
- Containerized deployment for demos and pilots  

### Out of scope (Phase 1)

- AI/LLM-based compliance decisions  
- Drafting legal documents (privacy policies, DPAs)  
- Ongoing consent management or monitoring  
- Integration with customer systems (CRM, PMS, website)  
- Multi-tenant SaaS with user accounts  
- Certified legal opinions  

---

## 9. Target users and sectors

### Users

| User | Need |
|------|------|
| SME business owner | Understand DPDP applicability and gaps quickly |
| Operations / IT manager | Actionable checklist before May 2027 |
| Internal compliance champion | Structured starting point |
| CEO / leadership | Executive summary for decision-making |

### Supported sectors (23)

Hospitality, retail, healthcare, D2C, food & beverage, travel, fintech, insurance, education, real estate, logistics, manufacturing, IT/SaaS, professional services, media, automotive, telecom, agriculture, nonprofit, staffing, beauty/wellness, fitness, and other.

---

## 10. Questionnaire and obligation engine

### Questionnaire sections (9)

1. Business profile  
2. Data collection  
3. Notice & consent  
4. Data lifecycle  
5. Data Principal rights  
6. Transparency & contact  
7. Processors & transfers  
8. Security & breach  
9. Employment & Significant Data Fiduciary  

### Obligation categories (39 total)

| Category | Count | Examples |
|----------|-------|----------|
| Lawful processing | 4 | Consent, legitimate use, purpose limitation |
| Notice & consent | 6 | Rule 3 notice, consent records, withdrawal |
| Data quality & lifecycle | 4 | Accuracy, retention, erasure |
| Data Principal rights | 6 | Access, correction, erasure, grievance |
| Transparency & contact | 2 | DPO contact, grievance officer |
| Processors & transfers | 3 | Contracts, oversight, cross-border |
| Security & breach | 5 | Safeguards, logging, breach notification |
| Children's data | 2 | Verifiable consent, no tracking |
| SDF / special cases | 7 | SDF assessment, employee data, CCTV |

### Status definitions

| Status | Meaning |
|--------|---------|
| **Met** | Reported practice satisfies obligation |
| **Partially met** | Some elements present; gaps remain |
| **Not met** | Material gap; action required |
| **Not applicable** | Does not apply based on answers |

---

## 11. Legal knowledge base

### How legal grounding works

1. Official DPDP Act and Rules PDFs are stored in the application  
2. Text is extracted and split into searchable segments  
3. When scoring an obligation, relevant segments are retrieved by keyword matching  
4. Excerpts are attached to the report with links to download the full source PDF  

### Why this matters for trust

Users can verify every recommendation against the original legal text — critical for a compliance product aimed at businesses without in-house legal teams.

---

## 12. Report output

### On-screen report includes

- Executive summary (obligations assessed, gaps found, critical gaps)  
- Regulatory timeline with key dates  
- Prioritized action plan (before Nov 2026 / before May 2027)  
- Detailed obligation assessment grouped by category  
- Legal excerpts with source download links  

### PDF report includes

- Professional cover page (company name, sector, IST timestamp)  
- Page numbers  
- Print-ready layout for sharing with stakeholders  
- Full disclaimer  

---

## 13. Technology stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, TypeScript, Vite |
| API server | Python 3.11, FastAPI, Uvicorn |
| Scoring | Deterministic Python rules engine |
| Legal retrieval | Keyword search over indexed corpus |
| PDF generation | WeasyPrint |
| Reverse proxy | nginx |
| Packaging | Docker, Docker Compose |

---

## 14. Deployment model

The application runs as two containerized services:

- **Frontend container** — nginx serving the React app on port 8888  
- **Backend container** — FastAPI API with legal data volume mounted  

Single URL access for demos and presentations. Suitable for on-premise pilot, private cloud, or internal network deployment.

---

## 15. Security and privacy

- Stateless API — no questionnaire data persisted to database in v1  
- Legal source PDFs mounted read-only  
- No authentication in v1 — intended for private/demo deployment  
- CORS restricted to application origin  
- Suitable for deployment behind corporate VPN or private network  

---

## 16. Limitations and disclaimers

### Limitations

1. **Self-reported answers** — report accuracy depends on honest input  
2. **Rule-based interpretation** — not a substitute for qualified legal counsel  
3. **Keyword citations** — excerpts support verification but should be cross-checked  
4. **Sector selection** — labels the business; scoring logic is largely sector-agnostic in v1  
5. **SDF status** — heuristic assessment only; government designates Significant Data Fiduciaries  

### Disclaimer

> This report is automated compliance guidance based on questionnaire answers and the DPDP Act 2023 / DPDP Rules 2025. It is not legal advice. Download and verify the cited source documents. Consult qualified counsel before relying on this report for regulatory decisions.

---

## 17. Product roadmap

| Phase | Capability | Status |
|-------|------------|--------|
| **Phase 1** | Gap assessment + action plan + PDF report | Complete |
| **Phase 2a** | Auto-draft privacy notices, DPAs, consent copy | Planned |
| **Phase 2b** | Consent management, data inventory, rights workflows | Planned |
| **Phase 3** | Full compliance operating system with integrations | Planned |

Phase 1 questionnaire data is structured to seed Phase 2 without requiring businesses to re-enter information.

---

## Document information

| Field | Value |
|-------|-------|
| Title | DPDP Compliance Guidance Generator — Phase 1 Overview |
| Version | 1.0 |
| Date | July 2026 |
| Purpose | Executive and technical sharing |

---

*End of document*
