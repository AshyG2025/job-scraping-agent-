# Job Scraping Agent

A scheduled agent that scours job boards and company career pages for **Senior / Principal Platform PM roles** that match my experience, scores them against my resume, and emails me a ranked digest 2–3x/week.

This is a personal project for **Ayesha Ghoshal** — currently Sr. PM-Tech (L6) at Amazon, looking for the next Platform PM role in Seattle / SF Bay / London.

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
| `PROJECT_BRIEF.md` | Ideal-role definition; the matcher's anchor | I want to change what counts as a "good fit" |
| `COMPANY_LIST.md` | Tier 1/2/3 named companies + discovery sources | I learn about a new company / want to add or remove one |
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
| ...change cadence / digest delivery | Edit `.github/workflows/scrape.yml` (the GitHub Actions schedule) |

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

🟢 **Session 1 + 1.5 complete** — all spec docs shipped (`PROJECT_BRIEF`, `COMPANY_LIST`, `HARD_FILTERS`, `SCORING_PROMPT`, `APPLICATION_LOG`, `QC_PROCESS`, `docs/EVAL_SET`, `docs/CALIBRATION_DEEP_DIVE`, `docs/qc-reports/TEMPLATE`), plus `TABLE_OF_CONTENTS` and `QUICK_COMMANDS`
🟢 **GitHub repo live** — private, at `github.com/AshyG2025/job-scraping-agent-` (initial push 2026-04-27)
🔴 **Session 2 (code) not started** — scrapers, scoring runner, asset matcher, digest emailer, Google Sheets writer, and monthly QC workflow still to build
