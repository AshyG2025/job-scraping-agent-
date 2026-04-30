"""
What this file does — fetches jobs from a Greenhouse-hosted careers page using
the public no-auth API at boards-api.greenhouse.io. Two functions:

- fetch_listing(slug, company_name): returns all open jobs (no JD body) as
  normalized dicts that the orchestrator can filter.
- fetch_jd_body(slug, job): given a job dict from fetch_listing, returns the
  full JD body as HTML.

Used for Stripe in Phase B. Many companies use Greenhouse — adding a new one
is one line in run_scrapers.py.

API docs: https://developers.greenhouse.io/job-board.html
"""

import requests

from .common import REQUEST_TIMEOUT_SEC, USER_AGENT

API_BASE = "https://boards-api.greenhouse.io/v1/boards"


def fetch_listing(board_slug: str, company_name: str) -> list[dict]:
    """Returns all open jobs for the given Greenhouse board, without JD body.

    Each item:
        {company, title, url, location, posted_at (ISO 8601), id, source_ats}
    """
    response = requests.get(
        f"{API_BASE}/{board_slug}/jobs",
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT_SEC,
    )
    response.raise_for_status()
    payload = response.json()
    return [
        {
            "company": company_name,
            "title": job.get("title", ""),
            "url": job.get("absolute_url", ""),
            "location": (job.get("location") or {}).get("name", ""),
            "posted_at": job.get("first_published") or job.get("updated_at", ""),
            "id": job["id"],
            "source_ats": "greenhouse",
        }
        for job in payload.get("jobs", [])
    ]


def fetch_jd_body(board_slug: str, job: dict) -> str:
    """Returns the full JD body (HTML) for a single job from fetch_listing()."""
    response = requests.get(
        f"{API_BASE}/{board_slug}/jobs/{job['id']}",
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT_SEC,
    )
    response.raise_for_status()
    return response.json().get("content", "")
