# Application Outcomes — Feedback Loop

> **Why this exists:** A score of 8/10 only means something if 8s actually convert to recruiter calls and interviews. Without outcome data, the scoring rubric is just a guess. With it, you have a calibration signal that exposes when the matcher is over- or under-rating roles, and what patterns lead to real conversion.
>
> **Where outcomes are tracked:** In the **Google Sheet** that logs every scraped role (the same one used as daily digest UI). This file describes the schema + how to use it; the sheet is the source of truth.
>
> **How outcomes feed back into the system:** During the monthly QC ritual (`QC_PROCESS.md`) — outcomes get aggregated into a calibration table, surfacing drift candidates and eval-set additions. Outcomes do NOT auto-feed into the scoring prompt in V1 (sample size too small + risk of overfitting to noise). After ~6 months of data, we can revisit using them as few-shot examples in `SCORING_PROMPT.md`.

---

## Outcome columns in the Google Sheet

Every row (one row per scored role) gets these additional columns. Most are empty until you take action:

| Column | Type | Filled when |
|---|---|---|
| `applied` | Yes / No | You apply (or decide not to) |
| `applied_date` | Date | You applied |
| `score_at_application` | Number (auto-copied from `final_score`) | Auto-filled when `applied` flips to Yes — frozen so prompt edits don't retroactively change it |
| `prompt_version_at_application` | Text (auto-copied) | Auto-filled — so we know which prompt produced this score |
| `outcome_status` | Enum (see below) | Updated as the application progresses |
| `outcome_date` | Date | Updated whenever `outcome_status` changes |
| `outcome_notes` | Free text | Optional — context on why the outcome happened |
| `score_in_hindsight` | Number (1–10) | Filled at monthly QC — what would you score this role *now*, knowing the outcome? |
| `add_to_eval_set` | Yes / No | Filled at monthly QC — should this become a permanent gold-standard example? |

### `outcome_status` enum values

| Value | Meaning |
|---|---|
| `not_applied` | You decided not to apply (default for everything you skip) |
| `applied_no_response` | Applied; no recruiter response within 14 days |
| `applied_rejected` | Applied; auto-rejected within 14 days |
| `recruiter_response` | Recruiter or hiring manager reached out |
| `phone_screen` | Phone screen scheduled / completed |
| `interview_round` | Made it past phone screen to formal interview rounds |
| `onsite` | Onsite (virtual or in-person) |
| `offer` | Got an offer |
| `accepted` | Accepted an offer (terminal) |
| `withdrew` | Withdrew yourself before outcome |
| `open` | Still in flight, no terminal status yet |

Higher in the funnel = stronger positive signal. Lower = stronger negative signal.

---

## Why "freeze" the score and prompt version at application time?

If you update `SCORING_PROMPT.md` after applying, the original score the model gave you is what mattered for that decision. The frozen `score_at_application` lets the monthly QC honestly say:
> *"Of roles scored 7–8 by prompt v1.0, 30% got recruiter responses. After v1.2 (which tightened skills weighting), of roles scored 7–8 by v1.2, 45% got recruiter responses."*

Without freezing, you'd retroactively rescore everything every time you tuned the prompt, and you'd lose the signal of whether the tuning helped.

---

## What "calibration" looks like in the monthly QC report

Every month, the QC report includes a calibration table aggregated from outcomes:

| Score band | # applied | Recruiter response rate | Interview rate | Offer rate |
|---|---|---|---|---|
| 9–10 (`prioritize`) | {n} | {%} | {%} | {%} |
| 7–8 (`apply`) | {n} | {%} | {%} | {%} |
| 5–6 (`consider`) | {n} | {%} | {%} | {%} |

**Healthy calibration:** Higher score bands have higher conversion rates at every funnel step. If 7–8s convert better than 9–10s, the rubric is broken — investigate.

**Sample size warning:** With < 10 applications in a band, the percentages are too noisy to act on. The report flags this so you don't over-tune on small samples.

---

## How outcomes drive prompt tuning (the feedback loop)

The monthly QC report surfaces three kinds of outcome-driven signals:

### Signal 1 — Score-vs-outcome conflicts (eval set candidates)

Roles where the outcome strongly contradicts the score:
- Scored 7+ → instant rejection or no response
- Scored ≤ 5 → recruiter outreach + interview

For each, the QC report asks: *"What's `score_in_hindsight`? Should this go in `EVAL_SET.md` as a permanent example?"*

Adding 1–2 real-world-validated examples per month grows the eval set from 6 synthetic gold-standards to 50+ outcome-validated examples in 6 months. **This is the single highest-value tuning move.**

### Signal 2 — Band-level calibration drift

If conversion rates by band shift over time (e.g., 7–8 conversion drops from 30% → 10% over 3 months), it's evidence of:
- Real-world distribution shift (companies posting different roles)
- Prompt drift (model rating things higher / lower than before)
- Your taste shifting (you're applying to roles you'd reject now)

The QC report shows the trend; you decide which is the cause.

### Signal 3 — Pattern recognition from outcome cohorts

In the QC report, the auto-generation pulls out the 5 most-recent recruiter-responded roles and the 5 most-recent rejections. Read both lists side-by-side. What do the responders have in common that the rejected ones don't? Often it's something the rubric doesn't currently weight — e.g., "all the responders were post-Series-D growth-stage" or "all the rejections required >10 years."

When you spot a pattern, update either:
- `PROJECT_BRIEF.md` (refine what counts as a good fit)
- `SCORING_PROMPT.md` (refine how dimensions are weighted or defined)
- `HARD_FILTERS.md` (drop the pattern before it gets scored)

---

## What you do at monthly QC for outcomes (~5 min of your 15)

1. **Update outcome columns for the past month's applications** — quick fill in the Sheet (probably 2–3 min)
2. **Read the calibration table** — does it look right? Healthy?
3. **Review the conflicts list** (Signal 1) — for each, decide `score_in_hindsight` and whether to promote to eval set
4. **Read the response-vs-rejection cohort lists** (Signal 3) — note any pattern in the action items section

That's it.

---

## Bootstrapping (before the Sheet exists)

Until Session 2 wires up the Google Sheet, log applications + outcomes manually in this section as a stop-gap:

| Date applied | Company | Role | Score at apply | Prompt version | Outcome | Outcome date | Score in hindsight | Notes |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| | | | | | | | | |

Once the Sheet is live, migrate this table into it and delete this section.
