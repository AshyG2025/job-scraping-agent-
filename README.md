# Job Scraping Agent

A scheduled agent that scours job boards and company career pages for **Senior / Principal Platform PM roles** that match my experience, scores them against my resume, and emails me a ranked digest 2–3x/week.

This is a personal project for **Ayesha Ghoshal** — currently Sr. PM-Tech (L6) at Amazon, looking for the next Platform PM role in Seattle / SF Bay / London.

---

## Why this is interesting from a platform-PM lens

Most "AI side projects" are demos. This one is structured the way a platform PM would build an internal AI tool — with the boring scaffolding that actually decides whether an LLM-powered system holds up in production:

- **Eval-driven from day 1.** Every prompt change is validated against a labeled gold set (`docs/EVAL_SET.md`) before it ships; targets are anchored to my own outcomes, not vibes.
- **Calibration as a first-class concern.** The monthly QC ritual (`QC_PROCESS.md`) builds a calibration table by score band; an inverted-calibration deep-dive playbook (`docs/CALIBRATION_DEEP_DIVE.md`) fires when the rubric breaks rather than letting drift accumulate.
- **Cost discipline at the boundary.** Pre-LLM hard filters (`HARD_FILTERS.md`) drop obvious no-go roles before they reach the paid scoring step; the system prompt is cached (~19.5K tokens) so per-call cost stays under $0.15 with high-effort thinking on Opus 4.7.
- **Observability for non-deterministic systems.** Every scored role emits a verbose `reasoning_trace` plus a `verify_flags` field for self-flagged uncertainty. That field caught a parser bug in v1 of the runner before any digest shipped — a working example of why audit trails are not optional for LLM pipelines.
- **Versioned prompts + schema'd outputs.** `prompt_version` is frozen at scoring time so historical scores stay interpretable; the JSON output schema is the contract every downstream step depends on.
- **Outcome-tied feedback loop.** Application outcomes (response / phone screen / interview / offer) flow back into the calibration table, so the rubric tunes against ground truth instead of intuition (`APPLICATION_LOG.md`).

The "personal job search" framing is the demo — the interesting part is the platform-PM design choices behind it.

---

## How it works (the pipeline)

```
                            ┌──────────────────────────┐
                            │   Schedule trigger       │
                            │   Tue + Thu (+ optional  │
                            │   Sat) at 7am PT         │
                            │   via GitHub Actions     │
                            └────────────┬─────────────┘
                                         ▼
   ┌─────────────────────┐    ┌─────────────────────────┐
   │  TARGETED scrapers  │    │  DISCOVERY scrapers     │
   │  ~50–70 named       │    │  LinkedIn + TrueUp +    │
   │  company career     │    │  YC Work at a Startup + │
   │  pages              │    │  VC portfolio boards    │
   │  (custom code)      │    │  (Apify + custom)       │
   └──────────┬──────────┘    └──────────┬──────────────┘
              │                          │
              └──────────────┬───────────┘
                             ▼
              ┌─────────────────────────────┐
              │   Hard filters              │
              │   (HARD_FILTERS.md)         │
              │   • IC roles only           │
              │   • Geo allowlist           │
              │   • H1B check (US)          │
              │   • Posting freshness       │
              │   • Dedup                   │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │   LLM scoring               │
              │   (SCORING_PROMPT.md)       │
              │   • Match score (1–10)      │
              │   • Reason                  │
              │   • Recommended resume      │
              │   • H1B verification flag   │
              │   Powered by Claude API     │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │   Asset matcher             │
              │   For roles ≥ 7/10:         │
              │   • Pick best base resume   │
              │   • Suggest bullet tweaks   │
              │   • Suggest cover letter    │
              │     angle                   │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │   Delivery                  │
              │   • Email digest (Resend)   │
              │   • Google Sheet log        │
              │   • [Future] Notion DB      │
              └─────────────────────────────┘
```

---

## Project files (what each one does)

| File | What it controls | Edit when... |
|---|---|---|
| `PROJECT_BRIEF_PUBLIC.md` | Ideal-role definition framework — the matcher's anchor *(named-company targets, comp expectations, and file-pathed resume routing live in the local-only working copy `PROJECT_BRIEF.md`)* | I want to change what counts as a "good fit" |
| `COMPANY_LIST_PUBLIC.md` | Tier framework + discovery sources *(named per-tier list and Referral Network live in the local-only working copy `COMPANY_LIST.md`)* | I learn about a new company / want to add or remove one |
| `HARD_FILTERS.md` | Pre-LLM rules (titles, geo, H1B, freshness) | I want to tighten or loosen filtering |
| `SCORING_PROMPT.md` | The Claude prompt that scores each role | I want to change scoring criteria or output format |
| `docs/EVAL_SET.md` | Labeled sample postings for testing the prompt | A scored role disagrees with my judgment — add it here as a labeled example |
| `QC_PROCESS.md` | Monthly QC ritual — what auto-runs on the 1st, what I do for ~15 min | I want to change cadence or QC criteria |
| `APPLICATION_LOG.md` | Outcome tracking schema + calibration feedback loop | I want to change what outcome data is captured |
| `docs/qc-reports/` | Auto-generated monthly QC reports — historical record of matcher health | (Don't delete) |
| `docs/CALIBRATION_DEEP_DIVE.md` | The 6-phase playbook for fixing inverted calibration | Calibration is severely broken (run only when QC flags 🚨) |
| `Ayesha Resume/` | The two base resumes the asset matcher picks from | I update my resume |
| `Job Posting samples/` | Reference: original analyzer prompt + sample JDs | (Read-only reference) |

**Anything I edit in any of the `.md` files takes effect on the next run** — no code change needed for content updates.

---

## How to use the output

Every Tuesday / Thursday morning I'll get an email digest like:

```
SUBJECT: 7 new Platform PM roles for you (3 strong, 2 moderate, 2 stretch)

═══════════════════════════════════════════════════════
🟢 STRONG MATCHES (≥ 8/10)
═══════════════════════════════════════════════════════

1. Wise — Senior Product Manager, Treasury Ledger Platform — London
   Score: 9/10  •  Verdict: prioritize  •  H1B: N/A (London)

   Reasoning:
     Domain (9):       FinTech ledger / data-integrity platform — direct match to Mexico Tax Recon work.
     Skills (9):       JD asks for technical IC + system-level thinking + roadmap from chaos. All directly evidenced.
     Level (8):        "Multiple years" reads as Senior–Staff IC — at-bar.
     Team needs (9):   "Completeness, accuracy, controls" mandate is exactly Mexico Tax Recon's problem.

   Resume: Start from Ayesha Base Platform PM.docx
   Suggested tweaks: (2) Reframe Mexico project as "Multi-System Data Integration Platform"...
   Cover-letter angle: Bridge "treasury ledger and tax reconciliation share the same hard problem..."

   [Apply on Wise career page →]
   [📋 Show full QC reasoning trace →]    ← deep dive available for top score / borderline / 10% sample

...
```

**Reasoning is always visible** — you'll see the per-dimension scores + a 1-line reason for every role, so QC takes seconds.

**Deep reasoning trace (QC mode)** fires for: the top-scoring role of each run, any role on the asset-match boundary (scores 6/7/8), and a random 10% sample. This is your audit trail — read these to spot where the matcher's judgment diverges from yours, then tune `SCORING_PROMPT.md`.

The Google Sheet keeps a running log of every role ever surfaced (so I don't see the same role twice) **plus the full reasoning trace and any QC deep dives** as columns you can review later.

---

## How to update the agent's behavior

| I want to... | Edit this file |
|---|---|
| ...stop matching to a company | Move it to `Skip` in `COMPANY_LIST.md` |
| ...add a company I just heard about | Add a bullet under the right tier in `COMPANY_LIST.md` |
| ...filter out a title pattern | Add to the title DROP list in `HARD_FILTERS.md` |
| ...broaden / narrow the geo | Edit the geo allowlist in `HARD_FILTERS.md` |
| ...change what scoring weighs | Edit `SCORING_PROMPT.md` |
| ...change my resume | Update files in `Ayesha Resume/` and re-state which leads what in `PROJECT_BRIEF.md` |
| ...change cron schedule | Edit the `cron:` line in `.github/workflows/scrape.yml`; use https://crontab.guru/ to translate. Remember: GitHub Actions cron is UTC. |
| ...disable the cron temporarily | Comment out the `cron:` line in `.github/workflows/scrape.yml`, commit, push. The manual trigger (Actions tab → Run workflow) still works. |

---

## Tech stack (for reference)

- **Code:** Python (written by Claude Code; I review, not author)
- **Scheduling:** GitHub Actions (free)
- **LinkedIn / Indeed scraping:** Apify (~$30–49/mo)
- **Career-page scrapers:** Custom Python per company
- **Brain:** Claude API
- **Storage:** Google Sheets
- **Email:** Resend (free tier)
- **Repo:** GitHub (private)

---

## QC and tuning over time

The matcher will drift — Claude API gets updated, you'll edit the brief, real-world job postings shift in shape. To catch this early:

- **Per-role QC** — every role's `reasoning_trace` is shown in the digest, so you can sanity-check at a glance (~5 sec per role)
- **Sampled deep dives** — for the top score of each run, borderline-asset-match roles, and a 10% random sample, the matcher emits a 7-step audit trail so you can see *how* it reasoned (not just what it concluded)
- **Monthly QC ritual** — on the 1st of every month at 9am Seattle, an automated workflow re-runs the eval set, aggregates production stats *and application outcomes*, and emails you a pre-populated report at `docs/qc-reports/YYYY-MM.md`. You spend ~15 min reviewing + filling action items. See `QC_PROCESS.md` for the full ritual.
- **Outcome-based calibration loop** — applications get tracked through the funnel (no response / recruiter / interview / offer) in the Google Sheet. The monthly QC builds a calibration table by score band and surfaces score-vs-outcome conflicts as eval-set candidates. See `APPLICATION_LOG.md`.
- **Inverted-calibration deep dive** — if the calibration table ever shows lower bands converting *higher* than higher bands (rubric is fundamentally broken), the QC report flips to 🚨 mode and links to `docs/CALIBRATION_DEEP_DIVE.md` — a structured 60–90 min playbook to run with Claude Code to find the root cause and ship a tested fix.

## Status

🟢 **Spec layer complete** (Sessions 1 + 1.5–1.7) — all spec docs shipped: `PROJECT_BRIEF`, `COMPANY_LIST`, `HARD_FILTERS`, `SCORING_PROMPT`, `APPLICATION_LOG`, `QC_PROCESS`, `docs/EVAL_SET`, `docs/EVAL_SET_JDS`, `docs/CALIBRATION_DEEP_DIVE`, `docs/qc-reports/TEMPLATE`, plus `TABLE_OF_CONTENTS` and `QUICK_COMMANDS`.

🟢 **Phase A — scoring runner shipped** (Session 2.0, commit `2987855`) — `scripts/score_jobs.py` reads JDs from `MANUAL_JDS.md`, scores each via the Claude API (Opus 4.7, prompt caching on the 3-file system context), and writes a digest to `_local/digest.md` plus structured results to `_local/scored_results.json`. Validated end-to-end on real postings; eval-set anchors hold within ±1 of target. The verbose `verify_flags` field caught a v1 parser bug before any digest landed.

🟢 **Phase B — career-page scrapers (mostly shipped)** (Sessions 2.1–2.1.4) — `scripts/run_scrapers.py` orchestrator + per-ATS modules under `scripts/scrapers/` (`greenhouse`, `smartrecruiters`, `workday`, `ashby`). 32 of 49 named-company targets covered (~65%). Remaining 17 are intentionally deferred: ~12 are routed to the discovery channel (Apify LinkedIn) rather than bespoke scrapers, since their custom in-house ATSes (or WAF-blocked portals like Coinbase + Checkout.com + American Express) aren't worth a per-co module; the rest are smaller modules pending (Lever, Workable, PhenomPeople). Coverage strategy is **partial-by-design** — named scrapers handle high-confidence targets, discovery handles the tail.

🟢 **Phase C — Google Sheets storage shipped** (Session 3.0, commit `6f5c6c5`) — `scripts/sheets.py` appends every scored role to a Google Sheet with a locked 31-column layout, sorted newest-first by score. Two engineering choices worth surfacing as platform-PM judgment calls: **(1)** `score_at_application` and `prompt_version_at_application` use Sheet formulas that auto-copy when `applied=Yes` and **survive sort** because the Sheets API SortRange updates row references server-side — picked over Apps Script or manual copy-paste because it adds zero moving parts. **(2)** JSON + Sheet are written in parallel during a 4-week proving period before the JSON is deprecated, so existing QC / eval scripts keep working through the migration rather than getting cut over in one shot. One-time setup walkthrough in `docs/PHASE_C_SETUP.md`.

🟢 **Phase D — email digest shipped** (Session 3.5) — `scripts/send_digest.py` reads `_local/scored_results.json` (Phase A's output), filters to roles ≥6/10 (configurable via `DIGEST_SCORE_THRESHOLD`), and sends a plain-text email via Resend's REST API with two sections (Strong ≥8, Moderate 6–7). Each role shows score / verdict / per-dim breakdown / 1-line reason / H1B note / apply URL; top of email links to the Google Sheet. Diagnostic at `scripts/check_resend.py`; setup walkthrough in `docs/PHASE_D_SETUP.md` (~5 min, 4 steps). Asset-match snippets intentionally deferred to V2 Resume Agent. Standalone script (not auto-fired from `score_jobs.py`) so it can be re-sent without re-scoring.

🟢 **Phase E — GitHub Actions cron shipped** (Session 3.6) — `.github/workflows/scrape.yml` runs the full pipeline (`run_scrapers.py && score_jobs.py && send_digest.py`) on cron `0 17 * * 2,4` (9am PT Tue + Thu year-round; drifts to 10am during PDT). Also exposes a manual `workflow_dispatch:` trigger via the Actions tab for ad-hoc runs. State persistence via `actions/cache@v4` for `_local/scraped_seen.json` (Phase B dedup) + `_local/last_sent_digest.json` (Phase D re-send guard) — without it, every Tuesday's run would re-surface roles surfaced last Thursday. `concurrency:` block prevents overlap so concurrent runs don't race on the shared Sheet. Failures email the repo owner via GitHub's default. Per-run output (digest.md + scored_results.json) uploaded as a 14-day artifact for post-mortem. Setup walkthrough at `docs/PHASE_E_SETUP.md` (~10 min: 7 GitHub secrets via web UI + a manual trigger to verify). Cost: $0 added (GitHub Actions free tier covers ~120 min/mo we'll use, well under 2K cap).

🔵 **V2 (after V1 phases close)** — outcome-driven few-shot examples in `SCORING_PROMPT.md` once 50+ application outcomes have accumulated; a dedicated **Resume & Cover Letter Expert Agent** (ATS-focused, authenticity-bounded, intentional-tweaks framing) that replaces the current bullet-tweak suggestions with a properly drafted tailored resume + cover letter; LinkedIn parsing for hiring managers / recruiters of prioritized roles; Notion as primary view.
