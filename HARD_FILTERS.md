# Hard Filters

> **How this file is used:** These rules run **before** any LLM scoring. A job posting that fails any of these filters is dropped from the pipeline entirely. The point is to save Claude API tokens (and your eyeballs) on roles that are obvious no-gos.
>
> **Last updated:** 2026-05-19 (Section 3 — temporary London-only geo restriction added as a cost guardrail; US scope paused. See Section 3 banner.) Earlier 2026-04-27.

---

## 1. Title filter — IC roles only

**KEEP** if title contains any of:
- `Product Manager` / `Senior Product Manager` / `Sr. Product Manager`
- `Staff Product Manager` / `Sr. Staff Product Manager`
- `Principal Product Manager`
- `Product Lead` (only if the JD body confirms IC scope; manager-style "Product Lead" titles get caught by the people-management filter below)
- `Group Product Manager` (borderline — pass through to LLM scoring with a flag; some companies use this as IC, some as managerial)

**DROP** if title contains any of:
- `Director`, `Sr. Director`, `Senior Director`
- `VP`, `Vice President`, `Head of`
- `Manager of Product`, `Manager, Product`
- `Engineering Manager`, `Design Manager`
- `Chief Product Officer`, `CPO`
- Any title implying direct reports (`Manager of PMs`, etc.)

**DROP** levels below Senior:
- `Product Manager I` / `Product Manager II` (entry / mid-level)
- `Associate Product Manager` / `APM`
- `Junior Product Manager`

---

## 2. People-management filter — JD body check

Drop the role if the JD body contains explicit people-management language, even if the title looked OK:

- "manage a team of \\d+ PMs"
- "lead a team of product managers"
- "you will hire / coach / mentor a team of"
- "direct reports"
- "people management responsibilities"

(Keyword-based first pass; LLM does the nuanced check on borderline cases.)

---

## 3. Geography filter

> ⚠️ **TEMPORARY RESTRICTION (added 2026-05-19): London-only.** US scope (Seattle / SF Bay / Remote — US) is paused as a cost guardrail after a busy run on 2026-05-19 surfaced 42 net-new roles and ran into Anthropic API credit exhaustion mid-scoring. Each scoring call costs ~$0.15, so a 100-role run = ~$15. Restricting to London cuts typical run cost to ~$1–2.
>
> **To restore full scope:** uncomment the US patterns in `scripts/scrapers/common.py` (lines 60-77) AND re-enable the Seattle + SF Bay LinkedIn search entries in `scripts/run_scrapers.py` (the two commented-out entries near line 95). Then revert this banner and the KEEP list below.

**KEEP** if location contains any of (case-insensitive):
- `London`, `Greater London`
- `Remote — UK` *(unconditional)*

**DROP** all other geos, including the previously-allowed US scope:
- ~~`Seattle`, `Bellevue`, `Redmond`~~ *(paused 2026-05-19)*
- ~~`San Francisco`, `SF`, `Bay Area`, `Palo Alto`, `Mountain View`, `Menlo Park`, `Sunnyvale`, `San Jose`, `Oakland`, `Berkeley`~~ *(paused 2026-05-19)*
- ~~`Remote — US`~~ *(paused 2026-05-19)*
- New York / NYC, Boston, Austin, Chicago, Los Angeles, Denver, Miami, etc.
- Manchester, Edinburgh, Dublin, Berlin, Paris, Amsterdam, Singapore, Sydney, etc.
- Anywhere in India, despite past work history there

**Hybrid / on-site / remote modality** — all three OK; not a filter dimension.

---

## 4. H1B sponsorship filter (US roles only)

For any role located in the US, cross-reference the company against `COMPANY_LIST.md`:

| Status in COMPANY_LIST | Action |
|---|---|
| ✅ H1B-friendly (Tier 1 / Tier 2 confirmed) | Pass through to scoring |
| ⚠️ Unclear H1B track record | Pass through with `h1b_warning: true` flag — show in digest with ⚠️ badge so user can research before applying |
| ❌ Known not to sponsor (or company size < 200 employees and not on confirmed list) | DROP |
| Unlisted company | Pass through with `h1b_warning: true` |

UK roles bypass this filter entirely (British citizen).

---

## 5. Seniority sanity check (LLM-assisted, not hard rule)

Years-of-experience requirements:
- `< 4 years` required → DROP (under-leveled for me)
- `4–8 years` required → KEEP (Senior band)
- `8–12 years` required → KEEP (Senior / Staff band)
- `12+ years` required → KEEP (Staff / Principal band — lead with longest tenure stories)
- No years stated → KEEP and let LLM judge from JD scope

---

## 6. Posting freshness

- **KEEP** postings ≤ 14 days old
- **DROP** postings > 30 days old (likely already filled or stale)
- **Flag** postings 14–30 days old as "older — apply soon if interested"

(Discovery-mode pulls from LinkedIn often include older jobs; career-page scrapers usually only show fresh ones.)

---

## 7. Deduplication

The same role can appear on LinkedIn, TrueUp, AND the company career page. The agent should keep one canonical record, preferring the company career page > LinkedIn > TrueUp > Indeed.

Dedup key: `(company_normalized, title_normalized, location_normalized)`.
