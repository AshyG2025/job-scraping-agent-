# Calibration Deep-Dive Playbook

> **When this is triggered:** The monthly QC report detects **inverted calibration** — a lower score band converting at a higher rate than a higher one (e.g., 7–8s getting more recruiter responses than 9–10s, or 5–6s outperforming 7–8s).
>
> **What inverted calibration means:** The rubric is fundamentally broken. Tuning a weight by 0.05 won't fix it. The dimensions, definitions, or weights are mis-modeling reality. This playbook is the structured root-cause session you run with Claude Code to find and fix it.
>
> **Time commitment:** 60–90 minutes, in one session. Don't split across days — context loss kills the diagnostic.
>
> **Sign-off requirement:** No prompt changes are committed without re-running the eval set + the past month's actual applications and confirming the new prompt no longer inverts.

---

## Inversion detection rules

The monthly QC fires this playbook when **any** of these are true (and sample size in each band is ≥ 8):

| Inversion type | Trigger | Severity |
|---|---|---|
| Adjacent band swap | Conversion rate of band [n] > conversion rate of band [n+1] | 🟡 Investigate |
| Multi-band swap | Conversion rate of band [n] > conversion rate of band [n+2] | 🚨 Critical |
| Top-band collapse | 9–10 conversion < 7–8 conversion AND 9–10 conversion < 5–6 conversion | 🚨 Critical |
| Funnel inversion | A lower score band has higher conversion at *interview* stage (not just response) | 🚨 Critical (deepest signal — recruiters might respond to anyone, but interviews are filtered) |

Any 🚨 → email subject: *"🚨 Inverted calibration — deep dive required"* and run halts new applications until fixed.

---

## How to run the session

When you get the alert, open Claude Code in the project folder and start a conversation with:

> *"Run the calibration deep-dive playbook with me. The monthly QC flagged {inversion type}. Walk me through it step by step."*

Claude Code follows the structure below. You don't memorize the steps — Claude Code drives, you respond.

---

## Phase 1 — Reconstruct the inversion (10 min)

**Goal:** Understand exactly which roles drove the inversion. Not just the aggregate numbers — the actual postings.

Claude Code pulls from the Google Sheet:
- All applications scored 9–10 in the past 90 days, with their outcomes
- All applications scored 7–8 in the past 90 days, with their outcomes
- All applications scored 5–6 in the past 90 days, with their outcomes
- For each: the original `reasoning_trace` and (if present) `qc_deep_dive` from the time of scoring

Print three side-by-side cohorts. Read them.

**Diagnostic questions:**
1. Are the 9–10s mostly from one company / one source? (e.g., all Wise roles got 9, but Wise stopped responding) — could be a *company-level* issue, not a rubric issue
2. Were the 9–10s scored by an old prompt version that's since been changed?
3. Of the 9–10s that didn't convert, what's the most-common reason in `outcome_notes`? (e.g., "no response," "rejected — over-qualified," "rejected — under-experienced")

**Output of Phase 1:** A 2-sentence statement of *what's actually happening* — e.g., *"Most 9–10s are FinTech ledger roles where I'm being rejected as 'not enough treasury experience.' Most 7–8s are integration platform roles with broader domain matching, where my Amazon experience is more legible."*

If Phase 1 reveals a *non-rubric* root cause (sample bias, single bad company, prompt version mix), **stop and fix that first** — don't proceed to dimension surgery.

---

## Phase 2 — Locate which dimension is mis-scoring (15 min)

**Goal:** For each high-scored-low-conversion role, identify which dimension is scoring too high.

For each 9–10 that didn't convert, Claude Code asks:
- Look at the original `reasoning_trace` for this role.
- Re-read the JD with the outcome in mind. Now that you know what happened (e.g., rejected for under-experience), which dimension's reasoning was wrong?
  - **Was domain over-rated?** Did the model treat an adjacent platform type as a direct match?
  - **Were skills over-rated?** Did the model assume your experience covered something it didn't?
  - **Was level over-rated?** Did the JD ask for more years/scope than the model gave it weight for?
  - **Were team-needs over-rated?** Did the model misread what the team actually wants?

Tag each non-converting 9–10 with the dimension(s) you think were over-rated.

For each 7–8 that *did* convert, do the inverse — which dimension was *under*-rated?

**Output of Phase 2:** A tally — e.g., *"Of 7 non-converting 9–10s, 5 had over-rated `level`. Of 4 converting 7–8s, 3 had under-rated `team_needs`."*

---

## Phase 3 — Diagnose the root cause (15 min)

**Goal:** Understand *why* the over-rated dimension is over-rating.

Once you know which dimension is the culprit, Claude Code walks through these root-cause options:

### If `domain` is over-rating

- Is the dimension definition in `SCORING_PROMPT.md` too generous about what counts as "direct match"?
- Are sub-domains being treated as the parent domain? (e.g., "treasury ledger" lumped in with "data integration" — both are "multi-system" but require different evidence)
- Has `PROJECT_BRIEF.md` over-claimed your platform experience?

### If `skills` is over-rating

- Is the model pattern-matching keywords (JD says "API" → bonus points) instead of evidence-mapping?
- Are flagship-project skill claims in `PROJECT_BRIEF.md` too broad?
- Is the model giving credit for skills that *transfer* in theory but not in interviews?

### If `level` is over-rating

- Is "Senior" being applied to roles that are actually Staff/Principal in scope?
- Does the JD use "Senior" but require 10+ years and Staff-level scope?
- Is the model not weighting the YoE requirement strictly enough?

### If `team_needs` is over-rating

- Is the model inferring team needs from the JD that aren't actually there?
- Is it under-weighting explicit "must-have" requirements?
- Is company-level context (stage, recent funding, recent press) being ignored when it should matter?

**Output of Phase 3:** A 1-sentence root cause — e.g., *"The `level` dimension is treating Senior-titled roles at growth-stage cos. as at-bar even when they require 10+ years of treasury domain experience."*

---

## Phase 4 — Propose specific fixes (15 min)

**Goal:** Concrete, testable changes to `SCORING_PROMPT.md`, `PROJECT_BRIEF.md`, or `HARD_FILTERS.md`.

Claude Code drafts 2–3 candidate fixes. Each fix must:
- Be specific (a sentence or paragraph that gets edited, not "tighten the rubric")
- Predict the impact (which eval-set scores will change, which non-converting roles would have been rated lower)
- Be reversible (note the current text alongside the proposed text)

**Examples of good fixes:**

> **Fix 1: Tighten `level` dimension definition.**
> Add to dimension 3: *"If the JD requires specific multi-year domain experience that Ayesha doesn't have (e.g., 'extensive treasury experience'), cap level_score at 5 even if the title says Senior."*
> Predicted impact: Wise Treasury 9 → 7, Boku 3 → 3, eval set still calibrated within ±1.

> **Fix 2: Add explicit hard filter.**
> In `HARD_FILTERS.md`, add: *"DROP if JD body contains 'extensive [domain] experience' for a domain not in {integration, platform, B2B, FinTech-rails}."*
> Predicted impact: 4 roles from past month would have been filtered before scoring.

> **Fix 3: Refine `PROJECT_BRIEF.md` flagship descriptions.**
> Change Mexico Tax Recon framing from *"financial operations platform"* to *"financial operations platform — adjacent to but distinct from treasury / live-ledger work."*
> Predicted impact: Domain dimension stops over-counting Mexico for treasury roles.

---

## Phase 5 — Test before commit (10 min)

**Goal:** Don't ship a fix that breaks the eval set.

For each candidate fix:
1. Apply the fix in a draft (don't commit yet)
2. Re-run `docs/EVAL_SET.md` — record the new scores
3. Re-run the past-month conflict cohort — would the new prompt have flagged the non-converters as ≤ 7?
4. Compare:
   - Does the fix preserve all 6 eval-set scores within ±1 of target? (If not, the fix is too aggressive — back off.)
   - Does the fix actually drop the non-converters into the right band? (If not, the fix is wrong — back to Phase 3.)

If both pass, the fix is ready to ship.

---

## Phase 6 — Commit + log (5 min)

1. Apply the fix to the relevant file(s)
2. Bump `prompt_version` in `SCORING_PROMPT.md` (minor → major depending on scope)
3. Add an entry to the **Iteration log** at the bottom of `SCORING_PROMPT.md`:
   ```
   | v1.2 | 2026-06-14 | Tightened `level` dimension to cap at 5 when JD requires absent domain experience | Fixed inversion detected in May QC: 7-8s outperforming 9-10s on FinTech ledger roles | Eval set unchanged (all within ±1); 4 of 7 non-converting 9–10s now correctly score 6–7 |
   ```
4. Commit with a clear message:
   ```
   git commit -m "Calibration fix: SCORING_PROMPT v1.1 → v1.2

   Inverted calibration detected May 2026 (7-8 conversion > 9-10 conversion).
   Root cause: level dimension treating Senior-titled roles as at-bar despite
   missing required domain depth.
   Fix: cap level_score at 5 when JD requires extensive non-platform domain experience.
   Tested against EVAL_SET (no change) and May conflict cohort (4/7 corrected)."
   ```
5. Update the QC report to log:
   - The inversion was detected
   - The root cause
   - The fix shipped
   - Predicted impact on next month's calibration

---

## What NOT to do during a deep dive

- **Don't tweak weights as a first move.** If `domain` weight changes from 0.30 to 0.35, that's a small shift. If the dimension itself is mis-defined, no weight will save it. Definitions before weights.
- **Don't add a new dimension casually.** A 5th dimension means re-balancing all weights and re-validating against the eval set. Only add when the existing 4 truly can't capture the signal.
- **Don't ship without re-running the eval set.** Fixing the inversion at the cost of breaking the gold standard is a regression, not a fix.
- **Don't fix multiple issues at once.** One root cause, one fix, one version bump. If you ship 3 changes together and the next month's QC is worse, you can't tell which change caused it.
- **Don't skip Phase 1.** Sometimes the "inversion" is a sample-size artifact or single-company effect, not a rubric problem. Phase 1 catches that before you do unnecessary surgery.

---

## Sign-off checklist before committing the fix

- [ ] Phase 1 confirmed it's a rubric issue, not sampling/bias
- [ ] Phase 2 identified the specific over-/under-rating dimension(s)
- [ ] Phase 3 named the root cause in one sentence
- [ ] Phase 4 produced a concrete, testable fix (not "tighten the rubric")
- [ ] Phase 5 confirmed eval-set still calibrated within ±1 of targets
- [ ] Phase 5 confirmed the conflict cohort would have been correctly scored
- [ ] Iteration log entry written
- [ ] `prompt_version` bumped
- [ ] Commit message names the inversion, root cause, fix, and tested impact

If any box is unchecked, don't commit. The deep-dive ritual exists because rubric drift is hard to undo once shipped.
