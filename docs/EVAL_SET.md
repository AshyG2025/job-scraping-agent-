# Evaluation Set — Gold Standard for the Scoring Prompt

> **How this file is used:** Before deploying any change to `SCORING_PROMPT.md`, run the prompt against these 6 postings and confirm the scores match (within ±1 of the target). If they don't, iterate the prompt — don't ship.
>
> **Source:** Adapted from `Job Posting samples/JD mapping to my exp..docx` (Ayesha's manually labeled set).
>
> **JD bodies live in `docs/EVAL_SET_JDS.md`** — paste those into `MANUAL_JDS.md` and run `python scripts/score_jobs.py` to re-run the eval set. This file (`EVAL_SET.md`) holds only the targets + reasoning; the actual JD text is in the companion file so calibration stays runnable even after the original postings come down off live ATS boards.
>
> **Last updated:** 2026-05-02 (Session 2.2.1: companion file `docs/EVAL_SET_JDS.md` added with all 6 JD bodies extracted from the source docx, so calibration is no longer dependent on roles still being live)

---

## Why these 6 postings

This set was deliberately chosen to span the full scoring range — from "recruiter actually reached out" (a 9) through "weak match, manager-scope dealbreaker" (a 2). It also includes a tricky case (Boku) where surface-level signals look moderate but a hard-requirement dealbreaker (Mandarin fluency) drops the score. The matcher needs to catch all of these.

---

## Posting 1 — Wise: Senior PM, Invoicing (Wise Business)

**User label:** Very relevant
**Target final score:** **8** (`apply`)

| Dimension | Target | Reasoning |
|---|---|---|
| Domain | 8 | Invoicing is a B2B SaaS / FinTech rails platform — direct fit. SMB-focused getting-paid product. |
| Skills | 8 | JD explicitly asks for: building products end-to-end, working with backend engineers, technical trade-offs, structure-from-ambiguity. Direct match to WFM Convergence + Mexico stories. |
| Level | 8 | "5+ years experience" — at-bar / over-bar (she has 7) |
| Team needs | 8 | Building "low/no-code solutions" for B2B partners to get paid — multi-stakeholder, integration-heavy, exactly her type |

**Expected verdict:** `apply`
**Resume choice:** `Ayesha Base Platform PM.docx`
**H1B status:** `n/a_uk_role`
**Lead with:** WFM Convergence (B2B partners) + Mexico Tax Recon (financial integration)
**Notable bullet tweaks:** Reframe supplier onboarding as "B2B partner self-service onboarding"; emphasize API/data-contract work

---

## Posting 2 — Wise: Senior PM, Treasury Ledger Platform

**User label:** Recruiter reached out (the strongest possible signal)
**Target final score:** **9** (`prioritize`)

| Dimension | Target | Reasoning |
|---|---|---|
| Domain | 9 | Multi-system ledger platform processing 2bn+ journal entries/month — direct match to multi-system integration + reconciliation work |
| Skills | 9 | JD explicitly requires: technical leadership, deep-dive into architecture with engineers, strong IC, system-level thinking, hands-on. All direct strong-match. |
| Level | 8 | "Multiple years of product building" — flexible; the IC + technical-depth language signals Senior–Staff |
| Team needs | 9 | "Completeness, accuracy, controls" mandate maps almost 1:1 to Mexico Tax Recon (72→89% accuracy, 36-attribute mapping, controls framework) |

**Expected verdict:** `prioritize`
**Resume choice:** `Ayesha Base Platform PM.docx`
**H1B status:** `n/a_uk_role`
**Lead with:** Mexico Tax Reconciliation (frame as "ledger/integrity platform"); supporting story = WFM Convergence for systems-thinking
**Notable cover-letter angle:** "Treasury ledger and tax reconciliation share the same hard problem — guaranteeing data integrity across systems that weren't designed to talk to each other."

---

## Posting 3 — Liberis: Senior PM, Financial Systems

**User label:** Very relevant
**Target final score:** **8** (`apply`)

| Dimension | Target | Reasoning |
|---|---|---|
| Domain | 9 | Embedded finance platform; "payment rails, ledger, merchant revenue intelligence, identity systems" — very direct |
| Skills | 8 | JD asks for: systems thinker, technical depth, complex migrations, vendor transitions, build-vs-buy. Direct match to WFM 5→1 consolidation. |
| Level | 7 | Senior PM ask aligns with her band; scope is meaty Senior with some Staff-level breadth |
| Team needs | 8 | "Replace legacy vendor systems with in-house AI models" — direct match to AI Invoice Automation; "complex platform initiatives end-to-end" — direct match to WFM |

**Expected verdict:** `apply`
**Resume choice:** `Ayesha Base Platform PM.docx`
**H1B status:** `n/a_uk_role`
**Lead with:** WFM Convergence (platform consolidation, vendor migration); supporting = AI Invoice Automation (vendor-to-AI-model replacement parallel)
**Notable angle:** Liberis explicitly mentions AI-first transformation; AI Invoice Automation gives her direct credibility on "vendor-to-AI" transitions.

---

## Posting 4 — Ebury: (Senior) PM, API Platform & Developer Experience

**User label:** Moderate match
**Target final score:** **6** (`consider`)

| Dimension | Target | Reasoning |
|---|---|---|
| Domain | 7 | API platform — adjacent. But "developer experience" framing skews more external-developer-ecosystem than her B2B-partner experience |
| Skills | 6 | JD asks for: API design, webhooks, OAuth, event-driven systems, external developer feedback loops. Her API work was internal+B2B-partners, not external dev community. |
| Level | 7 | Senior or L4 ask is at-bar |
| Team needs | 5 | Team's primary need is growing external developer adoption + reducing integration time for new API consumers — adjacent but not direct match |

**Expected verdict:** `consider`
**Resume choice:** `Ayesha Base Platform PM.docx`
**H1B status:** `n/a_uk_role`
**Lead with:** WFM Convergence's API suite (Item Registration, Mapping Lookup, Bulk Sync) + reframe supplier onboarding NPS gains as "developer experience"
**Notable gap to address:** External developer ecosystem experience is the core gap; cover letter must explicitly bridge "B2B partner onboarding" → "developer onboarding" (same first-principles, different vocabulary).

---

## Posting 5 — Boku: Growth PM, Subscription Products

**User label:** Moderate match
**Target final score:** **3** (`weak`) — Mandarin requirement is dealbreaker
**⚠️ Note for Ayesha to confirm:** Your label said "moderate match" but the JD includes "**Fluency in Mandarin (spoken and written) is required.**" If you don't have Mandarin fluency, this should drop to a `weak`/`skip`. If I've misread or the JD changed, tell me and I'll adjust the eval target.

| Dimension | Target | Reasoning |
|---|---|---|
| Domain | 5 | B2B SaaS / payments, reasonable adjacency, but Growth PM is a different subdomain than Platform PM |
| Skills | 5 | Funnel analysis, A/B testing, RICE, JTBD — these are PM-general, not platform-specific. Her experimentation work (AI Invoice 4-week experiment) gives some evidence but not the core ask. |
| Level | 6 | "3–5 years" — she's over-leveled (7 years), borderline over |
| Team needs | 4 | Team needs growth-funnel optimization expertise (acquisition → activation → retention metrics, North Star, AARRR). Limited evidence in her flagships. |
| **Dealbreaker** | — | Mandarin fluency required (hard skill not in her profile per memory). One-dimension dealbreaker → cap final score at 4. |

**Expected verdict:** `weak`
**Resume choice:** N/A (score < 7, no asset matching)
**H1B status:** `n/a_uk_role`

---

## Posting 6 — Rippling: Product Lead, Talent Management

**User label:** Weak match
**Target final score:** **2** (`skip`)

| Dimension | Target | Reasoning |
|---|---|---|
| Domain | 2 | Talent Management product suite — HR / employee-management domain, no platform / API / integration focus. Wrong domain for her positioning. |
| Skills | 3 | JD asks for "Helicopter pilot mentality," strategic + UI polish, founder/hyper-growth experience, complex workflows + integration/marketplace products. Some skill overlap (workflow / integration) but framed for product leadership of a feature suite, not platform ownership. |
| Level | 4 | "8+ years of Product Management experience" — she has 7. Slightly under. Combined with "Product Lead" title, this is likely Group PM / Director-style scope at Rippling — possibly people-management. |
| Team needs | 3 | Team needs Talent Management product expertise (manager development, employee growth tools) — limited overlap |
| **Possible dealbreaker** | — | "Product Lead" with this scope often implies people-management at growth-stage SaaS. JD doesn't explicitly say "manage PMs" but the implicit scope suggests it. Should be flagged for manual review even before scoring. |

**Expected verdict:** `skip`
**Resume choice:** N/A
**H1B status:** `confirmed_sponsor` (Rippling does sponsor — confirmed in COMPANY_LIST research) — but irrelevant given the score

---

## How to use this file when iterating

1. After any meaningful change to `SCORING_PROMPT.md`, run the prompt against the 6 postings:
   - `cat docs/EVAL_SET_JDS.md >> MANUAL_JDS.md`
   - `python scripts/score_jobs.py`
   - Read `_local/digest.md` and compare each role's `final_score` to the target below.
2. Compare the model's `final_score` to the target above.
3. If any posting is off by **> 1 point**, the prompt isn't working — iterate before shipping.
4. If a posting is off by **exactly 1 point**, judgment call — usually fine, but read the model's reasoning and check if it's defensible.
5. **If your judgment changes** about a posting (e.g., you decide Ebury is actually a 5 not a 6), update this file *first*, then re-run the prompt against the new target.
6. **If you want to add a 7th, 8th, … posting** to the gold set: append a new section to this file with the same structure (label, target, per-dimension reasoning, expected verdict, resume choice, H1B), AND append the JD body to `docs/EVAL_SET_JDS.md` in the same format the runner reads.

---

## ⚠️ One question for you (Ayesha) before we treat this as final

**Posting 5 (Boku):** Do you have Mandarin fluency? If yes, I'll adjust the target score upward. If no, the Mandarin requirement is a hard dealbreaker and the target stays at 3.
