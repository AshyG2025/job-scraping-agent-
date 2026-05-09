"""
What this file does — fetches jobs from LinkedIn via the Apify actor
`curious_coder/linkedin-jobs-scraper`. This is the **discovery** channel:
companies aren't in COMPANY_LIST.md, so Phase C's tier lookup falls back to
"discovery" automatically (no Sheet changes needed).

Two functions matching the same contract as ashby.py / greenhouse.py:

- fetch_listing(src): runs the Apify actor synchronously with src["search_url"]
  + src["max_results"]. Apify returns `descriptionHtml` inlined per item, so we
  cache it on `_jd_html_cached` (same Ashby trick). No second round-trip.
- fetch_jd_body(src, job): returns the cached HTML.

Per-source config (in run_scrapers.py SOURCES list):
  - company: display label for the funnel summary, e.g. "LinkedIn — Seattle"
  - ats: "linkedin_apify"
  - search_url: a LinkedIn /jobs/search URL built in **incognito Chrome**
                (logged-in URLs carry session params and return 0 results)
  - max_results: per-search result cap. Apify charges $0.001 per result.

Required env var: APIFY_API_TOKEN — loaded by run_scrapers.py via python-dotenv
at the top of that file. Get the token at console.apify.com/account/integrations.

Cost: $0.001 per result. 3 SOURCES × 67 results × 2x/week × 4 weeks ≈ $1.60/mo.

Note: Apify runs the actor synchronously, taking 1–3 minutes per source.
That's noticeably slower than the HTTP-based ATS scrapers, but it's the
tradeoff for getting LinkedIn coverage.
"""

import os

from apify_client import ApifyClient

APIFY_ACTOR = "curious_coder/linkedin-jobs-scraper"
DEFAULT_MAX_RESULTS = 67


def _client() -> ApifyClient:
    token = os.environ.get("APIFY_API_TOKEN")
    if not token:
        raise RuntimeError(
            "APIFY_API_TOKEN not set — add it to .env (see TABLE_OF_CONTENTS.md "
            "for the linkedin_apify section)."
        )
    return ApifyClient(token=token)


def fetch_listing(src: dict) -> list[dict]:
    """Runs the Apify actor for src["search_url"] and returns normalized jobs.

    Each item:
        {company, title, url, location, posted_at, id, source_ats,
         _jd_html_cached}
    """
    max_results = src.get("max_results", DEFAULT_MAX_RESULTS)
    client = _client()
    run = client.actor(APIFY_ACTOR).call(
        run_input={
            "urls": [src["search_url"]],
            "count": max_results,
        }
    )
    if not run or not run.get("defaultDatasetId"):
        return []

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    listing = []
    for item in items:
        listing.append({
            "company": (item.get("companyName") or "").strip(),
            "title": (item.get("title") or "").strip(),
            "url": item.get("link") or "",
            "location": item.get("location") or "",
            "posted_at": item.get("postedAt") or "",
            "id": str(item.get("id") or ""),
            "source_ats": "linkedin_apify",
            "_jd_html_cached": item.get("descriptionHtml") or item.get("descriptionText") or "",
        })
    return listing


def fetch_jd_body(src: dict, job: dict) -> str:
    """Returns the JD body cached during fetch_listing.

    Apify inlines descriptionHtml on each listing item, so we don't need a
    second call — same pattern as ashby.py.
    """
    return job.get("_jd_html_cached", "")
