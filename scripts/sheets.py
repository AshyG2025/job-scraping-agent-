"""
sheets.py — Phase C Google Sheets writer.

What this file does, in plain English:
  1. Connects to your "Job Scraping Outcomes" Google Sheet using the service-
     account credentials from .env (set up via docs/PHASE_C_SETUP.md).
  2. Ensures the header row matches the locked 31-column layout (groups A → B
     → D → C, in the user-confirmed order).
  3. Appends one row per newly scored role with `scored_date`, `source`, and
     `tier` filled in alongside the LLM scoring fields.
  4. Pre-fills two Sheet formulas on each row:
       - score_at_application      = IF(applied="Yes", final_score, "")
       - prompt_version_at_application = IF(applied="Yes", prompt_version, "")
     so when you mark `applied = Yes`, the score + prompt version frozen at
     application time appear automatically (no Apps Script needed).
  5. Re-sorts the data range by `scored_date` DESC then `final_score` DESC,
     so the newest run lands at the top with its best role at row 2. Sort is
     done server-side via the Sheets API, which preserves formulas.

Called from score_jobs.py after the existing JSON write (Decision 3: keep both).
Reads two values from .env:
    GOOGLE_SHEETS_KEY_PATH — path to the service account JSON key
    GOOGLE_SHEET_ID        — the Sheet ID copied from the URL during setup

Tier lookup reads COMPANY_LIST.md and matches the scored role's company name
against the bullets under each Tier N section. Unmatched companies fall back
to `discovery` (if the LLM flagged it) or `unknown`.
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Lazy imports of gspread/google-auth happen inside write_results() so this
# module can still be imported (e.g., for unit checks) when the deps aren't
# installed yet.

PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMPANY_LIST_PATH = PROJECT_ROOT / "COMPANY_LIST.md"

# === Locked column order (groups A → B → D → C, per user-confirmed Phase C decision) ===
COLUMN_NAMES: list[str] = [
    # A. Identity (9)
    "scored_date",
    "company",
    "title",
    "location",
    "posting_url",
    "posting_age_days",
    "applicants_count",
    "source",
    "tier",
    # B. Scoring (8)
    "final_score",
    "score_domain",
    "score_skills",
    "score_level",
    "score_team_needs",
    "verdict",
    "reason_short",
    "resume_choice",
    # D. Outcomes (9 — manually filled, except the two _at_application formulas)
    "applied",
    "applied_date",
    "score_at_application",
    "prompt_version_at_application",
    "outcome_status",
    "outcome_date",
    "outcome_notes",
    "score_in_hindsight",
    "add_to_eval_set",
    # C. Flags / pointers (5)
    "h1b_status",
    "discovery_flag",
    "verify_flags",
    "prompt_version",
    "qc_deep_dive_url",
]

# Pre-computed column letters used in the auto-copy formulas. If you change
# COLUMN_NAMES above, regenerate these by running _col_letter on the names.
COL_APPLIED = "R"          # 18th column
COL_FINAL_SCORE = "J"      # 10th column
COL_PROMPT_VERSION = "AD"  # 30th column


# ============================================================
# === COLUMN-LETTER HELPERS ==================================
# ============================================================

def _col_letter(col_idx_1based: int) -> str:
    """Convert a 1-based column index to a Sheets column letter (1=A, 27=AA)."""
    letters = ""
    n = col_idx_1based
    while n > 0:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


# ============================================================
# === TIER LOOKUP (reads COMPANY_LIST.md) ====================
# ============================================================

def _parse_company_tiers(text: str) -> dict[str, str]:
    """
    Parse COMPANY_LIST.md and return {company_name_lowercased: tier_label}.

    Handles:
      - "**Stripe**"               → exact name
      - "**Stripe London**"        → matched via prefix-lookup (in lookup_tier)
      - "**Square (Block)**"       → adds aliases for both 'Square' and 'Block'
      - "**Bill.com**", "**Snorkel.AI**" → exact match (dots / case preserved
                                          on parse, normalized on lookup)
    Sections we DON'T add to the map: Skip / Discovery / Referral / Companies
    to research (those don't represent named-co tier targets).
    """
    tiers: dict[str, str] = {}
    current_tier: Optional[str] = None

    for line in text.splitlines():
        m = re.match(r"^##\s+Tier\s+(\d+)", line)
        if m:
            current_tier = m.group(1)
            continue
        # Any other ## heading resets us out of a tier section
        if re.match(r"^##\s+", line):
            current_tier = None
            continue
        if current_tier is None:
            continue
        # `- **Company Name** — ...`
        m = re.match(r"^-\s+\*\*([^*]+)\*\*", line)
        if not m:
            continue
        raw_name = m.group(1).strip()
        tiers[raw_name.lower()] = current_tier
        # If "Foo (Bar)" pattern, register both as aliases for the same tier
        parens = re.match(r"^([^(]+?)\s*\(([^)]+)\)\s*$", raw_name)
        if parens:
            tiers[parens.group(1).strip().lower()] = current_tier
            tiers[parens.group(2).strip().lower()] = current_tier

    return tiers


def lookup_tier(company_name: str, tier_map: dict[str, str], discovery_flag: bool = False) -> str:
    """
    Return the tier label ('1' / '2' / '3' / 'discovery' / 'unknown') for a
    company. Tries exact match first, then prefix match (e.g., "Stripe" matches
    "Stripe London"), preferring the lowest-numbered tier on conflicts.
    """
    if not company_name:
        return "discovery" if discovery_flag else "unknown"

    name_lower = company_name.strip().lower()
    if name_lower in tier_map:
        return tier_map[name_lower]

    best_tier: Optional[str] = None
    for raw_lower, tier in tier_map.items():
        if raw_lower.startswith(name_lower + " ") or raw_lower.startswith(name_lower + ","):
            if best_tier is None or tier < best_tier:
                best_tier = tier

    if best_tier is not None:
        return best_tier
    return "discovery" if discovery_flag else "unknown"


def load_tier_map() -> dict[str, str]:
    """Reads COMPANY_LIST.md once and returns the tier map. Cached at call site."""
    if not COMPANY_LIST_PATH.exists():
        return {}
    return _parse_company_tiers(COMPANY_LIST_PATH.read_text())


# ============================================================
# === ROW BUILDER ============================================
# ============================================================

def _format_list(value) -> str:
    """Flatten a list of strings into a comma-separated cell value, or pass through."""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return value if value is not None else ""


def build_row(result: dict, source: str, tier: str, row_num: int) -> list:
    """
    Convert one scored result (one item from scored_results.json) into a 31-element
    row, in the locked column order.

    `row_num` is the absolute Sheet row this entry will land on — used to embed
    self-referential formulas in the score_at_application + prompt_version_at_application
    columns. Sheets API SortRange updates these references when sort moves rows,
    so the formulas stay correct after sorting.
    """
    scores = result.get("scores") or {}
    asset_match = result.get("asset_match") or {}

    # Self-referential formulas (column letters from the locked layout)
    score_at_app = f'=IF({COL_APPLIED}{row_num}="Yes",{COL_FINAL_SCORE}{row_num},"")'
    pv_at_app = f'=IF({COL_APPLIED}{row_num}="Yes",{COL_PROMPT_VERSION}{row_num},"")'

    # qc_deep_dive_url points to the JSON file in _local/ (reachable when the
    # user is on the same machine; harmless string for portfolio readers).
    qc_deep_dive_url = "_local/scored_results.json"

    return [
        # --- A. Identity ---
        datetime.now().strftime("%Y-%m-%d"),     # scored_date (date only, per Phase C decision)
        result.get("company", ""),
        result.get("title", ""),
        result.get("location", ""),
        result.get("posting_url", ""),
        result.get("posting_age_days", ""),
        result.get("applicants_count", ""),
        source or "manual",
        tier,
        # --- B. Scoring ---
        result.get("final_score", ""),
        scores.get("domain", ""),
        scores.get("skills", ""),
        scores.get("level", ""),
        scores.get("team_needs", ""),
        result.get("verdict", ""),
        result.get("reason_short", ""),
        asset_match.get("resume_choice", ""),
        # --- D. Outcomes (manual; two formula cells; rest blank) ---
        "",                # applied
        "",                # applied_date
        score_at_app,      # score_at_application (formula)
        pv_at_app,         # prompt_version_at_application (formula)
        "",                # outcome_status
        "",                # outcome_date
        "",                # outcome_notes
        "",                # score_in_hindsight
        "",                # add_to_eval_set
        # --- C. Flags / pointers ---
        result.get("h1b_status", ""),
        result.get("discovery_flag", False),
        _format_list(result.get("verify_flags", [])),
        result.get("prompt_version", ""),
        qc_deep_dive_url,
    ]


# ============================================================
# === SHEETS CLIENT ==========================================
# ============================================================

def _get_worksheet():
    """Authorize via service account and return the first worksheet of the configured Sheet."""
    import gspread
    from google.oauth2.service_account import Credentials

    key_path = os.environ.get("GOOGLE_SHEETS_KEY_PATH")
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")
    if not key_path or not sheet_id:
        raise RuntimeError(
            "Missing GOOGLE_SHEETS_KEY_PATH or GOOGLE_SHEET_ID in .env. "
            "See docs/PHASE_C_SETUP.md."
        )
    creds = Credentials.from_service_account_file(
        key_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).sheet1


def _ensure_header(worksheet) -> None:
    """Write the locked 31-col header row if row 1 doesn't already match."""
    existing = worksheet.row_values(1)
    if existing == COLUMN_NAMES:
        return
    # Either empty or wrong — overwrite row 1 to match the locked schema.
    last_col = _col_letter(len(COLUMN_NAMES))
    worksheet.update(f"A1:{last_col}1", [COLUMN_NAMES])


def _sort_data_rows(worksheet) -> None:
    """
    Re-sort the data range (rows 2 onwards) by scored_date DESC, final_score DESC.
    Server-side via Sheets API SortRange — preserves formulas, updates self-refs.
    """
    last_col = _col_letter(len(COLUMN_NAMES))
    # Big upper bound — empty cells sort to the bottom under DES order.
    sort_range = f"A2:{last_col}10000"
    # 1 = scored_date column; 10 = final_score column.
    worksheet.sort(
        (1, "des"),
        (10, "des"),
        range=sort_range,
    )


# ============================================================
# === PUBLIC ENTRY POINT =====================================
# ============================================================

def write_results(results: list[dict], source_lookup: Optional[dict[str, str]] = None) -> int:
    """
    Append one row per result to the Sheet, then re-sort.

    `source_lookup` maps result['company'] (or whatever key the caller chooses)
    to a source string ('greenhouse', 'manual', etc.). If a result is missing
    from the lookup, falls back to result['_meta']['source'] or 'manual'.

    Returns the number of rows written.
    """
    if not results:
        return 0

    # Filter out failed entries — they don't have the fields we need.
    successful = [r for r in results if "_error" not in r]
    if not successful:
        return 0

    worksheet = _get_worksheet()
    _ensure_header(worksheet)

    tier_map = load_tier_map()

    # Compute the row number each new entry will land on, so the formulas
    # we embed reference the right rows.
    existing_rows = len(worksheet.get_all_values())  # includes header
    start_row = existing_rows + 1

    rows = []
    for i, result in enumerate(successful):
        row_num = start_row + i
        company = result.get("company", "")
        source = (
            (source_lookup or {}).get(company)
            or (result.get("_meta") or {}).get("source")
            or "manual"
        )
        tier = lookup_tier(company, tier_map, discovery_flag=bool(result.get("discovery_flag")))
        rows.append(build_row(result, source, tier, row_num))

    # USER_ENTERED so the formula strings are interpreted as formulas, not literals.
    worksheet.append_rows(rows, value_input_option="USER_ENTERED")
    _sort_data_rows(worksheet)
    return len(rows)


if __name__ == "__main__":
    # Convenience: `python scripts/sheets.py` runs the connection check.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from check_sheets import main as check_main  # type: ignore
    check_main()
