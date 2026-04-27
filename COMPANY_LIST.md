# Company List

> **How this file is used:**
> - The agent's **targeted scraper** scrapes the careers page of every company in Tier 1 / Tier 2 / Tier 3 on every run.
> - The H1B status here is the source of truth for the H1B filter in `HARD_FILTERS.md`.
> - **Edit freely.** Add a company by dropping a bullet under the right tier; remove one by deleting its line. Keep the format consistent so the parser can read it.
>
> **Format per company:** `- {Company} — {Why it matches} | H1B: {✅ ⚠️ ❌} | Geo focus: {Seattle / SF / London / Multiple}`
>
> **Last updated:** 2026-04-27

---

## Tier 1 — Strong Match (priority scrape, prioritize applications)

### Big Tech / Public — US
- **Amazon** — Already at; Vendor Central, Internal Tools, AWS internal platforms (NOT pure compute/storage AWS roles) | H1B: ✅ | Geo: Seattle, SF Bay
- **Microsoft** — Azure platform products, internal developer platforms, enterprise integration | H1B: ✅ | Geo: Seattle, SF Bay
- **Google** — Internal platform products, integration platforms (NOT pure GCP infrastructure) | H1B: ✅ | Geo: SF Bay, Seattle
- **Meta** — Internal platform engineering, internal tools (scale gap to address) | H1B: ✅ | Geo: SF Bay, Seattle
- **Salesforce** — Integration Hub, platform consolidation, API products | H1B: ✅ | Geo: SF Bay
- **ServiceNow** — Workflow automation platforms, enterprise integration | H1B: ✅ | Geo: SF Bay
- **Atlassian** — Jira/Confluence platform, integration products, developer tools | H1B: ✅ | Geo: SF Bay
- **Stripe** — Internal platforms, integration platforms (external API roles = stretch — see Tier 3) | H1B: ✅ | Geo: SF Bay
- **Visa** — Merchant platform, payment platform, internal operations platforms | H1B: ✅ | Geo: SF Bay
- **PayPal** — Merchant platform, internal platform products, payment integrations | H1B: ✅ | Geo: SF Bay
- **Uber** — Merchant platform, Driver platform, internal ops platforms | H1B: ✅ | Geo: SF Bay, Seattle
- **DoorDash** — Merchant platform, Dasher platform, logistics platforms | H1B: ✅ | Geo: SF Bay, Seattle
- **Airbnb** — Host platform, internal platforms | H1B: ✅ | Geo: SF Bay
- **Zillow** — Marketplace platform, agent/broker platform, real estate APIs | H1B: ✅ | Geo: Seattle

### FinTech growth-stage — US (Series C+)
- **Plaid** — FinTech APIs, integration platform, developer-facing | H1B: ✅ | Geo: SF Bay
- **Brex** — Corporate card / spend platform, finance integrations | H1B: ✅ | Geo: SF Bay
- **Ramp** — Spend management platform, finance integrations | H1B: ⚠️ verify | Geo: SF Bay (NYC HQ, lower priority for geo)
- **Mercury** — Banking-as-a-platform for startups | H1B: ⚠️ verify | Geo: SF Bay
- **Bill.com** — B2B payments platform, AP/AR automation | H1B: ✅ | Geo: SF Bay
- **Adyen** — Payments platform, merchant integrations | H1B: ⚠️ verify (NYC HQ for US, but London HQ open) | Geo: SF Bay, London
- **Marqeta** — Card-issuing platform | H1B: ⚠️ verify | Geo: SF Bay

### Big Tech / Public + Growth — UK / London (no visa filter)
- **Wise** — Business / Treasury / Invoicing platforms, FX rails | H1B: N/A | Geo: London
- **Revolut** — Multi-product FinTech platform, B2B + B2C | H1B: N/A | Geo: London
- **Stripe London** — Internal platforms, integration | H1B: N/A | Geo: London
- **Liberis** — Embedded finance platform, financial systems | H1B: N/A | Geo: London
- **Adyen London** — Payments platform | H1B: N/A | Geo: London
- **Deliveroo** — Merchant platform, restaurant ops, logistics | H1B: N/A | Geo: London
- **Monzo** — Banking platform, B2C + B2B | H1B: N/A | Geo: London
- **GoCardless** — Direct-debit payments platform, API-first | H1B: N/A | Geo: London
- **Checkout.com** — Payments platform, merchant APIs | H1B: N/A | Geo: London
- **Klarna** — Buy-now-pay-later platform, merchant integrations | H1B: N/A | Geo: London (Stockholm HQ but London office)

---

## Tier 2 — Moderate Match (worth scraping; apply with positioning)

### US
- **eBay** — Seller platform, marketplace platform | H1B: ✅ | Geo: SF Bay
- **Walmart** — Marketplace platform, supplier platform, logistics | H1B: ⚠️ verify for PMs | Geo: SF Bay (Bentonville HQ less relevant for geo)
- **Target** — Supplier platform, retail tech platforms | H1B: ⚠️ verify | Geo: Multiple (HQ Minneapolis, lower geo fit)
- **Capital One** — Internal FinTech platforms, ops platforms | H1B: ⚠️ verify for PMs | Geo: SF Bay
- **Square (Block)** — Merchant platform, FinTech rails | H1B: ✅ | Geo: SF Bay
- **Shopify** — Merchant platform, app platform, APIs | H1B: ⚠️ verify | Geo: Remote-friendly
- **Affirm** — BNPL platform, merchant integrations | H1B: ⚠️ verify | Geo: SF Bay
- **Coinbase** — Crypto platform, APIs (note: regulatory volatility) | H1B: ✅ | Geo: SF Bay (remote-first)
- **Snowflake** — Data platform (internal platform PM roles only — pure infra is a stretch) | H1B: ✅ | Geo: SF Bay
- **Databricks** — Data platform (internal platform PM roles only) | H1B: ✅ | Geo: SF Bay
- **Zoom** — Platform integrations, marketplace | H1B: ✅ | Geo: SF Bay

### UK / Europe
- **Starling Bank** — Banking platform, B2B + B2C | H1B: N/A | Geo: London
- **Tide** — SMB banking platform | H1B: N/A | Geo: London
- **Curve** — Card platform, FinTech | H1B: N/A | Geo: London
- **Modulr** — Payments-as-a-platform, B2B | H1B: N/A | Geo: London
- **Truelayer** — Open banking platform, APIs | H1B: N/A | Geo: London

---

## Tier 3 — Stretch (apply only with strong positioning / cover letter)

- **Stripe — external API products** — Their flagship developer platform; my supplier-platform experience needs strong reframing as developer experience | H1B: ✅ | Geo: SF Bay, London
- **Oracle** — Enterprise platforms; technical depth bar is higher than my experience | H1B: ✅ | Geo: SF Bay
- **Snowflake / Databricks — pure data platform PMs** — Different domain; can apply if I'm willing to learn data platform specifics | H1B: ✅ | Geo: SF Bay
- **AWS — internal tools team only** — Pure compute/storage AWS roles are wrong domain; internal tools is OK | H1B: ✅ | Geo: Seattle

---

## Skip / Avoid

- **Pure consumer social platforms** (Instagram, TikTok, Snapchat, Pinterest creator-facing) — wrong domain; exception: their internal platform/infra teams
- **US startups < 200 employees** — H1B sponsorship risk too high
- **Companies known not to sponsor PM H1Bs** — track record indicates won't transfer

---

## Discovery mode — sources

Beyond the named-company scrape, the agent pulls from these **aggregator boards** so we catch growth-stage companies I haven't thought of:

### Always-on aggregators
- **LinkedIn** (via Apify) — title + geo + posting-age filters
- **TrueUp** (truup.com) — Tech-focused aggregator, already part of my manual workflow

### Startup / VC-backed boards (NEW — covers growth-stage companies not on named list)
- **Y Combinator's Work at a Startup** (workatastartup.com) — YC portfolio companies, all stages; useful for catching YC growth-stage cos. (Stripe, DoorDash, Coinbase, Brex, Mercury, etc. all started here)
- **Wellfound** (wellfound.com, formerly AngelList Talent) — Broad startup coverage with stage + role filters
- **A16Z portfolio jobs** (a16z.com/jobs) — Andreessen Horowitz portfolio, leans growth-stage
- **Sequoia Capital portfolio** (sequoiacap.com → portfolio job pages, may scrape via Sequoia Talent)
- **Index Ventures portfolio** — Heavy in European FinTech; relevant for London search
- **Accel portfolio jobs** — Growth-stage tilt
- **Bessemer Venture Partners** — Strong B2B SaaS portfolio
- **Insight Partners** — Late-stage growth, B2B SaaS heavy

### Filters applied to all discovery sources
- Title: contains "Product Manager" + level keywords (Senior / Staff / Principal)
- Location: in geo allowlist (Seattle, SF Bay, London)
- Posting age: ≤ 14 days
- Hard filters from `HARD_FILTERS.md` (no manager titles, IC-only, etc.)
- US roles: H1B status check against this file's named list; unlisted companies get ⚠️ flag (research before applying)

Roles from companies *not* on this list pass through scoring with a `discovery: true` flag. If one scores ≥ 7/10, **promote that company into Tier 1 or Tier 2 by editing this file**.

> **Note on VC portfolio boards:** Many VCs publish portfolio job pages via Greenhouse/Lever/Ashby aggregators. I'll figure out the most reliable scrape path for each in Session 2 when I write the code — some are well-structured, some aren't. If any prove unscrapeable, we either drop them or write a one-off Apify scraper for ~$5/mo.

---

## Companies to research and add (parking lot)

> Add candidates here when I think of them; I'll triage into tiers later.

- _(empty — add as needed)_
