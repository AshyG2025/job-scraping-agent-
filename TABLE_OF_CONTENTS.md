# Table of Contents — Where Things Live + When to Use Them

> **What this file is for:** This is your navigation map. The project has ~12 docs across the root + `docs/` folder, and each one controls something specific. Use this file when you've forgotten where something lives, when you're starting a workflow you haven't done before, or when you're orienting a future Claude session that hasn't seen this project yet.
>
> **How to read it:**
> - **Section 1 (Quick lookup)** — start here. "When X happens, go to Y." This is what you'll use 90% of the time.
> - **Section 2 (Each file & folder explained)** — deeper reference. What each file does, how to use it, and concrete use cases.
> - **Section 3 (When to consult this TOC)** — meta — when to open this file in the first place.
>
> **Last updated:** 2026-05-09 (Added `Ayesha Resume/Cover Letters/` subfolder for per-application cover letters; gitignored alongside the existing `Resume to use repository/`. Section 2 `Ayesha Resume/` sub-section updated to document the new folder. First cover letter saved: Visa Sr PM — Post Purchase Data Integrations & AI. Earlier 2026-05-09: Eval set: added Posting 9 — Wise Sr PM Cards Pay-in Orchestration. Recruiter reached out 2026-05-09 + HM call scheduled week of 2026-05-12 → callback-anchored target **9** (matcher scored 8 in the Session 3.1 LinkedIn first-firing). First eval-set entry surfaced via the discovery channel itself. EVAL_SET.md + EVAL_SET_JDS.md updated; eval-run cost bumped 8 × $0.12 → 9 × $0.12 = ~$1.08. JD body re-fetched live from the Wise SmartRecruiters API since MANUAL_JDS.md had been cleared. **Note:** SCORING_PROMPT.md §"Calibration: anchor against the gold set" calibration table is **stale** (still lists 6 of the original postings, missing Snorkel + Zillow/FUB + Wise Cards Pay-in, and Liberis is mis-stated at 8 not 9 post-callback). Updating that table is out-of-scope for this change because the project convention requires a prompt-version bump + full eval re-run when SCORING_PROMPT.md changes — flag as separate work. Earlier 2026-05-08 (Apify LinkedIn discovery channel SHIPPED — Phase B leftover #1. New: `scripts/scrapers/linkedin_apify.py` (Ashby pattern: descriptionHtml inlined, no second round-trip), `apify-client>=1.8.0` in `requirements.txt`, `APIFY_API_TOKEN` in `.env`, 3 LinkedIn `/jobs/search` URLs added to `SOURCES` (Seattle / SF Bay / London, all `keywords=Product Manager` + `f_E=4` Mid-Senior + `f_TPR=r2592000` last 30 days), 67 results per source = ~$0.20/run × 2x/wk = ~$1.60/mo. Companies aren't tied to `COMPANY_LIST.md` tiers — Phase C tier lookup falls back to "discovery" automatically. `run_scrapers.py` now `load_dotenv()`s at top so future scrapers needing secrets work the same way. Earlier 2026-05-07 (Phase C — Google Sheets storage SHIPPED. New: `scripts/sheets.py` (writer), `scripts/check_sheets.py` (connection diagnostic), `docs/PHASE_C_SETUP.md` (one-time setup walkthrough). `scripts/score_jobs.py` now appends every scored role to the configured Google Sheet (Decision 3: keep both JSON + Sheet) with the locked 31-column layout (groups A→B→D→C, sub-scores split out, source + tier auto-filled, score_at_application + prompt_version_at_application as Sheet formulas that auto-copy when `applied=Yes`). Sort: scored_date DESC, final_score DESC. `requirements.txt` adds `gspread` + `google-auth`. Earlier 2026-05-07 (small base resume update — commit f7d806e): WFM bullet $9.6M → $17M; FinAuto bullet 3.5M / 80 → 3M / 320 supplier formats. Earlier 2026-05-03 (Session 2.3 — WFM flagship #1 overhaul: PROJECT_BRIEF.md + PROJECT_BRIEF_PUBLIC.md flagship #1 (WFM Vendor Central Integration Platform) rewritten against `Product Experinces/Supplier deep dive_Prep_v3.docx`. Architecture corrected ("3-layer" → "monolith-first with three planned service extractions"); API claim corrected ("3 named APIs from day one" → "pilot was portal-only, programmatic APIs progressive in Wave 2"); scaling curve added (5 → 150 → 450 → 900 → 1,000+ over 18 months); $600K pilot outcome / team size / churn-NPS metrics added; $20M/$17M canonical reconfirmed by user. **10 new problem-shape framings (#9–#18)** added to flagship #1 (8 → 18) — unlocks distributed-systems, multi-tenant SaaS, ledger-migration, config-platform JD recognition. Stale "Three flagship" comment fixed. Resume non-update settled (user corrects $9.6M → $17M per-application). New memory `project_wfm_canonical_reconciliation.md` captures the resolution. Earlier 2026-05-03 (Session 2.2.2 + post-rerun cleanup): (a) added Posting 7 Snorkel.AI Sr PM Platform (Bay Area, H1B confirmed direct from HM + recruiter, target 9 — HM-callback after warm referral); (b) added Posting 8 Zillow/FUB Sr PM AI Platform & Ecosystem (Seattle, H1B sponsor, initially targeted 8 then retuned 8 → 7); (c) upgraded Posting 3 Liberis 8 → 9 after recruiter callback. Documented callback-anchor Δ -1 convention in EVAL_SET.md "How to use". New Tier 1 sub-section "AI / Data infrastructure growth-stage — US (Series C+)" added to COMPANY_LIST.md (Snorkel) + mirrored to PUBLIC. Women in Tech Jobs added to Always-on aggregators. Eval set 8 entries: 6 perfect Δ 0, 1 expected callback-anchor Δ -1 (Snorkel), 1 retuned to Δ 0 (Zillow). Periodic Sheets → Eval-set feedback loop logged to memory for Phase C activation. Earlier 2026-05-02 (Session 2.2.1): extracted 6 eval-set JD bodies from `Job Posting samples/JD mapping to my exp..docx` into `docs/EVAL_SET_JDS.md` — calibration is now runnable end-to-end via `cat docs/EVAL_SET_JDS.md >> MANUAL_JDS.md && python scripts/score_jobs.py`, no longer dependent on original postings still being live. Earlier 2026-05-02 (Session 2.2): added "Problem-shape framings" sub-block to each of the 4 flagships in `PROJECT_BRIEF.md` + `_PUBLIC.md` (30 framings total); `SCORING_PROMPT.md` v1.0 → v1.1 with new "Situational matching — read the problem-shape, not just the keywords" section + 4 explicit guardrails. Calibration: Liberis 9, Wise Treasury 9, PayPal 8, Salesforce MuleSoft 7 (-1 from v1.0; guardrail working). Earlier Session 2.1.4: Ashby module shipped at `scripts/scrapers/ashby.py` covering Ramp + Deliveroo (Tier 1). SOURCES now 30 named-co scrapers (28 → 30). Ashby's listing endpoint inlines `descriptionHtml`, so `fetch_jd_body()` returns a cached value — no second HTTP round-trip per job. First live run: 1 net-new JD (Deliveroo Staff PM, Ads, London). Earlier 2026-05-01: Session 2.1.3: Workday module at `scripts/scrapers/workday.py` covering 8 tenants — Visa, PayPal, Salesforce, Zillow, Target, Capital One, Walmart, Zoom. Module contract refactored: `fetch_listing` / `fetch_jd_body` take the full source dict instead of `(slug, company_name)`. SOURCES bulk-expanded to 28 named-co scrapers — Tier 1 + Tier 2 ATS recon + Boku added to COMPANY_LIST.md Tier 1 UK/London. Welcome to the Jungle added to discovery aggregators. Earlier 2026-04-30: Phase B shipped: `scripts/run_scrapers.py` orchestrator + `scripts/scrapers/` package with `common.py`, `greenhouse.py`, `smartrecruiters.py`; QC_PROCESS gains a 30-sec scraper-volume sanity check; requirements.txt adds `requests`. Same day: portfolio prep — gitignored `MANUAL_JDS_PROCESSED.md`, `Ayesha Resume/Resume to use repository/`, `COMPANY_LIST.md`, `PROJECT_BRIEF.md` as local-only working copies; added committed `*_PUBLIC.md` framework copies; added CLAUDE.md Rule 7; refreshed README Status + added platform-PM-lens framing subsection)

---

## 📍 Section 1 — Quick lookup (by trigger)

The most common workflows you'll do, and exactly where to go.

### Daily / weekly use

| When this happens... | Go to... | What you'll do (~time) |
|---|---|---|
| It's my Tuesday/Thursday-morning routine | `python scripts/run_scrapers.py && python scripts/score_jobs.py` | Auto-scrapes the named-co list **+ runs the Apify LinkedIn discovery channel (3 geo searches)**, filters, scores survivors, **appends rows to the Google Sheet** (Phase C). ~10–15 min + ~$1.20 per run (~$1 Anthropic + ~$0.20 Apify). |
| I saw a JD on LinkedIn (or anywhere) the auto-scrapers missed | `MANUAL_JDS.md` → run `python scripts/score_jobs.py` | Paste the JD; runner scores it, writes `_local/digest.md`, and appends a row to the Sheet (~30 sec/JD) |
| I receive the digest email | Email inbox + Google Sheet | Read top matches; mark `applied` Yes/No in the Sheet (~5 min) |
| I just applied to a role | Google Sheet | Update `applied=Yes`, `applied_date`, `outcome_status: open`. **`score_at_application` + `prompt_version_at_application` auto-fill** via Sheet formula (no copy-paste needed) (~30 sec) |
| A recruiter responded / I got a phone screen / interview / offer / rejection | Google Sheet | Update `outcome_status` + `outcome_date` + optional `outcome_notes` (~1 min) |
| I want to look at a role's full reasoning trace | Google Sheet → `qc_deep_dive_url` column → opens `_local/scored_results.json` | Read; sanity check the score |
| I disagree with a specific score | Comment in Google Sheet for now → flag at next monthly QC | (See below) |
| The Sheet didn't update after a scoring run | `python scripts/check_sheets.py` | One-line connection diagnostic; tells you which step of the Phase C setup broke (~5 sec) |

### Adding / changing what the agent looks at

| When this happens... | Go to... | What you'll do |
|---|---|---|
| I learn about a new company I want to track | `COMPANY_LIST.md` | Add a bullet under the right tier; commit |
| I want to drop a company entirely | `COMPANY_LIST.md` | Move to `Skip` section or delete; commit |
| I now have a contact who could refer me at company X | `COMPANY_LIST.md` § Referral Network | Add the company; bypasses the applicant-noise penalty in scoring |
| I want to broaden / narrow geography | `HARD_FILTERS.md` § 3 | Edit the geo allowlist; commit |
| I want to filter out a title pattern | `HARD_FILTERS.md` § 1 or 2 | Add to drop list; commit |
| I want to change cadence (run more / less often) | `.github/workflows/scrape.yml` *(Session 2)* | Edit the cron line |

### Tuning the matcher

| When this happens... | Go to... | What you'll do |
|---|---|---|
| I want to change scoring weights | `SCORING_PROMPT.md` § Tunable Parameters (top) | Edit weights, bump prompt version, re-run eval |
| I want to change asset-match threshold (default 7) | `SCORING_PROMPT.md` § Tunable Parameters | Edit `asset_match_threshold` |
| A scored role disagreed with my judgment | `docs/EVAL_SET.md` | Add it as a labeled example with target score |
| The matcher misunderstood a flagship project | `PROJECT_BRIEF.md` § "My positioning" | Tighten the project description |
| The matcher's reasoning is keyword-matching not substance | `SCORING_PROMPT.md` § dimension definitions | Refine the dimension(s) |
| I want to refresh how I describe my ideal role | `PROJECT_BRIEF.md` § Role brief | Edit; commit |

### Monthly + drift events

| When this happens... | Go to... | What you'll do |
|---|---|---|
| It's the 1st of the month + I get the QC email | `docs/qc-reports/YYYY-MM.md` | Run the 15–20 min ritual in `QC_PROCESS.md` |
| Calibration is **inverted** (🚨 alert) | `docs/CALIBRATION_DEEP_DIVE.md` | Run the 6-phase, 60–90 min deep-dive with Claude Code |
| I want to add an outcome-validated example to gold set | `docs/EVAL_SET.md` | Append posting + target score; mark in current QC report |
| I want to see how scoring has changed over time | `git log docs/qc-reports/` + `SCORING_PROMPT.md` § Iteration log | Browse history |

### When working with Claude

| When this happens... | Go to... | What you'll do |
|---|---|---|
| Claude isn't being accurate / is hallucinating | `CLAUDE.md` § Rule 1 | Re-read; if rule isn't strong enough, refine |
| Claude is using too much jargon | `CLAUDE.md` § Rule 2 | Reinforce or add a rule |
| Starting a fresh Claude Code session | This file (`TABLE_OF_CONTENTS.md`) | Tell Claude: "Read TABLE_OF_CONTENTS.md and CLAUDE.md before doing anything else" |
| I want a quick command / prompt I've seen before | `QUICK_COMMANDS.md` | Scan the cheatsheet by category — Claude will also auto-surface matching entries |
| Claude proposed a new useful command/prompt | (Claude auto-adds to `QUICK_COMMANDS.md` per Rule 6) | Just confirm the entry looks right |

### Resume / cover letter work

| When this happens... | Go to... | What you'll do |
|---|---|---|
| I need to choose between my two resumes for a role | Digest email's `resume_choice` recommendation OR `PROJECT_BRIEF.md` § Resume selection guidance | Use the suggestion; check rules manually if borderline |
| I want to update my resume | `Ayesha Resume/` | Replace the file(s); also update `PROJECT_BRIEF.md` § Three flagship project anchors if metrics changed |
| I want to remember a project's actual metrics | `PROJECT_BRIEF.md` § Three flagship project anchors OR `Product Experinces/` | Reference (these are source of truth — never invent numbers) |
| I want to use my detailed analyzer prompt manually for a role | `Job Posting samples/Platform PM Role ANALYZER - Instructions.docx` | Copy + run in Claude.ai |

---

## 📁 Section 2 — Each file & folder explained

### Root-level docs

#### `README.md`
- **What it is:** The "front door" of the project. Plain-English description of what the agent does, the pipeline diagram, the file map, and current status.
- **How to use it:** Read first when you (or anyone else) want to understand the project at a glance.
- **Use cases:**
  - Showing this project to someone — give them README first
  - You forgot the high-level structure and need a refresher
  - Future Claude session needs orientation (point it here + this TOC)
- **When to edit:** When the project's status changes (new milestones, new sources added, V2 features shipped)

#### `CLAUDE.md`
- **What it is:** Project-specific rules Claude Code reads at the start of every session in this folder. Currently covers: accuracy/verification, non-developer audience, authenticity over polish, memory upkeep.
- **How to use it:** Treat as your "house rules" for AI collaboration. If Claude is doing something annoying or risky, the fix usually goes here.
- **Use cases:**
  - Claude is hallucinating company names → already covered by Rule 1; reinforce if needed
  - Claude is over-engineering / using jargon → covered by Rule 2
  - You want a new behavior — e.g., "always show me the file path before editing" → add a rule
- **When to edit:** Any time Claude's default behavior doesn't fit how you want to work

#### `TABLE_OF_CONTENTS.md` (this file)
- **What it is:** Navigation map for the whole project.
- **How to use it:** First file to open when lost.
- **Use cases:** See Section 3 below.
- **When to edit:** Every time you add a new file/folder, or change a workflow

#### `QUICK_COMMANDS.md`
- **What it is:** Cheatsheet of every command, prompt, and shortcut that's been useful in this project. Organized by what you're trying to do.
- **How to use it:** Either scan it directly, or rely on Claude to auto-surface matching entries (per `CLAUDE.md` Rule 6) when you describe a relevant situation.
- **Use cases:**
  - You forgot the kickoff prompt for a fresh session
  - You forgot how to test SSH auth, or the syntax for a git command
  - You want to know all the project-specific prompts (re-run eval set, run deep dive, etc.)
- **When to edit:** Claude appends new entries automatically when it suggests a useful pattern; you can also edit directly.

#### `PROJECT_BRIEF.md` *(gitignored — local-only working copy)*
- **What it is:** "Ideal next role" definition + flagship-project descriptions + resume-selection rules + comp expectations + named-company target list + file-pathed routing for tweaked-resume variants. The matcher's primary anchor. Read by the scoring runner (`scripts/score_jobs.py`) at scoring time.
- **How to use it:** Edit when your career direction shifts. Per `CLAUDE.md` Rule 7, propagate framework changes (role brief, great-match / weak-match criteria, geography rules, flagship metrics, resume-selection routing logic) to `PROJECT_BRIEF_PUBLIC.md` in the same edit.
- **Use cases:**
  - "What types of roles am I actually looking for?" → read § Role brief
  - "What did I do at Amazon, with real metrics?" → read § Four flagship project anchors
  - "Should this role's resume start from Platform PM or generic?" → § Resume selection guidance
- **When to edit:** Career-direction shifts (e.g., "I'm now also open to data platform roles"), updated metrics on flagship projects, comp expectations changing

#### `PROJECT_BRIEF_PUBLIC.md` *(committed to GitHub)*
- **What it is:** Genericized portfolio-friendly version of `PROJECT_BRIEF.md`. Comp expectations and named-company target lists removed; flagship project metrics preserved (per user instruction); resume routing anonymized to "Domain-tailored variant (X)" descriptors.
- **How to use it:** This is what GitHub portfolio viewers see. Don't edit by hand in isolation — keep in sync with `PROJECT_BRIEF.md` per `CLAUDE.md` Rule 7.
- **When to edit:** Whenever framework / criteria / flagship metrics in `PROJECT_BRIEF.md` change.

#### `COMPANY_LIST.md` *(gitignored — local-only working copy)*
- **What it is:** Tier 1/2/3/Skip named-company list + Discovery sources (LinkedIn, TrueUp, YC Work at a Startup, VC portfolio boards) + Referral Network. Source of truth for the H1B filter and for the targeted scraper. Read by the scoring runner at scoring time.
- **How to use it:** Add / remove companies in this local working copy; promote discovery roles into named tiers. Per `CLAUDE.md` Rule 7, propagate framework changes (new tier, new sub-tier, changed filter logic) to `COMPANY_LIST_PUBLIC.md` in the same edit. Adding / removing a specific company doesn't propagate.
- **Use cases:**
  - You read about a relevant acquisition → add to the right tier
  - You decide to deprioritize a sector → move to Skip
  - QC report flags a discovery-mode company surfacing 3+ strong matches → promote into a named tier
- **When to edit:** Anytime you learn of a new company; at every monthly QC

#### `COMPANY_LIST_PUBLIC.md` *(committed to GitHub)*
- **What it is:** Genericized portfolio-friendly version of the tier framework + discovery sources. Specific company names and the H1B-status field are stripped; tier descriptions, filter logic, and aggregator-board list are kept.
- **How to use it:** This is what GitHub portfolio viewers see. Don't edit by hand in isolation — keep in sync with `COMPANY_LIST.md` per `CLAUDE.md` Rule 7.
- **When to edit:** When framework structure changes in the local working copy (new tier, new sub-tier, changed filter logic) — not when a specific company is added / removed.

#### `HARD_FILTERS.md`
- **What it is:** Pre-LLM rules. Drops obvious no-go roles before they hit the (paid) Claude scoring step. Covers titles, geos, H1B, freshness, dedup.
- **How to use it:** Tighten when too much noise; loosen when missing roles.
- **Use cases:**
  - Too many people-management roles slipping through → tighten title filter
  - Missing London roles because filter only matches "London, UK" exact string → loosen geo
  - Discovery mode keeps surfacing 30-day-old roles → tighten freshness
- **When to edit:** Every time the digest contains roles that obviously shouldn't be there (or is missing roles that obviously should)

#### `SCORING_PROMPT.md`
- **What it is:** The brain. The system prompt sent to Claude API for every role that survives hard filters. Has Tunable Parameters block at top, 4-dimension framework, JSON output schema, calibration anchors.
- **How to use it:** Tune via the Tunable Parameters block. Bump version when you change anything. Re-run eval set after every change.
- **Use cases:**
  - Want to weight team-needs higher → edit `weights` in TUNABLE PARAMETERS
  - Asset matcher firing too often → raise `asset_match_threshold` from 7 to 8
  - Adding a new dimension (rare) → restructure schema, bump major version
- **When to edit:** Quarterly tuning; in response to QC findings; never casually

#### `APPLICATION_LOG.md`
- **What it is:** Schema + workflow doc for outcome tracking. Outcomes themselves live in the Google Sheet; this file documents what columns exist and how the feedback loop works.
- **How to use it:** Reference when you're not sure what to put in an outcome column. Read when you onboard onto monthly QC.
- **Use cases:**
  - "What does `outcome_status: phone_screen` actually mean?" → read this file
  - "Why is `score_at_application` frozen?" → read this file
- **When to edit:** Rare — only if you want to add a new outcome column or change the calibration approach

#### `QC_PROCESS.md`
- **What it is:** The monthly QC ritual playbook. What auto-runs, what you do manually, mid-month alerts, inversion trigger.
- **How to use it:** Open on the 1st of every month after receiving the QC email.
- **Use cases:**
  - Monthly QC review (~15–20 min)
  - You forgot what triggers an inline alert → § "When QC alerts go off mid-month"
- **When to edit:** If you change cadence (e.g., move to bi-weekly), add new alert triggers, or refine the ritual

### `scripts/` folder

#### `scripts/run_scrapers.py` *(Phase B orchestrator)*
- **What it is:** Reads the `SOURCES` list at the top of the file, runs the matching ATS-specific scraper for each entry, applies title/geo/age filters from `scrapers/common.py`, dedupes against `_local/scraped_seen.json`, and appends survivors to `MANUAL_JDS.md` as ready-to-score entries. Prints a per-source funnel summary (e.g. `Stripe: 491 total → 4 pass title → 4 pass geo → 2 pass age → 2 new`). Calls `load_dotenv()` at the top so per-module env vars (`APIFY_API_TOKEN` for `linkedin_apify`, future scraper secrets) are available before any module runs.
- **How to use it:** `source .venv/bin/activate && python scripts/run_scrapers.py` from the project root. Run before `score_jobs.py`.
- **Use cases:**
  - Tuesday/Thursday-morning routine before the scoring run
  - Adding a new company — append a dict to `SOURCES` (no other code change if the company uses an ATS we already support)
- **When to edit:** When adding a new company, or supporting a new ATS (then also add a module under `scripts/scrapers/` and an entry in `ATS_MODULES`).

#### `scripts/scrapers/` *(per-ATS scraper package)*
- **What it is:** Modular per-ATS fetchers. Each module exposes the same two functions (`fetch_listing(src)`, `fetch_jd_body(src, job)`) where `src` is the full source dict from `run_scrapers.py`'s `SOURCES` list. Each module reads whatever fields it needs from `src` (Greenhouse/SmartRecruiters/Ashby use `slug`; Workday uses `tenant`/`host`/`site`).
  - `common.py` — shared helpers: title/geo/age filter regexes (mirror of `HARD_FILTERS.md`, in a TUNABLE PARAMETERS block at the top of the file), HTML→text cleanup, dedup cache I/O, MANUAL_JDS.md entry formatting.
  - `greenhouse.py` — fetches jobs from Greenhouse-hosted careers pages via `boards-api.greenhouse.io` (no auth). Used for ~18 Tier 1 + Tier 2 cos (Stripe, Adyen, Airbnb, Bill.com, Boku, Brex, DoorDash, GoCardless, Liberis, Marqeta, Mercury, Monzo, Affirm, Block, Coinbase, Databricks, Modulr, Tide).
  - `smartrecruiters.py` — fetches jobs from SmartRecruiters-hosted careers pages via `api.smartrecruiters.com` (no auth, paginated list). Used for Wise + ServiceNow.
  - `workday.py` — fetches jobs from Workday-hosted careers pages via the public CXS JSON endpoint (no auth, paginated list, POST). Used for 8 Tier 1 + Tier 2 cos (Visa, PayPal, Salesforce, Zillow, Target, Capital One, Walmart, Zoom). Per-company config is `(tenant, host, site)` triple, not a single slug — Workday tenants live on different `wd1..wd103` cloud hosts.
  - `ashby.py` — fetches jobs from Ashby-hosted careers pages via `api.ashbyhq.com/posting-api/job-board/{slug}` (no auth, single GET). The listing endpoint **inlines `descriptionHtml`** for every job, so `fetch_jd_body()` returns a value cached on the listing dict — no second HTTP round-trip per job. Used for Ramp + Deliveroo (Tier 1).
  - `linkedin_apify.py` — **discovery channel** (companies aren't in `COMPANY_LIST.md`). Calls Apify actor `curious_coder/linkedin-jobs-scraper` synchronously per LinkedIn `/jobs/search` URL configured in `SOURCES`. Same Ashby trick: actor returns `descriptionHtml` inlined per result, cached on `_jd_html_cached`, no second round-trip. Per-source config is `search_url` (build in **incognito Chrome** — logged-in URLs return 0 results) + `max_results` (Apify enforces ≥10). Costs $0.001/result; current config is 3 sources × 67 results = ~$0.20/run = ~$1.60/mo at 2x/wk. Requires `APIFY_API_TOKEN` env var (loaded by `run_scrapers.py` via `python-dotenv`). Synchronous Apify run = 1–3 min per source, slower than the HTTP-based scrapers — that's the cost of LinkedIn coverage. Tier defaults to "discovery" in the Sheet.
- **How to use it:** Don't run modules directly — `run_scrapers.py` orchestrates them.
- **When to edit:**
  - Filter regex changes → edit `common.py` TUNABLE PARAMETERS block, then mirror the change to `HARD_FILTERS.md` to keep the spec in sync.
  - New ATS (Lever, Workable, PhenomPeople) → add a new module exposing the two-function contract, then add it to `ATS_MODULES` in `run_scrapers.py`.
  - New / changed LinkedIn search URLs → edit the LinkedIn block in `run_scrapers.py` `SOURCES`. Always rebuild URLs in incognito Chrome so they don't carry session params.

#### `scripts/score_jobs.py`
- **What it is:** The Phase A scoring runner. Reads JDs from `MANUAL_JDS.md`, sends each one to the Claude API along with `SCORING_PROMPT.md` + `PROJECT_BRIEF.md` + `COMPANY_LIST.md` as context (cached, so you only pay full price once per run), parses the JSON results, and writes:
  - `_local/scored_results.json` — raw structured data
  - `_local/digest.md` — human-readable summary
  - **Phase C:** also appends each scored role as a row in your Google Sheet via `scripts/sheets.py` (non-fatal if Sheet is unreachable — JSON write is still authoritative)
  - Appends processed entries to `MANUAL_JDS_PROCESSED.md` and clears `MANUAL_JDS.md` so the same JD isn't re-scored.
- **How to use it:** `source .venv/bin/activate && python scripts/score_jobs.py` from the project root. Reads your API key from `.env`.
- **Use cases:**
  - You pasted JDs into `MANUAL_JDS.md` and want to score them
  - You want to validate a `SCORING_PROMPT.md` change against a real JD (paste one, run, inspect)
- **When to edit:** When the scoring runner needs a feature change (new metadata field, different model, different output format). Tunables (model name, effort level, max tokens) live at the top of the file.

#### `scripts/sheets.py` *(Phase C — Google Sheets writer)*
- **What it is:** The library module called by `score_jobs.py` after the JSON write. Connects to the configured Google Sheet via service-account credentials, ensures the locked 31-column header is in row 1, builds one row per scored result, appends them via the Sheets API, and re-sorts the data range by `scored_date` DESC then `final_score` DESC. Embeds two self-referential formulas per row (`score_at_application` + `prompt_version_at_application`) so values auto-copy the moment `applied=Yes` is set, and the formulas survive sorting because Sheets API SortRange updates row references. Also contains the tier-lookup helper that parses `COMPANY_LIST.md` and matches each scored role's company to its tier (1 / 2 / 3 / discovery / unknown), with prefix + parens-alias handling.
- **How to use it:** Don't run directly — `score_jobs.py` calls it. For a quick connection check, use `scripts/check_sheets.py` instead.
- **When to edit:**
  - Adding / removing a column → edit `COLUMN_NAMES` and the matching slot in `build_row()`. Update the column-letter constants (`COL_APPLIED`, `COL_FINAL_SCORE`, `COL_PROMPT_VERSION`) if your edit shifts those columns.
  - Changing the sort order → edit `_sort_data_rows()`.

#### `scripts/check_sheets.py` *(Phase C — connection diagnostic)*
- **What it is:** Tiny one-off script. Loads `.env`, authorizes the service account, opens the configured Sheet, prints `✅ Connected. Sheet title: …` on success or a clear `❌` message pointing at the broken setup step on failure.
- **How to use it:** `python scripts/check_sheets.py`. Run it after `docs/PHASE_C_SETUP.md` Step 9, or any time `score_jobs.py` stops writing rows.
- **When to edit:** Almost never. If the diagnostic surfaces a new failure mode worth catching, add a labeled error case before the gspread auth call.

### Root-level files added in Session 2 Phase A

#### `MANUAL_JDS.md`
- **What it is:** The manual paste-in for JDs the auto-scrapers (which arrive in Session 2 Phase B+) miss. One entry per JD; the runner reads them on the next invocation.
- **How to use it:** Open the file, copy the `[TEMPLATE]` block, paste a real JD into a new entry, save. Run `python scripts/score_jobs.py`.
- **Use cases:** A LinkedIn role you saw logged-in that the public scraper can't see; a JD a recruiter sent you directly; anything you want scored ad-hoc.
- **When to edit:** Whenever you have a new JD to score. Cleared automatically after each successful run.

#### `MANUAL_JDS_PROCESSED.md` *(gitignored — local-only)*
- **What it is:** Append-only archive of every JD entry that's been scored. Auto-maintained by the runner.
- **How to use it:** Read-only. Ignore unless you want a history of what's been scored.
- **Why gitignored:** Pushing this to a public/portfolio repo would expose which JDs (potentially including the recipient's own) you've scored. Kept local-only since the scoring trace + digest in `_local/` already cover everything you need day-to-day.
- **When to edit:** Don't.

#### `requirements.txt`
- **What it is:** Python dependencies for the scripts (`anthropic`, `python-dotenv`, `requests`, `gspread`, `google-auth`, `apify-client`). Used by `pip install -r requirements.txt`.
- **When to edit:** Only when adding a new Python package the scripts need.

#### `.env` *(gitignored — never committed)*
- **What it is:** Local secrets file. Holds `ANTHROPIC_API_KEY` (scoring), `GOOGLE_SHEETS_KEY_PATH` + `GOOGLE_SHEET_ID` (Phase C Sheet writes), and `APIFY_API_TOKEN` (LinkedIn discovery via `linkedin_apify`). Read by `score_jobs.py` and `run_scrapers.py` via `python-dotenv`.
- **How to use it:** Edit in TextEdit (or any editor). Never paste its contents into chat or commit it.
- **When to edit:** Rotating any of the keys, or adding new secrets in future sessions.

### `docs/` folder

#### `docs/EVAL_SET.md`
- **What it is:** 9 manually-labeled gold-standard postings + their target scores + per-dimension reasoning. The test fixture for every prompt change. **JD bodies live in the companion file `docs/EVAL_SET_JDS.md`** — `EVAL_SET.md` holds only the targets and the why; the JD text is split out so it can be fed to the scorer.
- **How to use it:** Reference when validating a prompt change. Append outcome-validated examples each month.
- **Use cases:**
  - You changed the prompt → run `cat docs/EVAL_SET_JDS.md >> MANUAL_JDS.md && python scripts/score_jobs.py`, then compare against the 6 targets here. Confirm scores within ±1.
  - You applied to a role + got rejected at score 8 → consider adding it as a labeled "should have been a 5" example (add the entry here AND the JD body to `docs/EVAL_SET_JDS.md`).
- **When to edit:** Every monthly QC (1–2 new examples typically); after any prompt version bump (record actual scores)

#### `docs/EVAL_SET_JDS.md`
- **What it is:** The 9 JD bodies backing `EVAL_SET.md`'s gold-standard targets, formatted for the scorer to read. The original 6 were extracted from `Job Posting samples/JD mapping to my exp..docx` (Session 2.2.1); two new entries (Snorkel, Zillow/FUB) were added in Session 2.2.2 from JDs Ayesha supplied during a session — both US-based, both H1B-sponsor; a third (Wise Cards Pay-in Orchestration) was added in Session 3.2 (2026-05-09) after the LinkedIn discovery channel surfaced it in its first firing and a recruiter callback validated it. JDs are committed so calibration doesn't break when original postings come down off live ATS boards.
- **How to use it:** When re-running the eval set for prompt validation or monthly QC: `cat docs/EVAL_SET_JDS.md >> MANUAL_JDS.md && python scripts/score_jobs.py`. Cost: ~$1.08 per full eval run (9 entries × ~$0.12).
- **Use cases:**
  - Before shipping a `SCORING_PROMPT.md` version bump — re-run and confirm no role drifts > 1 point
  - First-of-month QC ritual — eval set is one of the auto-runs
  - After-action: you applied to a role at score 8 and got rejected → add as eval set entry #7 (here + in `EVAL_SET.md`)
- **When to edit:** Whenever you add a new gold-set entry; never edit existing JD bodies (they're frozen snapshots — changing the body would invalidate the historical target).

#### `docs/PHASE_C_SETUP.md` *(Phase C — one-time setup walkthrough)*
- **What it is:** Step-by-step guide (~10–15 min total) for wiring up the Google Sheet that stores every scored role + outcomes. Walks through Cloud Console project + Sheets API enablement + service account creation + JSON key download + Sheet creation + sharing the Sheet with the service account + `.env` updates + connection verification. Plain-English explanations of *what* each step does and *why*. Includes a Troubleshooting section mapping the four common errors to the step that fixes them, and Security notes for key rotation if a key ever leaks.
- **How to use it:** Open it once when first setting up Phase C. After that, only reach for it again if you need to rotate the service-account key, point at a different Sheet, or re-do setup on a new machine.
- **Use cases:**
  - First-time Phase C setup
  - Service-account key rotation (delete + recreate via the same flow)
  - Onboarding the project to a new machine
- **When to edit:** When the Phase C setup process changes (new env var, new permission scope, different auth approach).

#### `docs/CALIBRATION_DEEP_DIVE.md`
- **What it is:** The 6-phase, 60–90 min playbook for fixing inverted calibration. Only opened when QC fires the 🚨 alert.
- **How to use it:** Run with Claude Code in a dedicated session. Don't shortcut phases.
- **Use cases:**
  - Monthly QC reports inverted bands (e.g., 7–8 conversion > 9–10 conversion)
  - You suspect rubric drift but the symptoms aren't yet inverted — can run preemptively
- **When to edit:** Rare. If a phase consistently doesn't surface useful info, refine it.

#### `docs/qc-reports/`
- **What it is:** Folder containing one auto-generated markdown report per month: `2026-05.md`, `2026-06.md`, etc. Plus `TEMPLATE.md` (the master template the workflow populates).
- **How to use it:** Open the latest report at monthly QC. Browse historicals via `git log docs/qc-reports/`.
- **Use cases:**
  - Monthly review (open `YYYY-MM.md`)
  - "How has my matcher performed over 6 months?" → browse multiple reports
  - "When did I last tune the prompt and why?" → cross-reference with `SCORING_PROMPT.md` Iteration log
- **When to edit:** Each month — fill in the action items + outcome-review sections of the latest report

### Existing folders (your assets, not generated by the agent)

#### `Ayesha Resume/`
- **What it is:** Two base resumes that anchor the agent + a growing repository of past tweaked variants + per-application cover letters. The folder has three distinct roles depending on which agent step is running.
  - **Top level** *(committed to GitHub)* — used by both **scoring** (Step 1) and **asset matching** (Step 2):
    - `Ayesha Base Platform PM.docx` — Platform-PM-optimized base
    - `Ayesha Ghoshal_Resume_2026.pdf` — Generic 1-page PM base
  - **`Resume to use repository/` subfolder** *(gitignored — local-only)* — used **only** by asset matching (Step 2), **NOT** by scoring. Houses real tweaked resumes Ayesha has used for past applications, so the asset matcher has more candidate starting points than just the two bases. Local Claude sessions can still read these files for resume/cover-letter work. **Why gitignored:** these tailored resumes name competitors and prior application targets — not safe to surface in a public/portfolio repo.
  - **`Cover Letters/` subfolder** *(gitignored — local-only)* — per-application cover letters paired with the tweaked resumes above. Not read by the agent itself; exists as a local archive for Ayesha to reuse phrasing, openings, and gap-disclosure framings across similar future applications. **Why gitignored:** same reasoning as the resume repository — tailored content names companies, roles, and contains role-specific framing not safe to push to a portfolio repo.
- **How to use it:** Drop new tweaked variants in `Resume to use repository/` and the matching cover letter in `Cover Letters/` after each real application. Only update the top-level bases when your headline positioning changes.
- **Use cases:**
  - Headline positioning changed → replace the relevant top-level base file
  - You used a tweaked resume + cover letter for a real application → save the final versions in `Resume to use repository/` and `Cover Letters/` respectively, with matching filenames so the pair is easy to find later
  - Brand-new domain you want a permanent base for → add as a third top-level file *and* update `PROJECT_BRIEF.md` § Resume selection guidance to add routing rules
- **When to edit:** Whenever your resumes or cover letters change. The two subfolders grow over time; the top level stays stable.

#### `Job Posting samples/`
- **What it is:** Reference materials. Contains the 6 sample JDs that seeded `EVAL_SET.md` and the original Platform PM Role Analyzer prompt that became `SCORING_PROMPT.md`.
- **How to use it:** Read-only reference. The agent doesn't read these directly.
- **Use cases:**
  - You want the original verbose Analyzer prompt (longer than `SCORING_PROMPT.md`'s adapted version) → read here
  - You want the original sample JDs in their full form → here
- **When to edit:** Don't, generally. These are historical seed material.

#### `Product Experinces/`
- **What it is:** Source-of-truth artifacts for your three flagship projects (PRDs, reference guides, metrics docs).
- **How to use it:** Read-only when verifying a metric or claim. **Never let Claude invent numbers — always verify against these files.**
- **Use cases:**
  - You wrote a bullet claiming "$9.6M impact" — verify the exact figure against `WFM_Supplier_Onboarding_Convergence_Reference_Guide.md.pdf`
  - You want to recall the original PRD for Mexico Tax Recon → `FinAuto/`
- **When to edit:** Only if you're updating a project's metrics or adding a new flagship project

#### `London Headhunters/` *(out of scope for this agent)*
- **What it is:** A parallel **semi-manual workflow** for direct outreach to London headhunters / VC talent partners. **Not part of the job-scraping agent.** Lives next to the project for convenience only.
- **How to use it:** Treat as out of scope for any agent code or scraper logic. The folder is gitignored — it does not push to the GitHub repo. It has its own strategy doc + CRM and is driven manually (or by user-level hooks), independent of the scraper pipeline.
- **Use cases:** Manual outreach sessions only. Session 2 (and future) agent code should never read or write to this folder.
- **When to edit:** Independent of this project — don't touch from inside agent workflows.

### Memory (managed automatically — you don't edit)

#### `~/.claude/projects/.../memory/`
- **What it is:** Cross-session memory Claude maintains automatically. Stores user profile, tech-comfort level, visa constraints, project decisions, file references.
- **How to use it:** You don't touch this. Claude updates it during conversations.
- **Use cases:**
  - You want to know what Claude "remembers" about you → ask Claude: "What memories do you have about me?"
  - You want Claude to forget something → tell Claude explicitly: "Forget X" — it'll remove the relevant memory
- **When to edit:** Only by asking Claude in conversation; don't edit files directly

---

## 🧭 Section 3 — When to consult this TOC

**Open this file when:**

1. **You can't remember where something lives.** ("Wait, did I put hard filters in their own file or in the prompt?") → Section 1.
2. **You're doing a workflow for the first time.** ("It's my first monthly QC — what do I open first?") → Section 1, monthly row.
3. **You're starting a fresh Claude Code session and want it to be useful immediately.** Tell Claude: *"Read TABLE_OF_CONTENTS.md and CLAUDE.md, then ask me what I want to do today."* → orients it without you having to re-explain everything.
4. **You're considering a new file or folder.** Check if there's already a place for what you want to track. If yes, edit that. If no, add the new file *and* a TOC entry.
5. **Something feels redundant.** ("Wait, are HARD_FILTERS.md and SCORING_PROMPT.md doing the same thing?") → Section 2 disambiguates.
6. **You're explaining the project to someone else.** Send them README + this file. They'll be 80% oriented.

**Don't open this file for:**

- Routine actions you do every week (digest review, marking outcomes) — those become muscle memory.
- Day-of-the-month QC ritual — go straight to `QC_PROCESS.md`.
- The actual content of a file — open the file directly.

---

## 🛠️ Maintaining this TOC

This file works only if it's kept current. Convention:

- **When you add a new file/folder** → add a row in Section 1 (if there's a trigger workflow) and a sub-section in Section 2.
- **When you delete a file** → remove all its rows + sub-section.
- **When a workflow changes** → update Section 1.
- **At every monthly QC** → glance at Section 1 and check if any row is stale.

If Claude adds a new file in this project without also updating this TOC, that's a bug in Claude's behavior — flag it and update `CLAUDE.md` to require TOC updates.
