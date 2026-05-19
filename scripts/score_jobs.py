"""
score_jobs.py — Phase A scoring runner for the job-scraping agent.

What this file does, in plain English:
  1. Reads JDs Ayesha has pasted into MANUAL_JDS.md.
  2. For each JD, sends it to the Claude API along with three context files
     (SCORING_PROMPT.md + PROJECT_BRIEF.md + COMPANY_LIST.md) that tell Claude
     how to score it. The three context files are cached after the first call,
     so you only pay full price once per run.
  3. Parses the JSON output Claude returns and writes:
       - _local/scored_results.json   (the raw structured data)
       - _local/digest.md             (a human-readable summary)
  4. Archives processed entries to MANUAL_JDS_PROCESSED.md so the same JD
     isn't re-scored next run.

Run from the project root:
    source .venv/bin/activate
    python scripts/score_jobs.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# --- Tunables (change here, no code edits elsewhere) ---
MODEL = "claude-opus-4-7"
EFFORT = "high"
MAX_TOKENS = 8000

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "MANUAL_JDS.md"
PROCESSED_FILE = PROJECT_ROOT / "MANUAL_JDS_PROCESSED.md"
OUTPUT_DIR = PROJECT_ROOT / "_local"
RESULTS_JSON = OUTPUT_DIR / "scored_results.json"
DIGEST_MD = OUTPUT_DIR / "digest.md"

CONTEXT_FILES = [
    PROJECT_ROOT / "SCORING_PROMPT.md",
    PROJECT_ROOT / "PROJECT_BRIEF.md",
    PROJECT_ROOT / "COMPANY_LIST.md",
]


def load_system_prompt() -> str:
    """Concatenate the three context files into a single system prompt."""
    parts = []
    for f in CONTEXT_FILES:
        parts.append(f"<<< {f.name} >>>\n{f.read_text()}\n<<< END {f.name} >>>")
    return "\n\n".join(parts)


def parse_manual_jds(text: str) -> list[dict]:
    """
    Parse MANUAL_JDS.md into a list of entries.

    Each entry starts with `## Company — Title` and may include URL, Posted,
    and Applicants metadata fields. The JD body lives between `---` markers.
    Entries marked `[done]` in the heading are skipped.
    """
    entries = []
    headers = list(re.finditer(r"^##\s+(.+)$", text, re.MULTILINE))
    for i, m in enumerate(headers):
        title_line = m.group(1).strip()
        if "[done]" in title_line.lower() or "[template]" in title_line.lower():
            continue

        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[start:end]

        # Split company and title (separator is "—" em dash, "–" en dash, or "-")
        parts = re.split(r"\s+[—–-]\s+", title_line, maxsplit=1)
        company = parts[0].strip()
        title = parts[1].strip() if len(parts) > 1 else ""

        url = _grab_field(block, "URL")
        posted_raw = _grab_field(block, "Posted")
        applicants_raw = _grab_field(block, "Applicants")
        source_raw = _grab_field(block, "Source")
        jd_body = _grab_jd_body(block)

        entries.append({
            "company": company,
            "title": title,
            "url": url,
            "posting_age_days": _parse_int(posted_raw),
            "applicants_count": _parse_int(applicants_raw),
            "source": _parse_source(source_raw),
            "jd_text": jd_body,
        })
    return entries


def _grab_field(block: str, name: str) -> str | None:
    m = re.search(rf"\*\*{name}:\*\*\s*(.+)", block)
    return m.group(1).strip() if m else None


def _grab_jd_body(block: str) -> str:
    # Split on `---` only when it appears on its own line — URLs in metadata
    # often contain `---` (e.g. Workday job URLs), so a naive split scrambles
    # the entry. Body is between the first and second on-its-own-line markers.
    parts = re.split(r"^---\s*$", block, flags=re.MULTILINE)
    return parts[1].strip() if len(parts) >= 3 else block.strip()


def _parse_int(raw: str | None) -> int | None:
    if not raw:
        return None
    m = re.search(r"\d+", raw)
    return int(m.group()) if m else None


def _parse_source(raw: str | None) -> str:
    """Extract the ATS / channel name from the Source field, e.g.
    `greenhouse (auto-scraped)` → `greenhouse`. Defaults to `manual` for
    paste-in entries that have no Source field."""
    if not raw:
        return "manual"
    return raw.split("(", 1)[0].strip().lower() or "manual"


def build_user_message(entry: dict) -> str:
    """Build the per-JD user-turn content sent to Claude."""
    return f"""Score this job posting against Ayesha's profile using the
scoring framework in the system prompt.

Company: {entry["company"]}
Title: {entry["title"]}
URL: {entry["url"] or "(not provided)"}
posting_age_days: {entry["posting_age_days"] if entry["posting_age_days"] is not None else "unknown"}
applicants_count: {entry["applicants_count"] if entry["applicants_count"] is not None else "unknown"}

Job description:
---
{entry["jd_text"]}
---

Output ONLY a single JSON object matching the schema in SCORING_PROMPT.md.
No preamble, no markdown code fences, no prose after the JSON. The pipeline
parses the entire response as JSON, so anything outside the object will fail."""


def extract_json(text: str) -> dict:
    """Pull a JSON object out of the model response, tolerating fences/prose."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    m = re.search(r"(\{.*\})", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    raise ValueError("No JSON object found in response")


def score_one(client: anthropic.Anthropic, system_prompt: str, entry: dict) -> tuple[dict, dict]:
    """Send one JD to Claude, return (parsed JSON result, usage dict)."""
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        output_config={"effort": EFFORT},
        system=[{
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": build_user_message(entry)}],
    ) as stream:
        message = stream.get_final_message()

    text = "".join(b.text for b in message.content if b.type == "text")
    parsed = extract_json(text)
    usage = {
        "input_tokens": message.usage.input_tokens,
        "cache_creation_input_tokens": message.usage.cache_creation_input_tokens,
        "cache_read_input_tokens": message.usage.cache_read_input_tokens,
        "output_tokens": message.usage.output_tokens,
    }
    return parsed, usage


def build_digest(results: list[dict]) -> str:
    """Render a human-readable markdown digest of the scoring results."""
    lines = [
        f"# Scoring Digest — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Scored {len(results)} role(s).",
        "",
    ]
    for r in sorted(results, key=lambda x: -(x.get("final_score") or 0)):
        if "_error" in r:
            lines.append(f"## ⚠️ {r['_entry']['company']} — {r['_entry']['title']}")
            lines.append(f"FAILED: `{r['_error']}`")
            lines.append("")
            continue
        score = r.get("final_score", "?")
        verdict = r.get("verdict", "?")
        lines.append(f"## {r.get('company', '?')} — {r.get('title', '?')}  →  **{score}** ({verdict})")
        if r.get("posting_url"):
            lines.append(f"- URL: {r['posting_url']}")
        if r.get("noise_penalty_applied"):
            lines.append(f"- ⚠️ noise penalty applied: {r.get('noise_penalty_reason', '')}")
        if r.get("reason_short"):
            lines.append(f"- {r['reason_short']}")
        # asset_match is null (not missing) for roles scored < 7, so
        # `.get("asset_match", {})` would return None, not {}. Use `or {}` instead.
        if (r.get("asset_match") or {}).get("resume_choice"):
            lines.append(f"- Resume: `{r['asset_match']['resume_choice']}`")
        lines.append("")
    return "\n".join(lines)


def archive_processed(original_text: str, entries: list[dict]) -> None:
    """Append processed entries to the archive and clear MANUAL_JDS.md."""
    if not entries:
        return
    archive_block = [f"\n\n## Archived run — {datetime.now().strftime('%Y-%m-%d %H:%M')}"]
    for e in entries:
        archive_block.append(f"- {e['company']} — {e['title']} ({e['url'] or 'no url'})")

    if PROCESSED_FILE.exists():
        existing = PROCESSED_FILE.read_text()
    else:
        existing = "# Processed JDs (archive)\n\nEntries scored in past runs of `score_jobs.py`.\n"
    PROCESSED_FILE.write_text(existing + "\n".join(archive_block))

    # Reset MANUAL_JDS.md to a clean template (preserves header + instructions).
    # Detect missing/duplicate markers and surface loudly — silent no-op here
    # would re-score the same JDs at full token cost on the next run, and
    # silent reset under duplicate markers could discard user-pasted content.
    parts = INPUT_FILE.read_text().split("<!-- ENTRIES BELOW -->")
    if len(parts) == 2:
        INPUT_FILE.write_text(parts[0] + "<!-- ENTRIES BELOW -->\n")
    elif len(parts) == 1:
        print(
            f"⚠️  '<!-- ENTRIES BELOW -->' marker not found in {INPUT_FILE.name}. "
            f"File NOT reset — the same JD entries will be re-scored on the "
            f"next run (at full token cost). Manually clear processed entries "
            f"OR re-add the marker line below the [TEMPLATE] block."
        )
    else:
        print(
            f"⚠️  Found {len(parts) - 1} '<!-- ENTRIES BELOW -->' markers in "
            f"{INPUT_FILE.name} (expected exactly 1). File NOT reset to avoid "
            f"silent data loss. Remove duplicate markers and re-run."
        )


def main() -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Missing ANTHROPIC_API_KEY. Did you save it in .env?")

    if not INPUT_FILE.exists():
        sys.exit(f"No {INPUT_FILE.name} found at project root.")

    raw = INPUT_FILE.read_text()
    entries = parse_manual_jds(raw)
    if not entries:
        print(f"No JD entries found in {INPUT_FILE.name}. Add some and run again.")
        return

    print(f"Found {len(entries)} JD(s) to score.\n")

    # 120s per-request timeout: without this, a TCP socket that goes dead
    # without a FIN packet can leave the SDK waiting forever (observed
    # 2026-05-08: 11+ hour hang on first call against the 50-JD queue).
    client = anthropic.Anthropic(timeout=120.0)
    system_prompt = load_system_prompt()
    OUTPUT_DIR.mkdir(exist_ok=True)

    results = []
    for i, entry in enumerate(entries, 1):
        print(f"[{i}/{len(entries)}] {entry['company']} — {entry['title']}")
        try:
            parsed, usage = score_one(client, system_prompt, entry)
            parsed["_meta"] = {
                "scored_at": datetime.now().isoformat(timespec="seconds"),
                "model": MODEL,
                "effort": EFFORT,
                "source": entry.get("source", "manual"),
                "usage": usage,
            }
            results.append(parsed)
            score = parsed.get("final_score", "?")
            verdict = parsed.get("verdict", "?")
            cache_hit = usage["cache_read_input_tokens"]
            print(f"   → score: {score} ({verdict})    [cache_read: {cache_hit:,} tokens]")
        except anthropic.APIError as e:
            # Fail loud on any Anthropic API error (insufficient credit, bad key,
            # rate limit after SDK retries, 5xx). Every subsequent call would hit
            # the same error, so continuing burns Apify $ on a doomed pipeline
            # AND leaves the GitHub Actions workflow showing green when it
            # shouldn't. Persist whatever partial results we have so the run
            # artifact still has debug context, then exit non-zero.
            OUTPUT_DIR.mkdir(exist_ok=True)
            if results:
                RESULTS_JSON.write_text(json.dumps(results, indent=2, default=str))
                DIGEST_MD.write_text(build_digest(results))
            sys.exit(
                f"\n❌ Anthropic API error on entry [{i}/{len(entries)}] "
                f"({entry['company']} — {entry['title']}): {e}\n"
                f"\nStopped the run to avoid burning more Apify $ on a doomed "
                f"pipeline. Common fixes:\n"
                f"  • Insufficient credit → top up at https://console.anthropic.com/settings/billing\n"
                f"  • Bad API key → check ANTHROPIC_API_KEY (.env locally, secret in GitHub Actions)\n"
                f"  • Persistent rate limit → wait a few minutes and re-trigger\n"
                f"  • Anthropic outage → check https://status.anthropic.com/\n"
            )
        except Exception as e:
            # Non-API errors (JSON parse, unexpected response shape) — log and
            # continue with the next role.
            print(f"   ✗ FAILED: {e}")
            results.append({"_error": str(e), "_entry": entry})

    RESULTS_JSON.write_text(json.dumps(results, indent=2, default=str))
    DIGEST_MD.write_text(build_digest(results))
    archive_processed(raw, [e for r, e in zip(results, entries) if "_error" not in r])

    print(f"\nWrote: {RESULTS_JSON.relative_to(PROJECT_ROOT)}")
    print(f"Wrote: {DIGEST_MD.relative_to(PROJECT_ROOT)}")
    print(f"Archived processed entries to: {PROCESSED_FILE.name}")

    # Phase C: append rows to the Google Sheet (Decision 3 — keep both JSON + Sheet).
    # Failure here doesn't fail the run — the JSON write above is still authoritative.
    try:
        import sheets  # local-package import (sys.path was set in run_scrapers; here we add it inline)
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import sheets  # type: ignore
    try:
        n_written = sheets.write_results(results)
        print(f"Appended {n_written} row(s) to Google Sheet.")
    except Exception as e:
        print(f"⚠️ Sheet write failed (non-fatal — JSON results above are still good): {e}")


if __name__ == "__main__":
    main()
