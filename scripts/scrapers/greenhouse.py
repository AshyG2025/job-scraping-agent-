"""
What this file does — fetches jobs from a Greenhouse-hosted careers page using
the public no-auth API at boards-api.greenhouse.io. Two functions:

- fetch_listing(src): returns all open jobs (no JD body) as normalized dicts
  that the orchestrator can filter. `src` is the source-dict from SOURCES.
- fetch_jd_body(src, job): given a job dict from fetch_listing, returns the
  full JD body as HTML.

Used for many Tier 1 + Tier 2 companies in Phase B. Adding a new one is one
line in run_scrapers.py.

API docs: https://developers.greenhouse.io/job-board.html
"""

import requests

from .common import REQUEST_TIMEOUT_SEC, USER_AGENT

API_BASE = "https://boards-api.greenhouse.io/v1/boards"


def fetch_listing(src: dict) -> list[dict]:
    """Returns all open jobs for the given Greenhouse board, without JD body.

    Each item:
        {company, title, url, location, posted_at (ISO 8601), id, source_ats}
    """
    response = requests.get(
        f"{API_BASE}/{src['slug']}/jobs",
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT_SEC,
    )
    response.raise_for_status()
    payload = response.json()
    return [
        {
            "company": src["company"],
            "title": job.get("title", ""),
            "url": job.get("absolute_url", ""),
            "location": (job.get("location") or {}).get("name", ""),
            "posted_at": job.get("first_published") or job.get("updated_at", ""),
            "id": job["id"],
            "source_ats": "greenhouse",
        }
        for job in payload.get("jobs", [])
    ]


def fetch_jd_body(src: dict, job: dict) -> str:
    """Returns the full JD body (HTML) for a single job from fetch_listing()."""
    response = requests.get(
        f"{API_BASE}/{src['slug']}/jobs/{job['id']}",
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT_SEC,
    )
    response.raise_for_status()
    return response.json().get("content", "")
