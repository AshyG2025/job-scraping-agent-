# Phase D — Email Digest Setup (one-time, ~5 min)

> **What this is:** A short walkthrough to wire up the email digest that lands in your inbox after every `python scripts/score_jobs.py` run. You only do this once. After that, every time you run `python scripts/send_digest.py`, your inbox gets a structured email of the day's matches (≥6/10 only — weak roles stay in the Sheet).
>
> **Why Resend (not Gmail API)?** Resend gives you one POST endpoint + one API key — about 10 lines of integration code vs ~50 for Gmail OAuth + Google Cloud setup. The free tier (3,000 emails/mo) is far more than this project will ever use. The trade-off: emails arrive from a Resend-managed `From` address rather than your personal Gmail. If deliverability becomes a problem, the Optional Step at the bottom shows how to verify your own domain later.
>
> **What you'll end up with:** A `RESEND_API_KEY` + `DIGEST_RECIPIENT_EMAIL` + `DIGEST_FROM_EMAIL` in your `.env`, and a working `python scripts/check_resend.py` that lands a test email in your inbox.

---

## Prerequisites

- Any working email address (where the digests should land)
- ~5 min of focused time
- A web browser

---

## Step 1 — Create a free Resend account

1. Go to https://resend.com/signup
2. Sign up with email + password (or "Sign in with GitHub" — both work)
3. Verify your email address via the confirmation link Resend sends you

**Verify:** You're now in the Resend dashboard at `resend.com/dashboard`.

---

## Step 2 — Create an API key

1. In the left sidebar, click **API Keys**
2. Click the **+ Create API Key** button (top-right)
3. Name it `job-scraping-agent` (or any name you'll recognize)
4. **Permission:** leave as **"Sending access"** (the default — read-only for sending, can't manage your account)
5. **Domain:** leave as **"All domains"** for now (we're using Resend's pre-verified `onboarding@resend.dev` sender)
6. Click **Add**
7. **CRITICAL:** Resend shows you the API key **once**. Copy it now. It looks like `re_AbCdEf123...`. If you lose it, you'll have to create a new one — that's fine, just don't close the modal without copying.

---

## Step 3 — Add the three env vars to `.env`

Open `.env` in your project root (it already exists from earlier setup) and append these three lines:

```bash
# Phase D — email digest
RESEND_API_KEY=re_paste_your_key_here
DIGEST_RECIPIENT_EMAIL=ghoshalayesha@gmail.com
DIGEST_FROM_EMAIL=Job Matcher <onboarding@resend.dev>
```

Notes:
- **`RESEND_API_KEY`** — paste the `re_…` value from Step 2.
- **`DIGEST_RECIPIENT_EMAIL`** — already filled in with the address you gave during setup. Edit if you want digests sent somewhere else.
- **`DIGEST_FROM_EMAIL`** — leave as the default. `onboarding@resend.dev` is a Resend-managed sender that needs zero DNS setup. The `Job Matcher` part is just the display name your inbox will show.

**Optional 4th var** if you want to override the default score threshold (which is 6, meaning roles scoring ≥6 are emailed):

```bash
DIGEST_SCORE_THRESHOLD=7   # only "apply" or stronger
```

---

## Step 4 — Send a test email

```bash
source .venv/bin/activate
python scripts/check_resend.py
```

**Expected output:**
```
Sending test email from Job Matcher <onboarding@resend.dev> to ghoshalayesha@gmail.com...
✅ Sent successfully — Resend ID: 7c3d…
   Check ghoshalayesha@gmail.com in 5–10 sec.
```

Check your inbox. The test email's subject is `[Job Matcher] Test email — Phase D wired up ✓`. If it lands in spam, mark it "Not spam" once and Gmail will learn.

**If you got an error instead:**
- `❌ RESEND_API_KEY missing from .env` → re-check Step 3; make sure no quotes around the key value, no trailing whitespace
- `❌ Resend returned HTTP 401` → API key is wrong/revoked; create a new one in Step 2
- `❌ Resend returned HTTP 422` → recipient email is malformed; double-check `DIGEST_RECIPIENT_EMAIL`

---

## Step 5 — Preview a real digest (no email sent)

Now that Resend works, preview what a real digest would look like off your existing scored results — without actually sending:

```bash
python scripts/send_digest.py --dry-run
```

This prints the subject line + email body to your terminal. Sanity-check the formatting and which roles are included. When you're happy with it, drop the `--dry-run` flag to actually send.

---

## Day-to-day usage

After every scoring run, send the digest:

```bash
python scripts/run_scrapers.py && python scripts/score_jobs.py && python scripts/send_digest.py
```

When Phase E (GitHub Actions cron) ships, this whole chain runs automatically Tue + Thu mornings.

---

## Optional — Verify your own domain (later, not required)

If deliverability becomes a problem (digests landing in spam consistently, or you want a custom `From` address like `digest@yourdomain.com`):

1. In Resend dashboard, click **Domains** → **+ Add Domain**
2. Resend gives you 3 DNS records to add to your domain registrar (TXT records for SPF + DKIM + DMARC)
3. Once verified, edit `.env`: `DIGEST_FROM_EMAIL=digest@yourdomain.com`

Skip this until / unless you actually see a deliverability problem. The default `onboarding@resend.dev` sender is fine for personal-volume usage.

---

## Troubleshooting

**Test email arrived but a real digest never sends:**
Run `python scripts/send_digest.py --dry-run` first. If body renders, the issue is your env vars; if body is empty, your last `score_jobs.py` run produced 0 roles ≥ threshold (check `_local/scored_results.json`).

**API key got committed to git by accident:**
Revoke it immediately in Resend dashboard → API Keys → trash icon. Create a new one. Then `git filter-repo` or rewrite history to scrub the leaked key.

**Want HTML formatting instead of plain text:**
Out of scope for V1 by design — plain text matches the README mockup, has zero rendering surprises across Gmail / Outlook / Apple Mail, and is easier to review at a glance. If you want HTML later, Resend's REST API takes an `html` field alongside `text` — drop it into `send_via_resend()` in `scripts/send_digest.py`.
