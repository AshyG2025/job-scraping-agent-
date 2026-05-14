# Phase E — GitHub Actions Cron Setup (one-time, ~10 min)

> **What this is:** A walkthrough to enable the cron workflow that runs the full pipeline (`run_scrapers.py && score_jobs.py && send_digest.py`) automatically every Tuesday + Thursday at 9am PT. You set 9 secrets via the GitHub web UI once, then the cron runs hands-off forever.
>
> **Note (2026-05-14):** Two of the 9 secrets — `PROJECT_BRIEF_MD` and `COMPANY_LIST_MD` — hold the *contents* of two markdown files that are gitignored locally (per CLAUDE.md Rule 7). Whenever you edit `PROJECT_BRIEF.md` or `COMPANY_LIST.md` locally, you must re-upload the corresponding secret or the cron will keep scoring against the stale version. The re-upload procedure is the same as the initial upload (Step 2 below).
>
> **What you'll end up with:** A working scheduled workflow at `.github/workflows/scrape.yml`. Every Tue + Thu morning, the runner spins up, scrapes, scores, writes to your Sheet, and emails you the digest. If anything fails, GitHub emails the repo owner automatically (no extra config).
>
> **Why secrets and not `.env`?** GitHub Actions runners are fresh ephemeral VMs — they don't have your local `.env` file. Secrets are GitHub's encrypted storage for values your workflow needs (API keys, IDs, etc.). They're injected as environment variables at workflow runtime and never logged.

---

## Prerequisites

- Phases A + B + C + D all working locally (verified end-to-end)
- The workflow file `.github/workflows/scrape.yml` is committed to `main` (it should be — that ships in the same PR as this doc)
- Repo URL: `https://github.com/AshyG2025/job-scraping-agent-`
- ~10 min focused time + your existing local `.env` open in another window for reference

---

## Step 1 — Open the GitHub Secrets page

1. In your browser, go to: **https://github.com/AshyG2025/job-scraping-agent-/settings/secrets/actions**
2. You should see a page titled **"Actions secrets and variables"**
3. The **"Repository secrets"** section is what you'll be adding to (probably empty right now)

If GitHub asks you to log in or re-authenticate, do that first.

---

## Step 2 — Add the 9 secrets

Click **"New repository secret"** (green button, top-right of the Repository secrets section) once for each row below. For each: enter the **Name** exactly as shown (case-sensitive), paste the **Value** from your local `.env`, click **Add secret**.

| # | Name | Value source | Notes |
|---|---|---|---|
| 1 | `ANTHROPIC_API_KEY` | Copy from `.env` line `ANTHROPIC_API_KEY=…` | The `sk-ant-…` value |
| 2 | `GOOGLE_SHEET_ID` | Copy from `.env` line `GOOGLE_SHEET_ID=…` | The Sheet ID (like `119f25y…`) |
| 3 | `GOOGLE_SHEETS_KEY_JSON` | **Special** — see Step 3 below | The *contents* of `_local/google_sheets_key.json`, NOT the path |
| 4 | `APIFY_API_TOKEN` | Copy from `.env` line `APIFY_API_TOKEN=…` | The `apify_api_…` value |
| 5 | `RESEND_API_KEY` | Copy from `.env` line `RESEND_API_KEY=…` | The `re_…` value |
| 6 | `DIGEST_RECIPIENT_EMAIL` | Copy from `.env` line `DIGEST_RECIPIENT_EMAIL=…` | e.g., `danielsnora07@gmail.com` |
| 7 | `DIGEST_FROM_EMAIL` | Copy from `.env` line `DIGEST_FROM_EMAIL=…` | e.g., `Job Matcher <onboarding@resend.dev>` |
| 8 | `PROJECT_BRIEF_MD` | **Special** — see Step 3b below | The *contents* of local `PROJECT_BRIEF.md` (the file is gitignored, so it's pasted into a secret) |
| 9 | `COMPANY_LIST_MD` | **Special** — see Step 3b below | The *contents* of local `COMPANY_LIST.md` (same reason as #8) |

---

## Step 3 — The Google Sheets JSON secret (special)

Secret #3 above is different from the others — locally, `.env` has a *path* (`GOOGLE_SHEETS_KEY_PATH=_local/google_sheets_key.json`), but GitHub Actions can't read your local files. So we paste the *contents* of that JSON key into the secret, and the workflow writes them to a file at runtime.

1. In Terminal, from your project root, run:
   ```
   pbcopy < _local/google_sheets_key.json
   ```
   This copies the entire JSON file contents to your clipboard. (`pbcopy` is Mac-only; Windows: open the file in TextEdit, Cmd+A, Cmd+C.)
2. Back on the GitHub secrets page, click **New repository secret**
3. **Name:** `GOOGLE_SHEETS_KEY_JSON` (exactly — case-sensitive, ends in `_JSON`, not `_PATH`)
4. **Value:** Paste (Cmd+V). You should see a multi-line block starting with `{` and ending with `}`, containing fields like `"type"`, `"project_id"`, `"private_key"`, etc.
5. Click **Add secret**

**Verify:** The secrets page should now list 7 entries: `ANTHROPIC_API_KEY`, `APIFY_API_TOKEN`, `DIGEST_FROM_EMAIL`, `DIGEST_RECIPIENT_EMAIL`, `GOOGLE_SHEET_ID`, `GOOGLE_SHEETS_KEY_JSON`, `RESEND_API_KEY` (alphabetically sorted by GitHub). After Step 3b you'll have 9 total.

---

## Step 3b — The two markdown-content secrets (PROJECT_BRIEF_MD + COMPANY_LIST_MD)

Secrets #8 and #9 are like #3 — locally these are *files* (`PROJECT_BRIEF.md`, `COMPANY_LIST.md` at the repo root), but they're gitignored per CLAUDE.md Rule 7 (they contain your private strategic detail + named target companies). So we paste each file's *contents* into a secret, and the workflow writes them back to disk at runtime.

For each of the two files, run from your project root:

```
pbcopy < PROJECT_BRIEF.md
```

then on the GitHub secrets page → **New repository secret** → Name `PROJECT_BRIEF_MD` → paste (Cmd+V) → **Add secret**.

Repeat with:

```
pbcopy < COMPANY_LIST.md
```

→ Name `COMPANY_LIST_MD` → paste → **Add secret**.

**Verify:** The secrets page should now list 9 entries total (7 from Step 2 + `COMPANY_LIST_MD` + `PROJECT_BRIEF_MD`).

**Important — ongoing chore:** Whenever you edit `PROJECT_BRIEF.md` or `COMPANY_LIST.md` locally (adding a company, changing a tier, updating a flagship metric, etc.), re-run the matching `pbcopy < …` command and **update the corresponding secret** in GitHub:
- Open the secret on the secrets page
- Click **Update**
- Paste the fresh contents
- Click **Update secret**

If you forget, the next cron run will score against the stale version of the file (silently — there's no warning). A reasonable habit: re-upload the secret in the same session you edit the local file.

---

## Step 4 — Test the workflow manually (don't wait for Tuesday)

1. In your browser, go to: **https://github.com/AshyG2025/job-scraping-agent-/actions**
2. In the left sidebar, click the workflow named **"Job scraper — Tue/Thu morning"**
3. Click **"Run workflow"** (gray dropdown button, right side of the page)
4. Leave the branch as `main`, click the green **Run workflow** button in the dropdown
5. Refresh the page after ~5 sec — a new run should appear at the top with a yellow "in progress" dot
6. Click the run to watch live logs. Each step should turn green:
   - ✅ Checkout repo
   - ✅ Set up Python 3.11
   - ✅ Install dependencies
   - ✅ Restore _local/ runtime state
   - ✅ Write Google Sheets service-account key
   - ✅ Write private context files from secrets
   - ✅ Run scrapers (Phase B)
   - ✅ Score jobs (Phase A + Phase C Sheet write)
   - ✅ Send email digest (Phase D)
   - ✅ Upload run artifacts

**Expected total time:** ~10–15 min. The Apify LinkedIn step is the slow one (~5-8 min).

**Done when:** the run shows a green check at the top, and:
- A new email lands in `DIGEST_RECIPIENT_EMAIL` with subject `[Job Matcher] N new Platform PM role(s)…`
- New rows appear in your Google Sheet
- An artifact named `pipeline-output-<run-id>` is downloadable from the run's summary page (contains `digest.md` + `scored_results.json` for post-mortem)

---

## Day-to-day usage

**You do nothing.** Every Tuesday + Thursday at 9am PT (year-round; drifts to 10am during US Daylight Saving), the cron fires automatically. You check your inbox + Sheet.

If a workflow fails, GitHub emails the repo owner (you, at the email associated with your GitHub account). Click the link in the failure email to see the failed step's logs.

---

## Troubleshooting

**The run failed at "Run scrapers (Phase B)" with `ApifyApiError: invalid token`:**
The `APIFY_API_TOKEN` secret value doesn't match a live Apify token. Re-check Step 2 — the token may have been rotated locally without updating GitHub.

**The run failed at "Score jobs" with `anthropic.AuthenticationError`:**
The `ANTHROPIC_API_KEY` secret is wrong/revoked. Generate a new key at console.anthropic.com → API Keys, paste into GitHub secrets, rotate `.env` locally too.

**The run failed at "Score jobs" with a Google Sheets error:**
Most likely the `GOOGLE_SHEETS_KEY_JSON` secret has malformed JSON (extra whitespace, trailing characters, missing braces). Re-do Step 3 — `pbcopy < _local/google_sheets_key.json` and paste fresh.

**The run failed at "Score jobs" with `FileNotFoundError: PROJECT_BRIEF.md` or `COMPANY_LIST.md`:**
The corresponding markdown-content secret (`PROJECT_BRIEF_MD` or `COMPANY_LIST_MD`) is either missing or empty. Re-do Step 3b — `pbcopy < PROJECT_BRIEF.md` (or `< COMPANY_LIST.md`), open the secret on GitHub, click **Update**, paste, **Update secret**.

**The cron picked stale company / brief content (e.g., scored against an old tier list):**
You edited `PROJECT_BRIEF.md` or `COMPANY_LIST.md` locally but forgot to re-upload the matching secret. Do the `pbcopy` + Update flow in Step 3b. Confirm with a manual `workflow_dispatch` trigger — the next run will use the fresh content.

**The run failed at "Send email digest" with HTTP 403:**
You're hitting the same Resend gotcha as Phase D setup — `DIGEST_RECIPIENT_EMAIL` doesn't match the email you signed up to Resend with. See `docs/PHASE_D_SETUP.md` Step 4 troubleshooting for the three fixes.

**The run succeeded but the email never arrived:**
Check spam. If still missing, click the run's `Send email digest` step to see if it logged `Skipping — already emailed at …` (the re-send guard fired because nothing changed since the last run).

**I want to disable the cron temporarily:**
Open `.github/workflows/scrape.yml`, comment out the `- cron: "0 17 * * 2,4"` line, commit, push. Re-enable by uncommenting. The `workflow_dispatch:` trigger still works for manual runs while disabled.

**I want to change the schedule:**
Edit the cron expression on line `- cron: "0 17 * * 2,4"`. Use https://crontab.guru/ to translate. Remember: GitHub Actions cron is **always UTC** — convert from PT yourself (PT = UTC−8 winter, UTC−7 summer; pick one and accept the 1hr drift twice a year).

---

## Optional — Slack / Discord / SMS notifications

GitHub's default failure email is the lightest path. If you want richer alerting later, common patterns:
- **Slack:** add a step using `slackapi/slack-github-action` with a webhook URL stored as another secret
- **Discord:** same idea using `Ilshidur/action-discord`
- **SMS:** Twilio API call from a final step

Out of scope for V1.

---

## Cost reminder

Per-run costs (matches the local Tue/Thu chain):
- Anthropic API: ~$1 (≈8-12 roles × $0.12 each)
- Apify LinkedIn: ~$0.20 (3 searches × ~67 results)
- Resend: $0 (free tier covers ≤3K emails/mo; we send ≤8/mo)
- GitHub Actions: $0 (public/private repo on free tier gets 2K minutes/mo; our runs are ~15 min × 8 = 120 min/mo)

**Monthly total:** ~$10/mo (~$1.20 × 8 runs). Same as the local chain — Phase E adds zero compute cost.
