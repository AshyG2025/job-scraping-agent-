"""
What this file does — shared helpers used by all per-ATS scrapers in Phase B.

- Applies the title / geo / age filters from HARD_FILTERS.md (mirrored in the
  TUNABLE PARAMETERS block below — when you change one, update HARD_FILTERS.md
  too, and vice versa).
- Lightly cleans up HTML JD bodies into plain text the LLM can read.
- Formats survivors into MANUAL_JDS.md entry blocks that score_jobs.py reads.
- Maintains a local-only dedup cache so the same role isn't surfaced on every run.

This file does NOT make any HTTP calls — that's the job of the per-ATS modules
(greenhouse.py, smartrecruiters.py).
"""

import json
import re
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

# ============================================================
# === TUNABLE PARAMETERS (mirror of HARD_FILTERS.md) ==========
# ============================================================
# Source-of-truth for these rules: HARD_FILTERS.md.
# When you edit one of those rules, mirror the change here so the code agrees
# with the spec.

# Title KEEP — at least one of these regex patterns must match the title for
# the job to survive the title gate (Option A from Phase B planning: permissive,
# matches HARD_FILTERS.md as written).
TITLE_KEEP_PATTERNS = [
    r"\bSenior\s+Product\s+Manager\b",
    r"\bSr\.?\s*Product\s+Manager\b",
    r"\bStaff\s+Product\s+Manager\b",
    r"\bSr\.?\s*Staff\s+Product\s+Manager\b",
    r"\bPrincipal\s+Product\s+Manager\b",
    r"\bGroup\s+Product\s+Manager\b",   # borderline — kept; LLM judges
    r"\bProduct\s+Lead\b",              # borderline — kept; LLM judges
]

# Title DROP — any match here = drop, even if title also matches a KEEP pattern.
# Catches managerial / wrong-level / leadership-implying titles.
TITLE_DROP_PATTERNS = [
    r"\bDirector\b",
    r"\bVP\b", r"\bVice\s+President\b",
    r"\bHead\s+of\b",
    r"\bManager\s+of\s+Product\b",
    r"\bManager,?\s*Product\b",
    r"\bEngineering\s+Manager\b",
    r"\bDesign\s+Manager\b",
    r"\bChief\s+Product\s+Officer\b",
    r"\bCPO\b",
    r"\bManager\s+of\s+PMs\b",
    r"\bProduct\s+Manager\s*I+\b",         # PM I, PM II, PM III
    r"\bAssociate\s+Product\s+Manager\b",
    r"\bAPM\b",
    r"\bJunior\s+Product\s+Manager\b",
]

# Geo KEEP — at least one of these regex patterns must match the location.
GEO_KEEP_PATTERNS = [
    r"\bSeattle\b", r"\bBellevue\b", r"\bRedmond\b",
    r"\bSan\s+Francisco\b", r"\bSF\b", r"\bBay\s+Area\b",
    r"\bPalo\s+Alto\b", r"\bMountain\s+View\b", r"\bMenlo\s+Park\b",
    r"\bSunnyvale\b", r"\bSan\s+Jose\b", r"\bOakland\b", r"\bBerkeley\b",
    r"\bLondon\b", r"\bGreater\s+London\b",
    r"Remote.*\bUS\b", r"Remote.*\bUK\b",
]

# Posting freshness — calendar days since first publication.
MAX_POSTING_AGE_DAYS = 30      # > this = drop
FLAG_POSTING_AGE_DAYS = 14     # 14 < age <= 30 = "older — apply soon"

# HTTP politeness
REQUEST_TIMEOUT_SEC = 15
USER_AGENT = "job-scraping-agent (Ayesha Ghoshal personal project)"

# Dedup cache location — gitignored (parent _local/ is in .gitignore).
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SEEN_CACHE_PATH = PROJECT_ROOT / "_local" / "scraped_seen.json"


# ============================================================
# === FILTER HELPERS =========================================
# ============================================================

def passes_title_filter(title: str) -> bool:
    """True iff title matches a KEEP pattern AND no DROP pattern."""
    if not title:
        return False
    if any(re.search(p, title, re.IGNORECASE) for p in TITLE_DROP_PATTERNS):
        return False
    return any(re.search(p, title, re.IGNORECASE) for p in TITLE_KEEP_PATTERNS)


def passes_geo_filter(location: str) -> bool:
    """True iff location matches at least one KEEP pattern."""
    if not location:
        return False
    return any(re.search(p, location, re.IGNORECASE) for p in GEO_KEEP_PATTERNS)


def compute_posting_age_days(posted_at_iso: str) -> int:
    """Returns calendar days since posting. -1 if input is unparseable."""
    if not posted_at_iso:
        return -1
    try:
        s = posted_at_iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days
    except (ValueError, TypeError):
        return -1


def passes_age_filter(age_days: int) -> bool:
    """True iff age is unknown OR within MAX_POSTING_AGE_DAYS."""
    if age_days < 0:
        return True   # unknown — let LLM judge from JD body
    return age_days <= MAX_POSTING_AGE_DAYS


def is_age_flagged(age_days: int) -> bool:
    """True iff age is in the 'older — apply soon' band (14 < age <= 30)."""
    return FLAG_POSTING_AGE_DAYS < age_days <= MAX_POSTING_AGE_DAYS


# ============================================================
# === HTML → PLAIN-TEXT (light cleanup for the LLM) ==========
# ============================================================

def html_to_text(s: str) -> str:
    """Strip HTML tags + decode entities. Best-effort, not bulletproof —
    the LLM tolerates leftover noise fine.

    Order matters: unescape() FIRST, then strip tags. Some ATS APIs
    (Greenhouse) return content with entities pre-encoded (`&lt;h2&gt;` rather
    than `<h2>`), so the regex strip wouldn't catch them if entity-decoding
    happened last.
    """
    if not s:
        return ""
    s = unescape(unescape(s))                           # twice handles double-encoded entities (Greenhouse does this)
    s = re.sub(r"<\s*br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</\s*(p|li|h[1-6]|div)\s*>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<\s*li\s*>", "• ", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# ============================================================
# === MANUAL_JDS.md FORMATTING ===============================
# ============================================================

def format_manual_jds_entry(job: dict, age_days: int) -> str:
    """Format a normalized job dict as a MANUAL_JDS.md entry block."""
    posted_clause = f"{age_days} days ago" if age_days >= 0 else "unknown"
    if is_age_flagged(age_days):
        posted_clause += " (older — apply soon)"
    return (
        f"\n## {job['company']} — {job['title']}\n"
        f"**URL:** {job['url']}\n"
        f"**Posted:** {posted_clause}\n"
        f"**Source:** {job.get('source_ats', 'unknown')} (auto-scraped)\n"
        f"\n---\n{html_to_text(job.get('jd_html', ''))}\n---\n"
    )


# ============================================================
# === DEDUP CACHE ============================================
# ============================================================

def load_seen() -> dict:
    """Returns dict of {url: first_seen_iso}. Empty dict on first run."""
    if not SEEN_CACHE_PATH.exists():
        return {}
    try:
        with open(SEEN_CACHE_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_seen(seen: dict) -> None:
    """Writes the seen-cache back to disk, creating parent dir if needed."""
    SEEN_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SEEN_CACHE_PATH, "w") as f:
        json.dump(seen, f, indent=2, sort_keys=True)


def is_seen(seen: dict, url: str) -> bool:
    return url in seen


def mark_seen(seen: dict, url: str) -> None:
    seen[url] = datetime.now(timezone.utc).isoformat()
