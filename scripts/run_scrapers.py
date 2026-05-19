"""
What this file does — Phase B career-page scraper orchestrator.

For each entry in SOURCES below, it runs the matching ATS-specific scraper,
applies the title / geo / age filters from scrapers/common.py, dedupes against
_local/scraped_seen.json (so the same role isn't surfaced on every run), then
appends survivors to MANUAL_JDS.md as ready-to-score entries. After this
script finishes, run scripts/score_jobs.py as usual to score them.

Run:
    source .venv/bin/activate
    python scripts/run_scrapers.py

Adding a new company: append a dict to SOURCES below. If the company uses an
ATS that already has a scraper module (greenhouse, smartrecruiters), no new
code needed. New ATS = new module under scripts/scrapers/ + one line in
ATS_MODULES below.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env so per-module env vars (e.g. APIFY_API_TOKEN for linkedin_apify)
# are available before any scraper module runs.
load_dotenv()

# Make scripts/ importable as a package when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from scrapers import ashby, common, greenhouse, linkedin_apify, smartrecruiters, workday

# === SOURCES TO SCRAPE ===
# Slugs verified against each company's live ATS board on 2026-05-01.
SOURCES = [
    # ---- Greenhouse ----
    # Tier 1
    {"company": "Adyen",      "ats": "greenhouse", "slug": "adyen"},
    {"company": "Airbnb",     "ats": "greenhouse", "slug": "airbnb"},
    {"company": "Bill.com",   "ats": "greenhouse", "slug": "billcom"},
    {"company": "Boku",       "ats": "greenhouse", "slug": "boku"},
    {"company": "Brex",       "ats": "greenhouse", "slug": "brex"},
    {"company": "DoorDash",   "ats": "greenhouse", "slug": "doordashusa"},   # bare `doordash` 404s
    {"company": "Ebury",      "ats": "greenhouse", "slug": "ebury"},        # added 2026-05-12; London FX/payments fintech, ~240 jobs total (geo filter trims hard)
    {"company": "GoCardless", "ats": "greenhouse", "slug": "gocardless"},
    {"company": "Liberis",    "ats": "greenhouse", "slug": "liberis"},
    {"company": "Marqeta",    "ats": "greenhouse", "slug": "marqeta"},
    {"company": "Mercury",    "ats": "greenhouse", "slug": "mercury"},
    {"company": "Monzo",      "ats": "greenhouse", "slug": "monzo"},
    {"company": "Snorkel.AI", "ats": "greenhouse", "slug": "snorkelai"},   # added 2026-05-11; HM-callback Tier 1; slug confirmed via API + careers-page embed
    {"company": "Stripe",     "ats": "greenhouse", "slug": "stripe"},
    # Tier 2
    {"company": "Affirm",     "ats": "greenhouse", "slug": "affirm"},
    {"company": "Block",      "ats": "greenhouse", "slug": "block"},        # migrated off SmartRecruiters; ex-`Square` tenant is dormant
    # Coinbase: Greenhouse slug `coinbase` returned 404 starting 2026-05-08 (slug retired).
    # Re-recon 2026-05-11 found no working endpoint on Greenhouse / Lever / Ashby / SmartRecruiters.
    # Workday tenants (`coinbase` wd1/wd5, `coinbasecorp` wd1, `coinbase` wd103) all return cryptic 422s
    # — endpoint exists but `site` value unknown without inside knowledge. jobs.coinbase.com is
    # Cloudflare-blocked (403 even with browser headers). Fallback: LinkedIn Apify discovery channel
    # surfaces Coinbase roles; that's the active path until we get the right Workday `site` value.
    {"company": "Databricks", "ats": "greenhouse", "slug": "databricks"},
    {"company": "Modulr",     "ats": "greenhouse", "slug": "modulrfinance"},  # company is "Modulr"; legal name "Modulr Finance"
    {"company": "Tide",       "ats": "greenhouse", "slug": "tide"},

    # ---- SmartRecruiters (slugs are case-sensitive) ----
    # Tier 1
    {"company": "ServiceNow",   "ats": "smartrecruiters", "slug": "ServiceNow"},
    {"company": "Wise",         "ats": "smartrecruiters", "slug": "wise"},

    # ---- Workday (per-co config is tenant + host + site, not slug) ----
    # Tier 1
    {"company": "PayPal",       "ats": "workday", "tenant": "paypal",     "host": "wd1",  "site": "jobs"},
    {"company": "Salesforce",   "ats": "workday", "tenant": "salesforce", "host": "wd12", "site": "External_Career_Site"},
    {"company": "Visa",         "ats": "workday", "tenant": "visa",       "host": "wd5",  "site": "Visa"},
    {"company": "Zillow",       "ats": "workday", "tenant": "zillow",     "host": "wd5",  "site": "Zillow_Group_External"},
    # Tier 2
    {"company": "Capital One",  "ats": "workday", "tenant": "capitalone", "host": "wd12", "site": "Capital_One"},
    {"company": "Target",       "ats": "workday", "tenant": "target",     "host": "wd5",  "site": "targetcareers"},
    {"company": "Walmart",      "ats": "workday", "tenant": "walmart",    "host": "wd5",  "site": "WalmartExternal"},
    {"company": "Zoom",         "ats": "workday", "tenant": "zoom",       "host": "wd5",  "site": "Zoom"},

    # ---- Ashby ----
    # Tier 1
    {"company": "Deliveroo",    "ats": "ashby", "slug": "deliveroo"},     # migrated off Greenhouse 2026-05-01
    {"company": "Ramp",         "ats": "ashby", "slug": "ramp"},
    # Tier 2
    {"company": "Multiverse",   "ats": "ashby", "slug": "multiverse"},    # added 2026-05-12; UK apprenticeship platform, ~38 jobs

    # ---- LinkedIn (Apify) — DISCOVERY channel ----
    # Each entry = one LinkedIn /jobs/search URL built in incognito Chrome
    # (logged-in URLs return 0 results). max_results capped per-source so total
    # cost stays at ~$0.20/run ($1/1000 results × 200 results = ~$1.60/mo at 2x/wk).
    # Companies aren't tied to COMPANY_LIST.md tiers — the Sheet shows tier="discovery".
    #
    # Seattle + SF Bay paused 2026-05-19 alongside the London-only geo guardrail
    # in scripts/scrapers/common.py — leaving them active would burn ~$0.14/run
    # of Apify time scraping roles that all get dropped by the geo filter
    # downstream. To re-enable, uncomment the two entries below.
    # {
    #     "company": "LinkedIn — Seattle",
    #     "ats": "linkedin_apify",
    #     "search_url": "https://www.linkedin.com/jobs/search/?keywords=Product%20Manager&location=Seattle%2C%20Washington%2C%20United%20States&f_TPR=r2592000&f_E=4&f_JT=F&sortBy=DD",
    #     "max_results": 67,
    # },
    # {
    #     "company": "LinkedIn — SF Bay",
    #     "ats": "linkedin_apify",
    #     "search_url": "https://www.linkedin.com/jobs/search/?keywords=Product%20Manager&location=San%20Francisco%20Bay%20Area&f_TPR=r2592000&f_E=4&f_JT=F&sortBy=DD",
    #     "max_results": 67,
    # },
    {
        "company": "LinkedIn — London",
        "ats": "linkedin_apify",
        "search_url": "https://www.linkedin.com/jobs/search/?keywords=Product%20Manager&location=London%2C%20England%2C%20United%20Kingdom&f_TPR=r2592000&f_E=4&f_JT=F&sortBy=DD",
        "max_results": 67,
    },

]

# Note on Checkout.com: re-probed 2026-05-11 with the proper Workday CXS payload
# (`appliedFacets`/`searchText`). Results: `checkout` wd1/wd5/wd103 all return cryptic 422
# (endpoint exists but the `site` value is unknown — tried CheckoutCareers / External /
# CheckoutCom / Careers / Checkout, all 422); `checkout` wd3 returns 403 (auth-gated);
# `careers.checkout.com` connection-failed (HTTP 000); no working endpoint found on
# Greenhouse / Lever / Ashby / SmartRecruiters. Like Coinbase, this is a dead-end via blind
# probing — needs inside knowledge of the Workday `site` value, or LinkedIn Apify discovery
# (which already covers London) as the fallback. Re-probe at next monthly QC.
#
# Note on American Express: probed 2026-05-12 against Greenhouse / Lever / Ashby /
# SmartRecruiters (all 404 or empty placeholder) and Workday tenants `americanexpress` +
# `amex` × wd1/wd5/wd103/wd3 × 5 candidate `site` values (External / Careers /
# AmexCareers / AmericanExpress / americanexpress) — all return cryptic 422
# (endpoint exists but `site` value unknown without inside knowledge). The careers
# page at careers.americanexpress.com (HTTP 200) is JS-rendered and reveals no
# Workday URL in HTML. Same dead-end pattern as Coinbase / Checkout.com. Fallback:
# Apify LinkedIn discovery — Amex has SF Bay + London tech offices, so SF Bay and
# London search channels will surface their roles. (NYC is not in our LinkedIn
# search set; if NYC becomes geo-relevant, add a 4th LinkedIn search.) Re-probe
# at next monthly QC; Workday `site` values do occasionally surface in HR-tech blogs.

ATS_MODULES = {
    "greenhouse": greenhouse,
    "smartrecruiters": smartrecruiters,
    "workday": workday,
    "ashby": ashby,
    "linkedin_apify": linkedin_apify,
}

MANUAL_JDS_PATH = Path(__file__).resolve().parents[1] / "MANUAL_JDS.md"


def main():
    seen = common.load_seen()
    new_entries = []
    summary_lines = []

    for src in SOURCES:
        try:
            module = ATS_MODULES[src["ats"]]
            listing = module.fetch_listing(src)
        except Exception as e:
            summary_lines.append(
                f"❌ {src['company']} ({src['ats']}): fetch_listing failed — {e}"
            )
            continue

        total = len(listing)
        title_pass = [j for j in listing if common.passes_title_filter(j["title"])]
        geo_pass = [j for j in title_pass if common.passes_geo_filter(j["location"])]
        for j in geo_pass:
            j["_age_days"] = common.compute_posting_age_days(j["posted_at"])
        age_pass = [j for j in geo_pass if common.passes_age_filter(j["_age_days"])]
        unseen = [j for j in age_pass if not common.is_seen(seen, j["url"])]

        # Fetch JD body only for jobs that survived all filters AND are new.
        for job in unseen:
            try:
                job["jd_html"] = module.fetch_jd_body(src, job)
                common.mark_seen(seen, job["url"])
                new_entries.append(common.format_manual_jds_entry(job, job["_age_days"]))
            except Exception as e:
                summary_lines.append(
                    f"   ⚠️ {src['company']}: failed to fetch JD body for "
                    f"{job['title']!r} — {e}"
                )

        summary_lines.append(
            f"✅ {src['company']} ({src['ats']}): {total} total → "
            f"{len(title_pass)} pass title → {len(geo_pass)} pass geo → "
            f"{len(age_pass)} pass age → {len(unseen)} new "
            f"({len(age_pass) - len(unseen)} already seen)"
        )

    if new_entries:
        with open(MANUAL_JDS_PATH, "a") as f:
            f.write(
                "\n<!-- Added by run_scrapers.py — review/edit before running "
                "score_jobs.py -->\n"
            )
            f.write("".join(new_entries))

    common.save_seen(seen)

    print()
    print("=" * 60)
    print("Phase B scraper run summary")
    print("=" * 60)
    for line in summary_lines:
        print(line)
    print()
    if new_entries:
        print(f"📝 {len(new_entries)} new JD(s) appended to MANUAL_JDS.md.")
        print(f"   Next: python scripts/score_jobs.py")
    else:
        print("No new JDs found this run.")


if __name__ == "__main__":
    main()
