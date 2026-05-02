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

# Make scripts/ importable as a package when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from scrapers import ashby, common, greenhouse, smartrecruiters, workday

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
    {"company": "GoCardless", "ats": "greenhouse", "slug": "gocardless"},
    {"company": "Liberis",    "ats": "greenhouse", "slug": "liberis"},
    {"company": "Marqeta",    "ats": "greenhouse", "slug": "marqeta"},
    {"company": "Mercury",    "ats": "greenhouse", "slug": "mercury"},
    {"company": "Monzo",      "ats": "greenhouse", "slug": "monzo"},
    {"company": "Stripe",     "ats": "greenhouse", "slug": "stripe"},
    # Tier 2
    {"company": "Affirm",     "ats": "greenhouse", "slug": "affirm"},
    {"company": "Block",      "ats": "greenhouse", "slug": "block"},        # migrated off SmartRecruiters; ex-`Square` tenant is dormant
    {"company": "Coinbase",   "ats": "greenhouse", "slug": "coinbase"},
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
]

# Note on Checkout.com: re-reconned to Workday (tenant `checkout`/site `CheckoutCareers`)
# but tenant was in transient maintenance at recon. Add to the Workday block above
# only after a live CXS-endpoint probe confirms it's serving.

ATS_MODULES = {
    "greenhouse": greenhouse,
    "smartrecruiters": smartrecruiters,
    "workday": workday,
    "ashby": ashby,
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
