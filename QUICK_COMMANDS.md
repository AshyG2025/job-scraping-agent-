# Quick Commands & Prompts Cheatsheet

> **What this is:** Every command, prompt, and shortcut Claude has suggested that you might want to reach for again. Organized by **what you're trying to do**, not by tool. Most are for the Terminal or as messages to Claude in a Claude Code session.
>
> **How Claude uses this:** Per `CLAUDE.md` Rule 6, Claude reads this file at the start of every session and will **proactively surface the relevant entry** when your context matches one of these workflows. You don't need to consult it manually most of the time.
>
> **How you maintain it:** When Claude suggests a useful new pattern during a session, Claude will add it here automatically and tell you it did. You can also add or edit entries freely.
>
> **Last updated:** 2026-05-12 (Phase D shipped: new `python scripts/send_digest.py` (with `--dry-run`) + `python scripts/check_resend.py` diagnostic. Tue/Thu one-liner now chains `&& python scripts/send_digest.py`. Earlier 2026-05-11 — Added `/analyze-jd` slash command — recruiter-grade deep JD analysis, distinct from the lightweight `score_jobs.py` matcher.)

---

## 🚀 Starting and resuming Claude Code

| When you want to... | Run / say... | Notes |
|---|---|---|
| Start Claude Code in this project | `cd "/Users/ashy/Documents/OVERALL JOB STRATEGY/Job Scraping project" && claude` | Always start from this folder so Claude has project memory + reads CLAUDE.md |
| Orient a fresh Claude session | *"I'm continuing work on the job-scraping-agent project. Please read TABLE_OF_CONTENTS.md and CLAUDE.md first to orient yourself, then check your memory for project context, and tell me where we left off + what the current open tasks are."* | Paste as your first message in any new session |
| Resume the most recent conversation in the same folder | `claude --continue` (or short: `claude -c`) | Loads the exact last conversation transcript |
| Pick from past sessions | `claude --resume` | Opens a picker showing past conversations in this folder |
| Exit Claude Code | `/exit` or `Ctrl + D` | Closes the session; conversation is saved |
| Run a shell command from inside Claude Code | Type `! <command>` in the prompt | The `!` prefix sends the command to Bash and shows output in the conversation |

---

## 💬 Telling Claude what to do (common prompts)

| When you want to... | Say to Claude... |
|---|---|
| Save a Claude-generated file local-only (won't go to GitHub) | *"Save this in `_drafts/`"* — files in `_drafts/`, `_local/`, or `scratch/` are gitignored |
| Re-run the eval set against the current scoring prompt | `cat docs/EVAL_SET_JDS.md >> MANUAL_JDS.md && python scripts/score_jobs.py` — then compare `_local/digest.md` scores against targets in `docs/EVAL_SET.md`. Cost ~$0.96 per run (8 entries × ~$0.12). |
| Trigger the calibration deep-dive ritual | *"Run the calibration deep-dive playbook with me. The monthly QC flagged {inversion type}. Walk me through it step by step."* |
| Add a company to the list | *"Add {Company} to COMPANY_LIST.md as Tier {N}, geo {Seattle/SF/London/Multiple}, H1B {✅/⚠️/❌}."* |
| Score a single role manually | *"Score this posting against my scoring prompt: {paste JD}. Use the JSON output schema from SCORING_PROMPT.md."* |
| **Deep recruiter-grade analysis of one JD** (vs the lightweight matcher) | `/analyze-jd <paste JD text or URL>` — produces the 6-section structured brief (Experience Level / Domain Alignment / per-skill ✓✓✓ table / Team Needs with Manageable-Non-issue-Dealbreaker tiers / Role Type Fit / Recommendation). Lives in `.claude/commands/analyze-jd.md`. Use on shortlisted roles only (~$0.30-0.50 per analysis). Catches role-type-mismatch JDs the lightweight matcher misses (Acuity-Analytics-style). |
| Draft a tailored resume / cover letter for a role | *"Open {role link or paste JD}. Pick the right base resume per PROJECT_BRIEF.md, draft the bullet tweaks, and save the result in `_drafts/{Company}-resume.md` so it stays local."* |
| Have Claude commit + push project changes | *"Commit these changes with a message describing what shipped, and push to GitHub."* |
| Verify Claude isn't drifting on accuracy | *"For everything in your last response, cite the source — file path, URL, or memory entry. Flag anything you can't source."* |

---

## 🧠 Memory management

| When you want to... | Say to Claude... |
|---|---|
| See what Claude remembers about you | *"What memories do you have about me?"* |
| Update or correct a memory | *"Update memory: {fact}. Reason: {why it's now accurate}."* |
| Have Claude forget something | *"Forget that I {old fact}."* — Claude removes the relevant memory file |
| Save something durable for future sessions | *"Remember that {fact} for future sessions."* |

---

## 🔧 Git & GitHub

| When you want to... | Run... | Notes |
|---|---|---|
| See what's changed | `cd "/path/to/project" && git status` | Shows modified, staged, and untracked files |
| See line-level changes (unstaged) | `git diff` | Walks you through every `+` (added) / `-` (removed) line in your modified files. Use to sanity-check before staging. |
| See line-level changes (already staged) | `git diff --staged` | Same as above but for the changes currently queued for commit (e.g., from `git rm --cached`). |
| Get a summary of what's changed | `git diff --stat` | One-line-per-file summary: filename + lines added/removed. Quicker than reading the full diff. |
| Commit + push *(usually Claude does this)* | `git add . && git commit -m "..." && git push` | Or just say *"commit and push"* and Claude handles it |
| See commit history | `git log --oneline -20` | Last 20 commits |
| Test SSH auth to GitHub | `ssh -T git@github.com` | Should print *"Hi AshyG2025! ..."* |
| Show your public SSH key | `cat ~/.ssh/id_ed25519.pub` | Safe to share — public is in the name |
| Copy public SSH key to clipboard | `pbcopy < ~/.ssh/id_ed25519.pub` | Mac-only |
| Verify git is using Xcode's binary (not the broken stub) | `which git` should print `/Applications/Xcode.app/Contents/Developer/usr/bin/git` | If it shows `/usr/bin/git`, the PATH in `~/.zshrc` was reset — re-add the export |

---

## 🖥️ Terminal & Mac shortcuts

| When you want to... | Press / type... |
|---|---|
| Open a new Terminal tab in the same window | `Cmd + T` |
| Open a new Terminal window | `Cmd + N` |
| Switch between Terminal tabs | `Cmd + 1`, `Cmd + 2`, ... |
| Open Spotlight (find apps fast) | `Cmd + Space` |
| Cancel a running command | `Ctrl + C` |
| Close the current Terminal tab | `Cmd + W` |
| See a folder's contents | `ls "/path/to/folder"` |
| Go to a folder | `cd "/path/to/folder"` |
| Open `.env` (or any hidden file) in TextEdit | `open -a TextEdit .env` (run from the project root) |
| Toggle hidden files on/off in Finder | `Cmd + Shift + .` (period) |

---

## 🐍 Python pipeline (Phases A + B + C + D)

| When you want to... | Run / say... | Notes |
|---|---|---|
| First-time setup (one-time) | `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` | Creates a virtual env, installs `anthropic` + `python-dotenv` + `requests`. Run from the project root. |
| Activate the venv in a new terminal session | `source .venv/bin/activate` | Prefix changes to `(.venv)` to confirm. Needed before every run. |
| Run the auto-scrapers (~30 named cos + 3 LinkedIn searches) | `python scripts/run_scrapers.py` | Hits each named-co's ATS API + runs Apify actor for the 3 LinkedIn URLs, applies title/geo/age filters, dedupes against `_local/scraped_seen.json`, appends new JDs to `MANUAL_JDS.md`. Prints a per-source funnel summary. ~6–10 min total (Apify is the slow leg at 1–3 min per LinkedIn search). |
| Score whatever's in `MANUAL_JDS.md` | `python scripts/score_jobs.py` | Output: `_local/digest.md` + `_local/scored_results.json` + appended rows in your Google Sheet. Reads `ANTHROPIC_API_KEY` from `.env`. |
| Full pipeline (scrape → score → Sheet → email) | `python scripts/run_scrapers.py && python scripts/score_jobs.py && python scripts/send_digest.py` | Tuesday/Thursday-morning one-liner. ~10–15 min + ~$1.20/run (~$1 Anthropic + ~$0.20 Apify; Resend is free under 3K emails/mo). |
| Send the email digest of the last scoring run | `python scripts/send_digest.py` | Reads `_local/scored_results.json`, filters to roles ≥6/10 (override via `DIGEST_SCORE_THRESHOLD` in `.env`), emails to `DIGEST_RECIPIENT_EMAIL`. Skips emailing when 0 roles meet threshold. |
| Preview the email body without sending | `python scripts/send_digest.py --dry-run` | Prints subject + body to terminal. Use to sanity-check formatting before sending. |
| Verify the Google Sheet connection | `python scripts/check_sheets.py` | Prints `✅ Connected. Sheet title: ...` on success. Run after Phase C setup or any time scoring stops writing to the Sheet. |
| Verify Resend (email) is wired | `python scripts/check_resend.py` | Sends one short test email to `DIGEST_RECIPIENT_EMAIL`. Run after Phase D setup or any time `send_digest.py` stops delivering. |
| Verify the Apify token + LinkedIn actor | `python -c "from dotenv import load_dotenv; import os; load_dotenv(); from apify_client import ApifyClient; print(ApifyClient(token=os.environ['APIFY_API_TOKEN']).actor('curious_coder/linkedin-jobs-scraper').get()['name'])"` | Should print `linkedin-jobs-scraper`. Use after rotating the token or if `run_scrapers.py` stops returning LinkedIn results. |
| Re-do the Phase C setup (key rotation, new machine, etc.) | Open `docs/PHASE_C_SETUP.md` | The 9-step walkthrough is the canonical path. Time: ~10–15 min. |
| Re-do the Phase D setup (Resend key rotation, new recipient, etc.) | Open `docs/PHASE_D_SETUP.md` | 4-step walkthrough. Time: ~5 min. |
| Deactivate the venv | `deactivate` | Drops the `(.venv)` prefix; reverts to system Python. |

---

## 📁 Project-specific files (most-edited)

| When you want to... | Open / edit... |
|---|---|
| Change what counts as a "good role" | `PROJECT_BRIEF.md` |
| Add or remove a company | `COMPANY_LIST.md` |
| Change pre-LLM filter rules | `HARD_FILTERS.md` |
| Tune scoring weights or thresholds | `SCORING_PROMPT.md` § TUNABLE PARAMETERS (top of file) |
| Add a real-world calibration example | `docs/EVAL_SET.md` |
| Run the monthly QC ritual | `QC_PROCESS.md` (read), then `docs/qc-reports/YYYY-MM.md` (fill in) |
| Run the inversion deep-dive | `docs/CALIBRATION_DEEP_DIVE.md` (with Claude Code in a session) |
| Find any other file | `TABLE_OF_CONTENTS.md` |

---

## ➕ How to add an entry to this cheatsheet

If a useful command or prompt comes up that isn't here:

1. **Easiest:** Just tell Claude *"Add this to QUICK_COMMANDS.md"* — it'll find the right section and append the entry.
2. **Manual:** Edit this file directly. Follow the existing table format (`| When you want to... | Run / say... | Notes |`). Bump the **Last updated** date at the top.
3. Per `CLAUDE.md` Rule 6, Claude will also auto-add entries it suggests during sessions. You'll see *"Added this to `QUICK_COMMANDS.md` for next time."* when it does.

---

## 🚫 What NOT to put here

- Long workflows (those go in their own `.md` file, with a link from `TABLE_OF_CONTENTS.md`)
- Sensitive credentials (API keys, passwords, SSH private keys — never commit these anywhere)
- Project-specific knowledge that belongs in memory or `PROJECT_BRIEF.md`
- Theoretical commands you've never tested — only entries that actually work
