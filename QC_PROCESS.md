# Monthly QC Process

> **Why this exists:** Job-matching prompts drift. Three sources of drift:
> 1. **Claude API model updates** — same prompt, different scores when Anthropic ships a new model
> 2. **Edits to `PROJECT_BRIEF.md` / `COMPANY_LIST.md` / `SCORING_PROMPT.md`** that you didn't re-test
> 3. **Real-world distribution shift** — companies post different kinds of roles in March vs. October; the matcher might silently mis-handle a new pattern
>
> Without periodic QC, drift compounds and you lose trust in the digest. This file describes the monthly ritual that catches drift early.
>
> **Cadence:** Auto-fires on the **1st of every month at 9am Seattle time** via GitHub Actions.
>
> **Time commitment:** ~15–20 minutes of your time. Most of the work is auto-done.

---

## What auto-happens on the 1st

A scheduled GitHub Actions workflow does the following, with no human input:

1. **Re-runs the eval set** — feeds all 6 postings in `docs/EVAL_SET.md` through the *current* `SCORING_PROMPT.md` using the *current* Claude API model. Scores are recorded.
2. **Compares to targets** — checks each eval-set score against the target listed in `EVAL_SET.md`. Any drift ≥ 2 points = ⚠️ alert; ≥ 3 points = 🚨 critical.
3. **Compares to last month** — diffs this month's eval-set re-run vs. last month's, so you can see month-over-month movement.
4. **Aggregates production stats from the past month:**
   - Total roles scraped, total roles scored (after hard filters)
   - Score distribution (how many 9–10s, 7–8s, 5–6s, 3–4s, 1–2s)
   - Verdict breakdown (prioritize / apply / consider / weak / skip counts)
   - Discovery vs. targeted source split
   - Top 10 highest-scored roles of the month
   - Companies surfaced via discovery mode that scored ≥ 7 (candidates to promote to Tier 1)
   - Roles flagged with `verify_flags` (uncertainty markers from the model)
5. **Picks 10 random scored postings** from the month for human review.
6. **Generates `docs/qc-reports/YYYY-MM.md`** by populating `docs/qc-reports/TEMPLATE.md` with all the above data.
7. **Emails you** with the report attached and a subject like *"📋 Monthly QC ready — May 2026 (1 ⚠️ drift alert)"*.

---

## What you do in your 15–20 minutes

When the report email arrives:

### 1. Open `docs/qc-reports/YYYY-MM.md` in your editor
This is the auto-generated report. Edit it directly — git history becomes your QC log.

### 2. Eval-set drift check (~3 min)
Look at the eval-set comparison table. Any row with ⚠️ or 🚨?
- If **no drift** → tick the box, move on.
- If **drift on 1 row** → read the model's `reasoning_trace` for that role. Did the model's reasoning change? Did `PROJECT_BRIEF.md` or `COMPANY_LIST.md` change recently? Note the cause in the report.
- If **drift on 2+ rows** → likely a Claude model update or a prompt edit you didn't realize broke things. Action: revert the prompt change, or update `EVAL_SET.md` targets if you genuinely think the new scores are correct.

### 3. Random sample review (~10 min)
The report includes 10 random scored postings from the month, each with the role title, score, and `reasoning_trace`. For each, mark one of:
- ✅ **Agree** — score is right
- ⚠️ **Off by 1** — minor disagreement, fine
- 🔴 **Off by 2+** — substantive disagreement, note why

If 7+ of the 10 are ✅ → matcher is healthy.
If 3+ are 🔴 → systematic issue; investigate the `reasoning_trace` for patterns and tune the relevant doc.

### 4. Discovery promotions (~2 min)
The report lists any company surfaced via discovery mode that scored ≥ 7 this month. For each:
- Promote to Tier 1 / Tier 2 in `COMPANY_LIST.md` (one-line edit)
- Or leave as-is if it's a one-off

**Plus a 30-sec scraper-volume sanity check:** glance at `_local/scraped_seen.json` and count entries added this month per configured company. Roughly 2–8 fresh roles per Tier-1 company per month is normal; 0 entries from a configured company over 4+ weeks signals a broken scraper (ATS changed, title regex no longer matches, etc.). If something's off, scan recent `run_scrapers.py` output for failure messages and check the relevant per-ATS module.

### 5. Application outcomes review (~5 min) — the calibration loop

The QC report includes **calibration data from real applications** (see `APPLICATION_LOG.md`). This is the strongest tuning signal you have.

a. **Update outcome columns** in the Google Sheet for any applications whose status changed since last QC (recruiter responded, interview happened, rejected, etc.). 2–3 min.

b. **Read the calibration table** — what % of each score band converted to recruiter response / interview / offer? Healthy = higher score bands have higher conversion. If 7–8s are converting better than 9–10s, the rubric is broken.

c. **Review the score-vs-outcome conflicts list** — roles where outcome strongly contradicted score (8 → instant reject, or 5 → interview offer). For each:
   - Fill in `score_in_hindsight` (what would you score it now?)
   - Mark `add_to_eval_set` Yes/No — promote to gold standard if the outcome is decisive
   
   *This is the highest-value tuning move you can make. Adding 1–2 outcome-validated examples per month grows your eval set from 6 synthetic to 50+ real-world over 6 months.*

d. **Read the response-vs-rejection cohort lists** — top 5 recent recruiter responses + top 5 recent rejections side-by-side. What do the responders have in common that the rejected ones don't? Often a pattern the rubric doesn't yet weight (e.g., "all responders were post-Series-D" or "all rejections required >10 yrs").

### 6. Action items (~3 min)
At the bottom of the report, write any actions for the next month based on what you saw in steps 2–5. Examples:
- "Tighten domain definition — model is treating data platforms as too-strong-a-match"
- "Add 3 outcome-validated postings to EVAL_SET — see Conflicts list"
- "Bump SCORING_PROMPT to v1.2 — reduce skills weight to 0.25, increase team_needs to 0.25"
- "Add hard filter for 10+ years required — pattern in rejections this month"

### 7. Commit the filled report
```
git add docs/qc-reports/2026-05.md
git commit -m "QC: May 2026 — 1 drift alert resolved, 2 companies promoted, 3 outcome-validated examples added to EVAL_SET"
git push
```
The report is now your historical record. Six months from now you can `git log docs/qc-reports/` to see your tuning history.

---

## When QC alerts go off mid-month (not just on the 1st)

The matcher emits **inline alerts** during normal runs if certain conditions hit, so you don't always have to wait for the 1st:

| Trigger | Alert |
|---|---|
| Eval-set drift ≥ 3 points on any role | 🚨 Email immediately, run halts |
| > 50% of a run's roles scored 1–2 (skip) | ⚠️ Probable filter or scoring bug — email warning |
| > 30% of a run's roles have non-empty `verify_flags` | ⚠️ Model uncertainty unusually high — investigate |
| New company surfaces with score ≥ 9 from discovery mode | 📌 Email highlight (not an error — just don't miss it) |

---

## 🚨 When calibration inverts: deep-dive ritual

If the monthly QC's calibration table shows **inverted bands** (a lower score band converting at a higher rate than a higher one — e.g., 7–8s getting more recruiter responses than 9–10s), tuning a weight by 0.05 won't fix it. The rubric itself is mis-modeling reality.

**This is rare, but high-stakes when it happens.** The deep-dive ritual is in `docs/CALIBRATION_DEEP_DIVE.md` — a structured 6-phase, 60–90 min playbook you run *with Claude Code in a dedicated session* to:

1. **Reconstruct the inversion** — pull the actual roles in each band and their reasoning traces
2. **Locate the mis-scoring dimension** — which of {domain, skills, level, team_needs} is over-rating?
3. **Diagnose the root cause** — definition issue? brief over-claim? hard filter gap?
4. **Propose specific testable fixes** — concrete edits with predicted impact, not vague "tighten the rubric"
5. **Test before commit** — re-run eval set + past-month conflict cohort
6. **Commit + log** — bump prompt version, write the iteration-log entry, commit with full diagnostic trail

The QC report's email subject changes to *"🚨 Inverted calibration — deep dive required"* when this fires, and the report links directly to the playbook. Don't ship a fix without going through all 6 phases — rubric drift is hard to undo once shipped.

---

## How to skip a month without breaking things

If you're traveling or busy, just don't fill in the report. The automation still runs and generates the next month's report. The only thing you lose is the historical record of *that month's* judgment — not a big deal.

If you skip 2+ months in a row, the next report's email subject will say *"📋 Monthly QC ready — Aug 2026 (3 months since last review)"* — gentle pressure to catch up.

---

## Bootstrapping (before the GitHub Actions cron is wired up)

Until Session 2 ships the workflow code, you can do this **manually once a month**:

1. Open `docs/EVAL_SET.md` and copy each posting's JD body
2. For each, run it through the Claude API with `SCORING_PROMPT.md` (or paste into Claude Code: *"Score this posting against my scoring prompt"*)
3. Compare the 6 scores to the targets in `EVAL_SET.md`
4. Copy `docs/qc-reports/TEMPLATE.md` to `docs/qc-reports/2026-05.md` and fill in by hand

Slower (~30 min instead of 15) but works. The point is to build the habit before the automation lands.
