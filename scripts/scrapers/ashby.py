"""
What this file does — fetches jobs from an Ashby-hosted careers page using
the public no-auth posting API at api.ashbyhq.com.

Two functions matching the same contract as greenhouse.py / workday.py:

- fetch_listing(src): a single GET to /posting-api/job-board/{slug} returns
  ALL open jobs WITH descriptionHtml inlined in the listing payload — so
  unlike Greenhouse/Workday we don't need a second round-trip per job. We
  stash the JD HTML on each normalized dict under `_jd_html_cached` so
  fetch_jd_body() can return it without re-hitting the API.
- fetch_jd_body(src, job): returns the cached HTML from the listing dict.

Per-co config is just `slug` (same shape as Greenhouse).

Used for: Ramp, Deliveroo (Tier 1 in COMPANY_LIST.md).

API docs: https://developers.ashbyhq.com/reference/publicjobpostingapi
"""

import requests

from .common import REQUEST_TIMEOUT_SEC, USER_AGENT

API_BASE = "https://api.ashbyhq.com/posting-api/job-board"


def _combine_locations(job: dict) -> str:
    """Joins primary + secondary locations with `; ` so the geo regex sees
    every option a job is open to (e.g. London + Paris + Remote UK)."""
    parts = [job.get("location") or ""]
    for sec in job.get("secondaryLocations") or []:
        parts.append(sec.get("location") or "")
    return "; ".join(p for p in parts if p)


def fetch_listing(src: dict) -> list[dict]:
    """Returns all publicly-listed open jobs for the given Ashby board.

    Each item:
        {company, title, url, location, posted_at (ISO 8601), id, source_ats,
         _jd_html_cached}
    """
    response = requests.get(
        f"{API_BASE}/{src['slug']}",
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT_SEC,
    )
    response.raise_for_status()
    payload = response.json()
    listing = []
    for job in payload.get("jobs") or []:
        if not job.get("isListed", True):
            continue
        listing.append({
            "company": src["company"],
            "title": (job.get("title") or "").strip(),
            "url": job.get("jobUrl") or "",
            "location": _combine_locations(job),
            "posted_at": job.get("publishedAt") or "",
            "id": job.get("id") or "",
            "source_ats": "ashby",
            "_jd_html_cached": job.get("descriptionHtml") or "",
        })
    return listing


def fetch_jd_body(src: dict, job: dict) -> str:
    """Returns the JD body cached during fetch_listing.

    Ashby returns descriptionHtml inline in the listing endpoint, so we don't
    need a second HTTP call here — we just hand back the cached value to keep
    the same two-function contract as the other ATS modules.
    """
    return job.get("_jd_html_cached", "")
