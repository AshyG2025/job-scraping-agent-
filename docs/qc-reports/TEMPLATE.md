# QC Report — {YYYY-MM}

**Run date:** {YYYY-MM-DD}
**Prompt version at time of run:** {prompt_version}
**Claude model used:** {model_id}
**Last edit to PROJECT_BRIEF.md:** {date}
**Last edit to COMPANY_LIST.md:** {date}
**Last edit to SCORING_PROMPT.md:** {date}
**Time since last QC report:** {N months}

---

## 🚦 Alert summary

- **Eval-set drift alerts:** {count of ⚠️ + 🚨}
- **Inline alerts fired this month:** {count}
- **Verdict:** {🟢 healthy / 🟡 needs tuning / 🔴 critical drift}

---

## 1. Eval-set re-run

How does the prompt score the gold standard right now?

| Posting | Target | Last month | This month | Δ vs target | Δ vs last month | Status |
|---|---|---|---|---|---|---|
| Wise Invoicing PM | 8 | {n} | {n} | {Δ} | {Δ} | {✅/⚠️/🚨} |
| Wise Treasury Ledger | 9 | {n} | {n} | {Δ} | {Δ} | {✅/⚠️/🚨} |
| Liberis Financial Systems | 8 | {n} | {n} | {Δ} | {Δ} | {✅/⚠️/🚨} |
| Ebury API Platform | 6 | {n} | {n} | {Δ} | {Δ} | {✅/⚠️/🚨} |
| Boku Growth PM | 3 | {n} | {n} | {Δ} | {Δ} | {✅/⚠️/🚨} |
| Rippling Talent Mgmt | 2 | {n} | {n} | {Δ} | {Δ} | {✅/⚠️/🚨} |

**Status legend:**
- ✅ Within ±1 of target — healthy
- ⚠️ Off by 2 — investigate
- 🚨 Off by 3+ — critical drift, halt and fix

**Your notes on any drift:**
> {fill in — what caused it? acceptable or not?}

---

## 2. Production stats — past 30 days

| Metric | This month | Last month | Δ |
|---|---|---|---|
| Roles scraped (raw) | {n} | {n} | {Δ} |
| Roles scored (after hard filters) | {n} | {n} | {Δ} |
| Filter drop rate | {%} | {%} | {Δ} |
| Avg score | {n} | {n} | {Δ} |
| Asset matcher fired (≥ 7) | {n} | {n} | {Δ} |
| Discovery-mode roles | {n} | {n} | {Δ} |
| H1B-flagged ⚠️ roles (US) | {n} | {n} | {Δ} |

### Score distribution

| Band | Count | % of total |
|---|---|---|
| 9–10 (prioritize) | {n} | {%} |
| 7–8 (apply) | {n} | {%} |
| 5–6 (consider) | {n} | {%} |
| 3–4 (weak) | {n} | {%} |
| 1–2 (skip) | {n} | {%} |

**Anything unusual?** {fill in — e.g., "spike in 5–6s suggests domain definition has loosened"}

---

## 3. Top 10 random samples for human review

For each, mark agreement: ✅ agree / ⚠️ off by 1 / 🔴 off by 2+

| # | Company / Role | Score | Verdict | Your call | Notes |
|---|---|---|---|---|---|
| 1 | {company} — {title} | {n} | {verdict} | {✅/⚠️/🔴} | {your notes} |
| 2 | {company} — {title} | {n} | {verdict} | {} | {} |
| 3 | {company} — {title} | {n} | {verdict} | {} | {} |
| 4 | {company} — {title} | {n} | {verdict} | {} | {} |
| 5 | {company} — {title} | {n} | {verdict} | {} | {} |
| 6 | {company} — {title} | {n} | {verdict} | {} | {} |
| 7 | {company} — {title} | {n} | {verdict} | {} | {} |
| 8 | {company} — {title} | {n} | {verdict} | {} | {} |
| 9 | {company} — {title} | {n} | {verdict} | {} | {} |
| 10 | {company} — {title} | {n} | {verdict} | {} | {} |

**Pattern in disagreements (if any):** {fill in}

**Health check:** {n}/10 ✅ → {🟢 healthy / 🟡 watch / 🔴 systematic issue}

---

## 4. Application outcome calibration

> Real-world outcomes from past applications, aggregated by score band. This is the strongest tuning signal you have. See `APPLICATION_LOG.md` for the schema.

### 4a. Calibration table (cumulative — all-time)

| Score band | # applied | Recruiter response | Phone screen | Interview rounds | Offer |
|---|---|---|---|---|---|
| 9–10 (`prioritize`) | {n} | {n} ({%}) | {n} ({%}) | {n} ({%}) | {n} ({%}) |
| 7–8 (`apply`) | {n} | {n} ({%}) | {n} ({%}) | {n} ({%}) | {n} ({%}) |
| 5–6 (`consider`) | {n} | {n} ({%}) | {n} ({%}) | {n} ({%}) | {n} ({%}) |
| 3–4 (`weak`) | {n} | {n} ({%}) | {n} ({%}) | {n} ({%}) | {n} ({%}) |

**Sample size warning:** Bands with < 10 applications have noisy percentages — flagged with ⚠️.

**Healthy?** Conversion rates should monotonically increase by score band. {🟢 yes / 🟡 mostly / 🔴 inverted — deep dive required}

**🚨 If 🔴 inverted:** stop here, open `docs/CALIBRATION_DEEP_DIVE.md`, and run the 6-phase deep-dive ritual with Claude Code before continuing this report. Don't tune weights or definitions ad-hoc — the playbook exists for a reason.

| Inversion type detected | Severity | Action |
|---|---|---|
| {none / adjacent-swap / multi-swap / top-collapse / funnel-inversion} | {🟢 / 🟡 / 🚨} | {none / log and watch / open CALIBRATION_DEEP_DIVE} |

### 4b. This month's applications (status updates needed)

| Date applied | Company / Role | Score | Prompt v | Current status | Status changed this month? |
|---|---|---|---|---|---|
| {date} | {company} — {title} | {n} | {v} | {status} | {Y/N} |

**Action:** Update outcome columns in the Sheet for any in-flight applications before completing the rest of this report.

### 4c. Score-vs-outcome conflicts (eval-set candidates)

Roles where outcome strongly contradicted score. For each, fill in `score_in_hindsight` and decide if it should be added to `EVAL_SET.md`.

| Company / Role | Score at apply | Outcome | Hindsight score | Add to EVAL_SET? | Why |
|---|---|---|---|---|---|
| {company} — {title} | {n} | {outcome} | {n} | {Y/N} | {reasoning} |

### 4d. Pattern-recognition cohorts

**Top 5 most recent recruiter-responses:**
1. {company} — {title} (scored {n}, applied {date})
2. ...

**Top 5 most recent rejections / no-responses:**
1. {company} — {title} (scored {n}, applied {date})
2. ...

**Patterns I notice (positive cohort):** {fill in — what do the responders share that the rejected don't?}

**Patterns I notice (negative cohort):** {fill in — what's common to rejections?}

---

## 5. Discovery-mode promotions

Companies surfaced via discovery sources (not on `COMPANY_LIST.md`) that scored ≥ 7 this month:

| Company | Highest role | Score | Source | Action |
|---|---|---|---|---|
| {company} | {title} | {n} | {LinkedIn / YC / a16z / etc.} | {promote to Tier 1 / Tier 2 / leave} |

**Edits applied to `COMPANY_LIST.md`:** {list, or "none"}

---

## 5. Roles flagged with `verify_flags` this month

The model marked these as needing human research before applying:

| Company / Role | Flag(s) | Resolution |
|---|---|---|
| {company} — {title} | {flag} | {researched and confirmed / dropped / still open} |

---

## 6. Action items for next month

> {Fill in — concrete changes you're going to make to the prompt, brief, company list, eval set, or filters before the next QC.}

- [ ] {action 1}
- [ ] {action 2}
- [ ] {action 3}

---

## 7. Carry-forward from previous QC

> Any unresolved action items from last month's report. Auto-populated by the workflow.

- [ ] {item from previous report}

---

## 8. Model + tooling notes

- Did Anthropic ship a new Claude model this month? {Y/N — if Y, which one}
- Any Apify scraper changes / failures this month? {Y/N — details}
- Any GitHub Actions workflow failures this month? {Y/N — details}
