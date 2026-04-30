"""
What this file does — fetches jobs from a SmartRecruiters-hosted careers page
using the public no-auth API at api.smartrecruiters.com. Same shape as
greenhouse.py but with two adjustments:

(1) The list endpoint paginates (max 100 per page), so we loop through pages.
(2) The detail endpoint returns the JD as a structured `sections` dict that
    we concatenate (with section titles as <h3>) into a single HTML body.

Used for Wise in Phase B. Many other employers use SmartRecruiters too.

API docs: https://dev.smartrecruiters.com/customer-api/posting-api/
"""

import requests

from .common import REQUEST_TIMEOUT_SEC, USER_AGENT

API_BASE = "https://api.smartrecruiters.com/v1/companies"
PAGE_SIZE = 100   # API max per their docs


def fetch_listing(company_slug: str, company_name: str) -> list[dict]:
    """Returns all open jobs for the given SmartRecruiters company, paginated.

    Each item:
        {company, title, url, location, posted_at (ISO 8601), id, source_ats}
    """
    listing = []
    offset = 0
    while True:
        response = requests.get(
            f"{API_BASE}/{company_slug}/postings",
            headers={"User-Agent": USER_AGENT},
            params={"limit": PAGE_SIZE, "offset": offset},
            timeout=REQUEST_TIMEOUT_SEC,
        )
        response.raise_for_status()
        payload = response.json()
        page = payload.get("content", []) or []
        if not page:
            break
        for posting in page:
            location = posting.get("location") or {}
            location_str = location.get("fullLocation") or (
                f"{location.get('city', '')}, {location.get('country', '').upper()}"
            ).strip(", ")
            listing.append({
                "company": company_name,
                "title": posting.get("name", ""),
                "url": f"https://jobs.smartrecruiters.com/{company_slug}/{posting['id']}",
                "location": location_str,
                "posted_at": posting.get("releasedDate", ""),
                "id": posting["id"],
                "source_ats": "smartrecruiters",
            })
        offset += PAGE_SIZE
        total = payload.get("totalFound", 0)
        if offset >= total:
            break
    return listing


def fetch_jd_body(company_slug: str, job: dict) -> str:
    """Returns the full JD body for a single job by concatenating its sections."""
    response = requests.get(
        f"{API_BASE}/{company_slug}/postings/{job['id']}",
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT_SEC,
    )
    response.raise_for_status()
    payload = response.json()
    sections = (payload.get("jobAd") or {}).get("sections") or {}
    body_parts = []
    for key in ("companyDescription", "jobDescription", "qualifications", "additionalInformation"):
        section = sections.get(key) or {}
        text = section.get("text", "")
        if not text:
            continue
        title = section.get("title", "")
        if title:
            body_parts.append(f"<h3>{title}</h3>")
        body_parts.append(text)
    return "\n".join(body_parts)
