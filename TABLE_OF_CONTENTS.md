# Table of Contents — Where Things Live + When to Use Them

> **What this file is for:** This is your navigation map. The project has ~12 docs across the root + `docs/` folder, and each one controls something specific. Use this file when you've forgotten where something lives, when you're starting a workflow you haven't done before, or when you're orienting a future Claude session that hasn't seen this project yet.
>
> **How to read it:**
> - **Section 1 (Quick lookup)** — start here. "When X happens, go to Y." This is what you'll use 90% of the time.
> - **Section 2 (Each file & folder explained)** — deeper reference. What each file does, how to use it, and concrete use cases.
> - **Section 3 (When to consult this TOC)** — meta — when to open this file in the first place.
>
> **Last updated:** 2026-04-27

---

## 📍 Section 1 — Quick lookup (by trigger)

The most common workflows you'll do, and exactly where to go.

### Daily / weekly use

| When this happens... | Go to... | What you'll do (~time) |
|---|---|---|
| I receive the digest email | Email inbox + Google Sheet | Read top matches; mark `applied` Yes/No (~5 min) |
| I just applied to a role | Google Sheet | Update `applied`, `applied_date`, `outcome_status: open` (~30 sec) |
| A recruiter responded / I got a phone screen / interview / offer / rejection | Google Sheet | Update `outcome_status` + `outcome_date` + optional `outcome_notes` (~1 min) |
| I want to look at a role's full reasoning trace | Google Sheet → `qc_deep_dive` column | Read; sanity check the score |
| I disagree with a specific score | Comment in Google Sheet for now → flag at next monthly QC | (See below) |

### Adding / changing what the agent looks at

| When this happens... | Go to... | What you'll do |
|---|---|---|
| I learn about a new company I want to track | `COMPANY_LIST.md` | Add a bullet under the right tier; commit |
| I want to drop a company entirely | `COMPANY_LIST.md` | Move to `Skip` section or delete; commit |
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

#### `PROJECT_BRIEF.md`
- **What it is:** Your "ideal next role" definition + flagship-project descriptions + resume-selection rules. The matcher's primary anchor.
- **How to use it:** Read this when you want to remind yourself what counts as "good." Edit when your career direction shifts.
- **Use cases:**
  - "What types of roles am I actually looking for?" → read § Role brief
  - "What did I do at Amazon, with real metrics?" → read § Three flagship project anchors
  - "Should this role's resume start from Platform PM or generic?" → § Resume selection guidance
- **When to edit:** Career-direction shifts (e.g., "I'm now also open to data platform roles"), updated metrics on flagship projects, comp expectations changing

#### `COMPANY_LIST.md`
- **What it is:** Tier 1/2/3/Skip company list + Discovery sources (LinkedIn, TrueUp, YC Work at a Startup, VC portfolio boards). Source of truth for the H1B filter.
- **How to use it:** Add/remove companies; promote discovery roles into named tiers.
- **Use cases:**
  - You read about Stripe acquiring Bridge → add to Tier 1 or Tier 2
  - You decide to deprioritize a sector → move to Skip
  - QC report says "Liberis surfaced 3 strong matches via discovery" → promote Liberis from Tier 1 (already there) or document the trend
- **When to edit:** Anytime you learn of a new company; at every monthly QC

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

### `docs/` folder

#### `docs/EVAL_SET.md`
- **What it is:** 6 manually-labeled gold-standard postings + their target scores. The test fixture for every prompt change.
- **How to use it:** Reference when validating a prompt change. Append outcome-validated examples each month.
- **Use cases:**
  - You changed the prompt → re-run all 6 and confirm scores within ±1 of target
  - You applied to a role + got rejected at score 8 → consider adding it as a labeled "should have been a 5" example
- **When to edit:** Every monthly QC (1–2 new examples typically); after any prompt version bump (record actual scores)

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
- **What it is:** Your two base resumes. The asset matcher picks one as the starting point for any role scored ≥ 7.
- **How to use it:** Keep current versions here. The agent reads filenames + content during asset matching.
- **Use cases:**
  - Resume update after a project shipped → replace the file
  - New resume variant for a domain → add as a third file + update `PROJECT_BRIEF.md` § Resume selection guidance to add a routing rule
- **When to edit:** Whenever your resumes change

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
