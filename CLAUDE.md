# Project Rules — Job Scraping Agent

This file is read by Claude at the start of every session in this project. The rules below override default behavior.

---

## Rule 1: Accuracy is non-negotiable. Verify before recommending.

This project surfaces **real job opportunities at real companies** and influences which roles I apply to. Hallucinating a company, an H1B status, a salary band, or a job link is worse than returning nothing — it wastes my time and could cost me opportunities.

**For every fact, claim, or recommendation you make:**

1. **State the source.** When recommending a company, citing H1B status, naming a role, or quoting a JD, point to where the information came from (the file, the URL, the prior conversation, the search result).
2. **If you're not sure, say so.** Use `⚠️` to flag anything unverified or low-confidence. It's better to surface 5 verified roles + 2 flagged unknowns than 7 confidently-stated guesses.
3. **Never invent.** Do not make up:
   - Company names
   - Job titles or job links
   - H1B sponsorship status (default to `⚠️ verify` unless you have evidence)
   - Salary or comp ranges
   - JD content (always quote from the actual posting; never paraphrase what you'd expect a posting to say)
   - Recruiter names, hiring manager names, or LinkedIn profiles
4. **Verify URLs before suggesting them.** If you suggest "apply at company.com/careers/12345," that URL must come from a real scrape result. Don't construct URLs by pattern.
5. **When the rubric says ≥7/10, the agent does asset matching.** Don't inflate scores to trigger the asset matcher; if a role is a 6, score it a 6.
6. **For resume tweaks, every claim must be 100% defensible** — refer to the authenticity guardrails in `Job Posting samples/Platform PM Role ANALYZER - Instructions.docx` (the "TONE & AUTHENTICITY" section). No fabricated metrics; no inflated scope; no architecture claims I can't defend in a technical interview.

**When you're uncertain, the right move is to ask me, not to guess.**

---

## Rule 2: This is a non-developer's project. Explain before you change things.

I'm a technical PM, not a software engineer. I don't write Python or TypeScript.

- Before introducing new code or a new dependency, explain in plain English what it does and why it's the right choice.
- Don't add code that I couldn't reason about with a 30-second explanation.
- For any file change touching code, include a short top-of-file comment that summarizes its purpose for non-developer reviewers.
- Prefer the path with the **least code I have to maintain** (managed services, GitHub Actions over self-hosted, Sheets over a database, ready-made scrapers over DIY).

---

## Rule 3: Authenticity over polish.

When recommending resume tweaks, cover-letter angles, or how to position my experience for a role:

- Better to undersell than oversell. Authenticity protects my long-term credibility.
- Never claim infrastructure platform experience for integration-platform work, or "external developer ecosystem" for B2B-partner work.
- Numbers I cite (1,000+ users, $9.6M, 80%+ adoption) are real and should not be inflated. If you're tempted to round up, don't.
- Mark borderline reframes with `⚠️` and ask before using them.

---

## Rule 4: Memory updates.

When I make a decision, change a constraint, or share new context, update the relevant memory file in `~/.claude/projects/.../memory/`. Don't let memory drift from current reality.

---

## Rule 5: Keep `TABLE_OF_CONTENTS.md` current.

Whenever you **add, rename, or delete** a file or folder in this project, also update `TABLE_OF_CONTENTS.md` in the same change. Specifically:

- **Adding a file/folder** → add a row in Section 1 (if there's a trigger workflow that uses it) **and** a sub-section in Section 2 with what / how / use cases / when to edit.
- **Renaming a file/folder** → update every reference to the old name across both Section 1 and Section 2 (and any other doc that links to it — `grep` first).
- **Deleting a file/folder** → remove all rows in Section 1 and the sub-section in Section 2.
- **Changing a workflow** (e.g., we move outcome tracking from Google Sheets to Notion) → update the affected rows in Section 1.

If you can't find the right place to add a new entry, **ask me where it goes — don't ship the file change alone.** A new file without a TOC entry is a half-finished change; the project's discoverability depends on the TOC staying complete.

The TOC also has a "Last updated" date at the top — bump it when you make TOC changes.

---

## Rule 6: Use and maintain `QUICK_COMMANDS.md`.

`QUICK_COMMANDS.md` is a cheatsheet of every command, prompt, and shortcut that's been useful in this project. **Read it at the start of every session in this project.**

### Proactive surfacing

When the user describes a situation that has a clear matching entry in `QUICK_COMMANDS.md`, **surface the entry inline at the top of your response** before doing anything else, formatted as:

> 📋 *Quick reference: `{exact command or prompt}` — {one-clause context}. (From `QUICK_COMMANDS.md`.)*

Then continue with your normal response.

**When NOT to surface:**
- The command is already what you're about to run yourself (don't show the user a command and then immediately run it for them)
- The user is asking a conceptual question that doesn't map to a single command
- The matching entry is trivial or already obvious from the conversation

When in doubt, do surface. False positives are mild noise; false negatives waste the cheatsheet's value.

### Auto-appending new entries

When you propose a new command, prompt, or shortcut during a session that the user might want to use again, **append it to `QUICK_COMMANDS.md`** in the appropriate section (`Starting and resuming Claude Code` / `Telling Claude what to do` / `Memory management` / `Git & GitHub` / `Terminal & Mac shortcuts` / `Project-specific files`). Then tell the user briefly:

> *"Added this to `QUICK_COMMANDS.md` for next time."*

Bump the **Last updated** date at the top of the file when you append.

**Don't add entries that are:**
- Sensitive (credentials, secrets, full SSH keys)
- One-off / project-specific knowledge that belongs in memory or `PROJECT_BRIEF.md`
- Untested or speculative commands

---

## Rule 7: Keep public/private file pairs in sync.

Two source-of-truth files are kept local-only (gitignored) with public-facing portfolio copies committed to GitHub:

| Local source-of-truth (read by the runner) | Public copy (on GitHub for portfolio) |
|---|---|
| `COMPANY_LIST.md` | `COMPANY_LIST_PUBLIC.md` |
| `PROJECT_BRIEF.md` | `PROJECT_BRIEF_PUBLIC.md` |

The local files are read by the scoring runner (`scripts/score_jobs.py`) and asset matcher; the public files exist only as portfolio-friendly framework summaries with personal/strategic detail anonymized.

**When the local file changes, automatically update the public copy in the same edit** — anonymized per the patterns already established in the public files (named companies → category descriptors; personal / visa / comp / contact-network reveals → omit; file-pathed resume routing → generic "Domain-tailored variant (X)" descriptors).

**When to propagate to the public copy:**
- New tier or sub-tier added to the framework
- H1B-filter or hard-filter logic changes
- Role brief, "great match" / "weak match" criteria, or geography rules change
- Flagship project anchors added / removed, or canonical metrics updated
- Resume-selection routing logic changes

**When NOT to propagate:**
- Adding / removing / re-tiering a specific company (the public copy doesn't enumerate companies)
- Editing the Referral Network list, comp section, or other sections that don't appear in the public copy

After updating the public copy, bump its `**Last updated:**` line at the top.

---

## Quick references

- **Navigation map (start here when lost):** `TABLE_OF_CONTENTS.md`
- **Cheatsheet (commands + prompts):** `QUICK_COMMANDS.md`
- **Resumes:** `Ayesha Resume/`
- **Sample JDs (gold set):** `Job Posting samples/JD mapping to my exp..docx`
- **Platform PM Analyzer (the scoring brain):** `Job Posting samples/Platform PM Role ANALYZER - Instructions.docx`
- **Project brief (what counts as a good role):** `PROJECT_BRIEF.md` *(local-only working copy; public framework summary at `PROJECT_BRIEF_PUBLIC.md`)*
- **Companies in scope:** `COMPANY_LIST.md` *(local-only working copy; public framework summary at `COMPANY_LIST_PUBLIC.md`)*
- **Pre-LLM filter rules:** `HARD_FILTERS.md`
