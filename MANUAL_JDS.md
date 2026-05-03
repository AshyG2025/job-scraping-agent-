# Manual JD Paste-in

> **What this file is for:** Paste job descriptions here that the auto-scrapers missed (e.g. roles you saw logged-in on LinkedIn). The next run of `python scripts/score_jobs.py` will score every entry below, write the results to `_local/scored_results.json` + `_local/digest.md`, and archive your entries to `MANUAL_JDS_PROCESSED.md`.
>
> **Format per entry** (copy the `[TEMPLATE]` block below for each new JD):
>
> - Heading: `## Company — Job Title`
> - Metadata lines: URL is recommended; Posted (in days) and Applicants (number) are optional. If you don't know them, leave blank — the noise penalty in `SCORING_PROMPT.md` won't fire without both.
> - JD text goes between `---` markers.
>
> **Don't worry about formatting the JD text** — paste it raw, line breaks and bullets and all. The model reads the whole thing.
>
> **Skipping an entry?** Add `[done]` anywhere in the heading line and the runner will ignore it (e.g. `## Stripe — Senior PM [done]`).

---

## [TEMPLATE] Company Name — Job Title
**URL:** https://...
**Posted:** 5 days ago
**Applicants:** 32

---
Paste the full job description text here.

Multiple paragraphs are fine. Bullet points are fine. Don't bother cleaning anything up.
---

<!-- ENTRIES BELOW -->
