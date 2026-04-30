# Company List — Framework (public copy)

> **What this file is:** The structural framework used by the job-scraping agent's targeted scraper to decide where to look for roles. The working copy with named per-tier targets and an H1B-status field per company is kept local-only — see `COMPANY_LIST.md` in the project's local working tree (gitignored).
>
> **Why the split:** Specific company targeting and an H1B-PM sponsorship track record per company are personal/strategic data not appropriate for a public portfolio repo; the tiering and filter framework are PM design choices that benefit from being visible.
>
> **Sync rule:** Per `CLAUDE.md` Rule 7, framework changes to the local working copy (new tier, new sub-tier, changed filter logic) must be reflected here in the same edit. Adding / removing specific companies inside an existing tier does not propagate.
>
> **Last updated:** 2026-04-30 (initial public copy)

---

## Tier 1 — Strong Match (priority scrape, prioritize applications)

### Big Tech / Public — US
Public US tech employers with platform / integration / API / multi-stakeholder PM roles in scope, and an established track record of H1B-PM sponsorship. Geo focus: Seattle and SF Bay.

### FinTech growth-stage — US (Series C+)
Series C+ US FinTech companies with platform PM roles — payment platforms, B2B fintech rails, embedded finance, BNPL, banking-as-a-platform, card-issuing — where H1B-PM sponsorship is plausible but per-company verification is required. Geo focus: SF Bay.

### Big Tech / Public + Growth — UK / London (no visa filter)
UK-based public tech and growth-stage employers in B2B SaaS / FinTech with platform / integration PM roles in scope. London geo focus; no visa-eligibility filter applies for this market.

> *Specific named targets per sub-tier are maintained in the local working copy.*

---

## Tier 2 — Moderate Match (worth scraping; apply with positioning)

### US
Public US tech and later-stage growth-stage companies with relevant platform PM roles, where positioning and cover-letter framing matter more than for Tier 1 (domain adjacency, less direct fit, or H1B-PM track record needs verification).

### UK / Europe
UK / European growth-stage banking, FinTech, and open-banking platform companies; smaller in scale than Tier 1, but platform-PM relevant.

---

## Tier 3 — Stretch (apply only with strong positioning / cover letter)

Roles where the platform domain or technical depth is adjacent to my experience and the application requires a strong custom cover-letter bridge. Examples include pure developer-platform / API-product roles, deep-infrastructure platform roles, and pure data-platform PM roles.

---

## Skip / Avoid

- **Pure consumer social platforms** — wrong domain; exception: their internal platform / infrastructure teams
- **US startups < 200 employees** — H1B sponsorship risk too high
- **Companies known not to sponsor PM H1Bs** — track record indicates won't transfer

---

## Discovery mode — sources

Beyond the named-company scrape, the agent pulls from these **aggregator boards** so we catch growth-stage companies I haven't thought of:

### Always-on aggregators
- **LinkedIn** (via Apify) — title + geo + posting-age filters
- **TrueUp** (truup.com) — Tech-focused aggregator, already part of my manual workflow

### Startup / VC-backed boards (covers growth-stage companies not on the named list)
- **Y Combinator's Work at a Startup** (workatastartup.com) — YC portfolio companies, all stages; useful for catching YC growth-stage cos.
- **Wellfound** (wellfound.com, formerly AngelList Talent) — Broad startup coverage with stage + role filters
- **A16Z portfolio jobs** (a16z.com/jobs) — Andreessen Horowitz portfolio, leans growth-stage
- **Sequoia Capital portfolio** (sequoiacap.com → portfolio job pages, may scrape via Sequoia Talent)
- **Index Ventures portfolio** — Heavy in European FinTech; relevant for London search
- **Accel portfolio jobs** — Growth-stage tilt
- **Bessemer Venture Partners** — Strong B2B SaaS portfolio
- **Insight Partners** — Late-stage growth, B2B SaaS heavy

### Filters applied to all discovery sources
- Title: contains "Product Manager" + level keywords (Senior / Staff / Principal)
- Location: in geo allowlist (Seattle, SF Bay, London)
- Posting age: ≤ 14 days
- Hard filters from `HARD_FILTERS.md` (no manager titles, IC-only, etc.)
- US roles: H1B status check against the local working copy's named list; unlisted companies get ⚠️ flag (research before applying)

Roles from companies *not* on the named list pass through scoring with a `discovery: true` flag. If one scores ≥ 7/10, **promote that company into Tier 1 or Tier 2 by editing the local working copy of this file**.

> **Note on VC portfolio boards:** Many VCs publish portfolio job pages via Greenhouse/Lever/Ashby aggregators. I'll figure out the most reliable scrape path for each in Session 2 when I write the code — some are well-structured, some aren't. If any prove unscrapeable, we either drop them or write a one-off Apify scraper for ~$5/mo.

---

## Referral Network — companies where I have a contact who could refer me

> **What this section does:** Companies listed in the local working copy **bypass the applicant-noise penalty** in `SCORING_PROMPT.md` (the −1 score deduction for >7-day-old roles with 100+ applicants). Reason: a referral routes around the cold-applicant queue, so applicant volume is no longer a meaningful signal — the application enters via a different channel.
>
> **Format (in the local working copy):** company name on each line, one per row. The matcher reads `companyName` from the scraped JD and matches against this list, so use the company's official name as it appears on LinkedIn.
>
> **Maintenance:** add companies in the local working copy as the network grows. Remove if a contact leaves or the relationship goes cold.

> *Specific company list maintained in the local working copy of this file.*

---

## Companies to research and add (parking lot)

> Add candidates here when I think of them; I'll triage into tiers later.

> *Maintained in the local working copy.*
