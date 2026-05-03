# Project Brief — Ideal Next Role (public copy)

> **What this file is:** The agent's primary anchor for what counts as a "good match." The working copy with personal/strategic detail (named-company target lists, comp expectations, file-pathed resume routing) is kept local-only — see `PROJECT_BRIEF.md` in the project's local working tree (gitignored).
>
> **Why the split:** Personal context (comp expectations, visa status), specific resume file paths, and competitor-named past-application analyses are kept local; the role brief, flagship project anchors, and resume-selection logic are visible here as PM design content.
>
> **Sync rule:** Per `CLAUDE.md` Rule 7, framework changes to the local working copy (role brief, great-match / weak-match criteria, geography rules, flagship metrics, resume-selection routing logic) must be reflected here in the same edit. Adding / removing specific companies in target lists, editing the comp section, or adjusting Referral Network does not propagate.
>
> **Last updated:** 2026-05-02 (Session 2.2: added "Problem-shape framings" sub-block to each of the 4 flagships — 6–8 illustrative framings per flagship that describe the same underlying work in different domain vocabularies, so the matcher can recognize situational matches even when JDs use unfamiliar terms. Companion change in `SCORING_PROMPT.md` v1.1 adds the prompt-side guardrail. Earlier 2026-04-30: initial public copy — genericized from local source.)

---

## Role brief (in my own words)

My ideal role is a **Senior or Principal Product Manager** working on **platform-based products** in the **B2B SaaS or FinTech** space, in **London or Seattle / Bay Area**, at either a **FAANG / public tech company** or a **growth-stage company (Series C+)**.

This role will see me build, manage, or scale **platform architecture serving multi-stakeholder customers** — external partners, internal product/engineering teams, or both. I want to own the platform end-to-end: vision, architecture decisions, API strategy, adoption metrics, and cross-functional execution.

This typically **won't be a feature-PM role on top of someone else's platform**, and it **won't be a people-management role** — I'm an individual contributor and want to stay that way for this next move. My value is in technical depth, systems thinking, and influence-without-authority across large cross-functional groups, not in managing direct reports.

---

## What "great match" looks like

A role I'd prioritize applying to has most of these:

| Dimension | Signal |
|---|---|
| **Title** | Senior / Sr. Staff / Principal Product Manager — Platform / Technical / Infrastructure / Integration / API |
| **Scope** | Owns a platform area end-to-end (vision → architecture → adoption), not a feature on top of one |
| **Platform type** | Integration platform, API platform, multi-stakeholder platform, internal developer/operations platform, B2B platform, marketplace, FinTech rails / ledger / payment infrastructure |
| **Stakeholders** | Multi-stakeholder (external partners + internal teams), or large cross-functional groups |
| **Technical depth expected** | Comfort discussing data models, API contracts, system architecture; engineers want this PM in the room |
| **Company stage** | FAANG, public tech, or Series C+ growth-stage with established H1B sponsorship (US) — any UK employer (no visa filter) |
| **Geo** | Seattle, San Francisco / Bay Area, or London (in-person, hybrid, or remote all OK) |

---

## What "weak match" or skip looks like

The agent should **down-rank or filter out** roles that look like:

- People-management / EM-style roles (any title with "Manager of PMs," "Head of," "Director" implying direct reports)
- Pure feature-PM roles (PM owns one feature on top of an existing platform; no architecture or platform-level scope)
- Pure consumer social platforms (Instagram, TikTok, Snapchat — unless the role is explicitly *internal platform / infrastructure* at one of these)
- Pure infrastructure/SRE PM roles requiring deep compute/storage/networking background (different domain than my integration-platform experience)
- US roles at companies with no H1B-PM sponsorship track record (Series A–B startups, smaller agencies)
- Generic "Product Manager II" / "Associate PM" roles — wrong level

---

## Companies and stages I'm targeting

**Primary targets** (see `COMPANY_LIST_PUBLIC.md` for the public tiered framework; the named per-tier list is in the local working copy):
- Big Tech / Public US tech employers with platform / integration / API PM roles in scope and an established H1B-PM sponsorship track record
- Growth-stage FinTech (Series C+) — payment platforms, B2B fintech rails, embedded finance, banking-as-a-platform, BNPL, marketplace platforms
- B2B SaaS — any Series C+ with platform / API products
- UK / London — public tech and growth-stage employers in B2B SaaS / FinTech (no visa filter)

I'm also **open to companies not on the named list** if a Senior Platform PM role surfaces that strongly maps to my experience — the agent's discovery mode (LinkedIn / TrueUp / YC / VC portfolio boards) should catch these.

---

## Geography & visa rules (HARD constraints)

- **Seattle, WA** — open
- **San Francisco / Bay Area** — open
- **London, UK** — open
- **Anywhere else** — skip
- **US roles** — hard-filtered against the H1B-PM sponsorship track record maintained in the local working copy of `COMPANY_LIST.md`. Roles at companies without a credible track record get a ⚠️ verify flag rather than auto-including.

---

## My positioning (for the matcher to score against)

**Primary narrative:** *Platform Product Manager with deep expertise building integration platforms, API products, multi-stakeholder systems, and regulatory product frameworks at scale. 7 years PM (11 years total). Consolidated 5 legacy systems into a unified platform serving 1,000+ external partners and 15+ internal teams at Amazon, designed 3-layer platform architecture with custom API suite, defined the global e-invoicing reference blueprint adopted across Amazon FinAuto's AP space, and delivered measurable impact across four flagship platform initiatives.*

**Four flagship project anchors** (the matcher should map JD requirements to whichever of these is most relevant):

1. **WFM Vendor Central Integration Platform** (lead for: integration / API / multi-stakeholder / platform consolidation roles)
   - 5 systems → 1 unified platform; 1,000+ external suppliers + 15+ internal teams
   - 3-layer architecture (Presentation → Transformation → Data)
   - 3 core APIs (Item Registration, Mapping Lookup, Bulk Sync)
   - ID transformation system (ASIN ↔ UPC ↔ PLU)
   - 90% onboarding-time reduction (8 weeks → 7 days); 80%+ adoption
   - **Total cost discovered during initial project discovery: $20M** (the cost-savings opportunity that justified the program)
   - **Revenue impact at 12–18 months post-launch: up to $17M generated through suppliers due to platform convergence**

   **Problem-shape framings (illustrative, not exhaustive — for situational matching when JDs describe the same underlying work in different domain vocabulary):**
   1. *Consolidate multiple legacy systems (5+) into a unified platform without disrupting live external partners (1,000+)*
   2. *Productize reusable platform capabilities (APIs, services, data contracts) for internal teams with explicit governance + adoption mechanisms*
   3. *Sequence a multi-year platform migration so the business keeps shipping while the infrastructure improves underneath*
   4. *Design a layered abstraction architecture (presentation / transformation / data) that decouples upstream complexity from downstream API consumers*
   5. *Build the data-model bridge between an internal source-of-truth and external partner vocabularies, so both can operate on shared truth without per-partner one-off integrations*
   6. *Drive 0 → 80%+ adoption of a new internal platform across 15+ teams without top-down mandate*
   7. *Design identifier-translation logic (ID-mapping) that lets systems with different native identifier schemes reconcile without manual intervention*
   8. *Ship the API contracts that became the integration foundation for an external partner ecosystem (1,000+ partners onboarding 8w → 7d)*

2. **Mexico Tax Reconciliation Automation Platform** (lead for: data / operations / FinTech platform roles)
   - Multi-system integration: Amazon payment systems + Mexican government tax portal
   - 36-attribute data architecture, 72% → 89% accuracy, $1.8M annual savings
   - Eliminated 90-person manual process

   **Problem-shape framings (illustrative, not exhaustive):**
   1. *Build multi-system reconciliation between an internal source-of-truth and an external regulated counterparty (e.g., a government tax authority) where the counterparty defines the schema you must conform to*
   2. *Define a multi-attribute data architecture (36+ attributes) that maps disparate schemas onto a common canonical model*
   3. *Move accuracy from a low baseline (~70%) to a compliance-grade threshold (~90%) via controls and validation framework — through better data architecture, not more headcount*
   4. *Replace a labor-intensive manual ops workflow (90+ FTEs reading + reconciling) with an automated platform — eliminate the people-as-API pattern*
   5. *Build the data-integrity layer that lets two systems with no native interoperability operate on shared truth, with audit trails for compliance*
   6. *Lead a regulated-data product where the external counterparty defines the schema you must conform to, with no negotiation power*
   7. *Design the reconciliation pipeline that surfaces discrepancies before they become compliance violations*

3. **AI Invoice Automation Platform** (lead for: AI/ML / automation / process platform roles)
   - OCR + ML platform processing 3M+ invoices/year
   - Template-based architecture (3.5M invoices → 80 formats → 25 pilot templates)
   - 80%+ accuracy vs. 75% manual baseline; scaled 5 → 320 suppliers; $2M savings; 92% processing-time reduction

   **Problem-shape framings (illustrative, not exhaustive):**
   1. *Replace a manual / vendor-based classification process with an in-house ML system, in production, without disrupting live business operations*
   2. *Design a template-based architecture that compresses massive variation (millions of inputs) into a manageable taxonomy (tens of templates) — engineering investment in templating + structure, not in novel modeling*
   3. *Scale a niche pilot to broad production deployment (5 → 320 suppliers) while maintaining quality bar (80%+ accuracy vs. 75% manual baseline)*
   4. *Build the ML platform that beats the manual baseline on the metric that matters — accuracy at scale, not just throughput*
   5. *Compress process time by orders of magnitude (days → hours, 92% reduction) via OCR + ML integration*
   6. *Define the data-extraction architecture for unstructured input (invoices, semi-structured documents) at scale (3M+ documents/year)*
   7. *Lead the AI/ML productization where the engineering investment is in structure + templating rather than in novel modeling — pragmatic AI, not research AI*

4. **Global E-Invoicing Platform Framework / FinAuto** (lead for: invoicing / billing / e-invoicing / tax-compliance / multi-country product launch / regulatory product roles)

   **Design phase — facts from the May 2022 Blueprint:**
   - Defined Amazon's global e-invoicing reference blueprint covering the inbound invoice lifecycle across 4 functional domains: **Ingestion, Processing, Booking, Reporting & Reconciliation**
   - Authored **7 recommended solution patterns (RS1–RS7)** mapping clearance models (open vs. closed) and government-API availability to specific tech architectures
   - Cataloged **27 product features (C1–C27)** across the inbound lifecycle with status, ownership, and applicable countries
   - Reference country scope: **Brazil, Mexico, Poland, Turkey, Italy, Egypt, India** — covering both open and closed e-invoicing clearance models
   - **Cross-org workgroup**: PMs across GIS, FinAuto, SPFT, FinTech, with contributions from Tax PMO, FinOps BP, E-Program. **12 working sessions** between 2022-02-14 kickoff and May 2022 publication
   - Long-term framework adoption mechanism: E-invoicing Steering Committee + centralized E-Invoice Wiki + framework evaluation gate at each new project intake

   **Post-launch outcomes (12–18 months after launch and scaling):**
   - **5–6 country deployment** (KSA, Poland, Egypt, etc.) serving **tens of thousands of business users**
   - **Reduced invoice rejection rates from 37% to under 10%**
   - **Cut processing time from 2 days to 2 hours** for clean invoices
   - **$25–30M annual reduction in vendor overpayments** across deployed markets
   - **7 pre-configured solutions (RS1–RS7) adopted by 15+ countries**
   - **Reduced new-country launch effort from 20+ engineering weeks to under 10 engineering weeks** (Blueprint set this as the design-phase target; achieved post-launch)

   **Problem-shape framings (illustrative, not exhaustive):**
   1. *Define the reference framework that disparate cross-org teams adopt as the shared standard — not a recommendation, a load-bearing standard*
   2. *Author governance + intake-gate mechanisms (steering committee + framework evaluation gate at each new project intake) that scale a framework across many markets without per-instance redesign*
   3. *Compress per-deployment effort (engineering weeks → fraction; 20+ → <10 weeks per country launch) by pre-defining solution patterns*
   4. *Lead the regulatory / compliance product framework that bridges multiple jurisdictions' divergent requirements (open vs. closed clearance models, government-API availability, etc.)*
   5. *Define the cross-functional product taxonomy (4 functional domains × 27 cataloged features) that becomes the org's shared vocabulary for the problem space*
   6. *Author the multi-country product launch playbook where each country's deployment is parameterization of an existing framework, not greenfield design*
   7. *Drive cross-org PM collaboration (5+ partner orgs, 12 working sessions over 3 months) to land a single framework all parties adopt*
   8. *Build the steering-committee + evaluation-gate machinery that keeps a platform framework load-bearing over time*

---

## Resume selection guidance

The agent reads from two distinct resume sets, depending on which step it's in.

### Step 1 — Initial JD ranking & scoring (every role)

The scoring step uses **only** the two top-level base resumes plus this brief — it does **not** read the local-only tweaked-resume repository. Mixing tweaked variants into the scoring context would muddy the signal of "what my actual experience looks like."

| Base resume | Path |
|---|---|
| Platform-PM-optimized base | `Ayesha Resume/Ayesha Base Platform PM.docx` |
| Generic 1-page PM base | `Ayesha Resume/Ayesha Ghoshal_Resume_2026.pdf` |

### Step 2 — Asset matching (roles scored ≥ 7/10)

For roles that pass scoring, the asset matcher picks a **starting resume** plus suggests bullet-level tweaks against the JD. The candidate set is wider here:

1. **The two base resumes above** (default starting points)
2. **Any past tweaked resume in the local-only resume repository** — these are real resumes I've previously used for actual applications, kept as a starting library so we don't draft from scratch each time. If one is materially closer to the current JD than either base resume, prefer it as the starting point and explain why in the recommendation.

**Default routing between the two base resumes:**

| If JD emphasizes... | Start from |
|---|---|
| Platform architecture, APIs, integration, multi-stakeholder, B2B platform, marketplace | `Ayesha Base Platform PM.docx` |
| Broader PM / digital transformation / mixed B2B-B2C / FinTech generally | `Ayesha Ghoshal_Resume_2026.pdf` |
| Hybrid / unclear | Default to Platform PM resume; flag for manual review |

**Default routing if a tweaked resume in the local-only repository is a closer fit:**

These are real past-application resumes pre-optimized for a specific domain. The repository is gitignored (kept local-only); the asset matcher reads it during the local scoring pass. Prefer them over the bases when the JD strongly matches:

| If JD primarily emphasizes... | Prefer starting from... |
|---|---|
| Identity / authentication / OAuth / federated identity / regulated or sensitive data | Domain-tailored variant (identity / auth) |
| Invoicing / billing / B2B get-paid workflows / multi-country product launch / e-invoicing / tax compliance | Domain-tailored variant (invoicing / e-invoicing) |
| Financial systems / payment rails / ledger / merchant identity / fintech infrastructure / vendor-to-AI migration | Domain-tailored variant (fintech / payment infra) |
| Data operations / workflow orchestration / human-in-the-loop / RLHF / data-production tooling | Domain-tailored variant (data ops / human-in-the-loop) |

⚠️ Each routing rule above is currently grounded in **1 confirmed past-application example**. As more (JD ↔ tweak) pairs are analyzed, confidence will grow. Treat each as a strong starting hypothesis, not a deterministic match. The matcher should always **explain why it picked the resume it did**, citing JD signals.

**Bullet-level tweaks:** for any role scored ≥ 7/10, also recommend specific tweaks to better mirror the JD's keywords (e.g., if JD says "developer experience," surface the NPS +35-40 and onboarding 8w→7d numbers; if JD says "platform consolidation," surface the 5→1 system bullet). Per `CLAUDE.md` Rule 3, never invent or inflate metrics — quote only numbers that already appear in the source resume or in `Product Experinces/`.

### Tweaking patterns (apply on top of any starting resume)

These are the patterns derived from 4 analyzed past-application (JD ↔ tweak) pairs. The asset matcher should apply these consistently:

1. **Headline domain swap** — replace the headline domain noun(s) with the JD's primary domain term(s). Examples seen: *"integration platforms"* → *"data operations platforms"*; *"platform architecture"* → *"identity & access infrastructure."*

2. **Bullet retitle for domain alignment** — at least one Amazon experience bullet's title gets reworded to mirror the JD's primary domain term. The Mexico Tax Recon bullet is the most flexible — it has been retitled to *"Payments & Regulated Data Platform,"* *"Financial Operations & Payment Reconciliation,"* and *"Data Ingestion, Pipeline Design & Quality"* depending on JD.

3. **Skills band re-leading** — reorder the skills section so the most JD-relevant band leads. For roles outside the canonical platform-PM identity (e.g., a domain-specific PM role like invoicing), the lead band may be entirely replaced with a JD-specific one.

4. **Bullet reordering** — position 1 should be the project most aligned with the JD's primary domain. If the JD aligns with the integration-platform story, keep the canonical order; otherwise, surface the matching project (AI/ML, identity, invoicing, etc.) to position 1.

5. **JD-language echoes** — embed 1–3 verbatim or near-verbatim phrases from the JD into bullets (*"comfortable working in ambiguity,"* *"human-in-the-loop,"* *"self-service,"* etc.). Surface phrasing only when the underlying experience genuinely supports it — never to fake a match.

6. **UK address swap** — for UK-based roles, change the address header to *"London, UK (relocating from Seattle)."*

**Authenticity guardrails (per `CLAUDE.md` Rule 1 + Rule 3):**
- Use only the numbers from the "Four flagship project anchors" section above. If a tweaked resume in the local-only repository cites a different number for the same project, treat the figure in this brief as canonical.
- Never invent project scope, impact figures, or claims.
- If a tweak surfaces work that's hard to defend in a technical interview, flag for manual review rather than encoding it.
