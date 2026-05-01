"""
What this file does — fetches jobs from a Workday-hosted careers page using
the public CXS JSON endpoint (no auth needed).

Per-company config is a triple, not a single slug:
  - tenant — e.g. "zillow", "visa", "paypal" (the company's Workday account name)
  - host   — Workday cloud host: "wd1", "wd5", "wd12" etc. Different tenants
             live on different hosts; not predictable from the company name.
  - site   — the customer-facing site name on Workday: "Zillow_Group_External",
             "External_Career_Site", "Visa", etc.

Endpoints we hit (no auth):
  - POST {base}/jobs        body {"appliedFacets":{},"limit":N,"offset":N,"searchText":""}
                            → paginated job listings
  - GET  {base}{externalPath} → job detail with jobDescription HTML

  where {base} = https://{tenant}.{host}.myworkdayjobs.com/wday/cxs/{tenant}/{site}

Public-facing apply URL (what we put in the digest, not the CXS path):
  https://{tenant}.{host}.myworkdayjobs.com/{site}{externalPath}

Used for 9 companies in Phase B+: Visa, PayPal, Salesforce, Zillow (Tier 1) +
Target, Capital One, Walmart, Zoom (Tier 2) + Checkout.com (Tier 1, ex-SR).
"""

import re
from datetime import datetime, timedelta, timezone

import requests

# Workday's CXS endpoint 403s on "job-scraping-agent"-style User-Agents; a stock
# browser UA passes. Probe-tested against Zillow's tenant on 2026-05-01.
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# Workday caps page size at 20 (limit=50 returns HTTP 400). Big tenants like
# Walmart/Target/Salesforce have 1500+ jobs = 75+ pages per run; the default
# 15s timeout in common.py is too tight for that — using 30s here.
REQUEST_TIMEOUT_SEC = 30
PAGE_SIZE = 20

# Workday returns `postedOn` as human text ("Posted Today" / "Posted N Days Ago"
# / "Posted 30+ Days Ago"), so we convert to ISO before the age filter sees it.
_DAYS_AGO_RE = re.compile(r"posted\s+(\d+)\+?\s+days?\s+ago", re.IGNORECASE)


def _cxs_base(src: dict) -> str:
    return (
        f"https://{src['tenant']}.{src['host']}.myworkdayjobs.com"
        f"/wday/cxs/{src['tenant']}/{src['site']}"
    )


def _public_url(src: dict, external_path: str) -> str:
    return (
        f"https://{src['tenant']}.{src['host']}.myworkdayjobs.com"
        f"/{src['site']}{external_path}"
    )


def _parse_posted_on(s: str) -> str:
    """Convert Workday's human 'postedOn' to ISO 8601.

    "Posted Today" → today; "Posted Yesterday" → today−1; "Posted N Days Ago"
    → today−N; "Posted 30+ Days Ago" → today−31 (so it fails the 30-day max);
    anything else → "" (treated as unknown by the age filter).
    """
    if not s:
        return ""
    text = s.strip().lower()
    now = datetime.now(timezone.utc)
    if "today" in text:
        return now.isoformat()
    if "yesterday" in text:
        return (now - timedelta(days=1)).isoformat()
    if "30+" in text:
        return (now - timedelta(days=31)).isoformat()
    match = _DAYS_AGO_RE.search(text)
    if match:
        return (now - timedelta(days=int(match.group(1)))).isoformat()
    return ""


def fetch_listing(src: dict) -> list[dict]:
    """Returns all open jobs for the given Workday tenant/site, paginated."""
    base = _cxs_base(src)
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    listing = []
    offset = 0
    total = None  # Workday returns the real total ONLY on the first page;
                  # subsequent pages return total=0 even when more exist.
    while True:
        response = requests.post(
            f"{base}/jobs",
            headers=headers,
            json={
                "appliedFacets": {},
                "limit": PAGE_SIZE,
                "offset": offset,
                "searchText": "",
            },
            timeout=REQUEST_TIMEOUT_SEC,
        )
        response.raise_for_status()
        payload = response.json()
        if total is None:
            total = payload.get("total", 0)
        postings = payload.get("jobPostings", []) or []
        if not postings:
            break
        for posting in postings:
            external_path = posting.get("externalPath", "")
            listing.append({
                "company": src["company"],
                "title": posting.get("title", ""),
                "url": _public_url(src, external_path),
                "location": posting.get("locationsText", ""),
                "posted_at": _parse_posted_on(posting.get("postedOn", "")),
                "id": external_path,
                "source_ats": "workday",
            })
        offset += PAGE_SIZE
        if offset >= total:
            break
    return listing


def fetch_jd_body(src: dict, job: dict) -> str:
    """Returns the full JD body (HTML) for a single Workday job."""
    response = requests.get(
        f"{_cxs_base(src)}{job['id']}",
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        timeout=REQUEST_TIMEOUT_SEC,
    )
    response.raise_for_status()
    info = response.json().get("jobPostingInfo") or {}
    return info.get("jobDescription", "")
