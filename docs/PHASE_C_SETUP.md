# Phase C — Google Sheets Setup (one-time, ~10–15 min)

> **What this is:** A step-by-step walkthrough to wire up the Google Sheet that will store every scored role + your application outcomes. You only do this once. After that, every `python scripts/score_jobs.py` run automatically writes new rows to your Sheet.
>
> **Why a service account (not your personal Google login)?** A service account is a "robot user" Google issues you. It has its own email address (looks like `something@something.iam.gserviceaccount.com`). The script logs in as the robot, not as you. This matters because:
> - When Phase E lands (GitHub Actions runs the pipeline on a cron), there's no human there to click "Allow" on a browser popup. Service-account auth works headless.
> - The robot only has access to Sheets you explicitly share with it. It can't see your other Google Drive files.
> - If the key ever leaks, you can revoke it in one click without affecting your personal Google account.
>
> **What you'll end up with:** A Google Sheet you can open like any normal Sheet, plus a JSON key file in `_local/google_sheets_key.json` (gitignored, never goes to GitHub) that the script uses to authenticate.

---

## Prerequisites

- A Google account (your personal one is fine — the robot user gets created underneath it)
- ~10–15 min of focused time
- A web browser

---

## Step 1 — Create (or reuse) a Google Cloud project

A "project" is just a Google Cloud namespace — like a folder for everything related to this script.

1. Open https://console.cloud.google.com/ in your browser.
2. **If this is your first time:** you'll see a "Welcome" screen. Accept the terms.
3. At the top of the page, click the **project dropdown** (it usually says "Select a project" or shows a current project name).
4. In the popup, click **"New Project"** (top-right).
5. Name it `job-scraping-agent` (or any name you'll recognize). Leave "Organization" / "Location" alone.
6. Click **"Create"**.
7. After ~10 seconds, click the project dropdown again and select your new project.

**Verify:** The top of the page should now show `job-scraping-agent` (or whatever you named it).

---

## Step 2 — Enable the Google Sheets API

By default, your project can't talk to Sheets. You need to flip a switch.

1. In the search bar at the top of the Cloud Console, type **"Google Sheets API"** and press Enter.
2. Click the result that says exactly **"Google Sheets API"** (look for the green Sheets icon).
3. Click the blue **"Enable"** button.
4. Wait ~5 seconds for it to enable.

**Verify:** The page should now say "API enabled" with a blue "Manage" button instead of "Enable."

---

## Step 3 — Create a service account

This is where you create the robot user.

1. In the search bar, type **"Service Accounts"** and click the first result (under IAM & Admin).
2. Click **"+ Create Service Account"** at the top.
3. Fill in:
   - **Service account name:** `job-scraping-sheets-writer`
   - **Service account ID:** auto-fills, leave it
   - **Description:** `Writes scored job rows to the tracking Sheet` *(optional)*
4. Click **"Create and Continue"**.
5. **"Grant this service account access to project"** step — skip it, click **"Continue"**.
6. **"Grant users access"** step — skip it, click **"Done"**.

**Verify:** You should see your new service account in the list with an email like `job-scraping-sheets-writer@<project-id>.iam.gserviceaccount.com`. **Copy this email — you'll need it in Step 7.**

---

## Step 4 — Download the service account's JSON key

The key is what the script uses to log in as the robot.

1. From the service accounts list, click on `job-scraping-sheets-writer` (the email you just created).
2. Go to the **"Keys"** tab at the top.
3. Click **"Add Key" → "Create new key"**.
4. Select **JSON** (default), click **"Create"**.
5. Your browser will download a file named something like `job-scraping-agent-abc123.json`. **This file is a password — guard it.**

---

## Step 5 — Save the key into your project

1. Open Finder. Navigate to your downloaded file.
2. Rename it to `google_sheets_key.json`.
3. Move it to:
   ```
   /Users/ashy/Documents/OVERALL JOB STRATEGY/Job Scraping project/_local/google_sheets_key.json
   ```
   The `_local/` folder is gitignored, so this file will **never** get committed to GitHub.

**Verify:** Run this in Terminal — it should print the file's path:
```
ls "_local/google_sheets_key.json"
```

---

## Step 6 — Create the Google Sheet

1. Open https://sheets.google.com/ and click **"Blank"** to create a new sheet.
2. Rename it to **"Job Scraping Outcomes"** (top-left of the page, click the title).
3. Don't worry about adding any columns or headers — the script will write the header row on its first run.
4. Look at the URL of the page. It looks like:
   ```
   https://docs.google.com/spreadsheets/d/1AbC-2dEfGhIjKlMn0pQrStUvWxYz/edit
                                          └────────── this part ───────────┘
   ```
   The string between `/d/` and `/edit` is the **Sheet ID**. Copy it — you'll need it in Step 8.

---

## Step 7 — Share the Sheet with the service account

The robot can't see the Sheet until you share it.

1. With "Job Scraping Outcomes" open, click the green **"Share"** button (top-right).
2. In the "Add people, groups, and calendar events" box, paste the service account email from Step 3 (the one ending in `iam.gserviceaccount.com`).
3. Make sure the role dropdown says **"Editor"** (not Viewer or Commenter).
4. **Uncheck** "Notify people" — there's no human at that email address.
5. Click **"Share"**.

**Verify:** Click the Share button again — you should see the service account email listed under "People with access" with "Editor" rights.

---

## Step 8 — Update your `.env` file

Open `.env` at the project root in TextEdit (or any editor). Add these two lines at the bottom:

```
GOOGLE_SHEETS_KEY_PATH=_local/google_sheets_key.json
GOOGLE_SHEET_ID=<paste the Sheet ID from Step 6 here>
```

Save and close.

**Verify:** Open the file again — both lines should be there. Don't quote the values.

---

## Step 9 — Verify the connection

Once everything's wired up, run these two commands in Terminal from the project root:

```
source .venv/bin/activate
pip install -r requirements.txt
```

The second command installs `gspread` + `google-auth` (added to `requirements.txt` as part of Phase C).

Then test the connection:

```
python -c "
import os, gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
load_dotenv()
creds = Credentials.from_service_account_file(
    os.environ['GOOGLE_SHEETS_KEY_PATH'],
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
client = gspread.authorize(creds)
sheet = client.open_by_key(os.environ['GOOGLE_SHEET_ID']).sheet1
print('✅ Connected. Sheet title:', sheet.spreadsheet.title)
"
```

**Expected output:** `✅ Connected. Sheet title: Job Scraping Outcomes`

If you get an error, see "Troubleshooting" below.

---

## What happens next

Once Step 9 prints the ✅, tell Claude. Claude will then ship:
- `scripts/sheets.py` — the Sheet writer
- Edits to `scripts/score_jobs.py` to call the writer after every scoring run
- Edits to `scripts/run_scrapers.py` to emit the `source` field
- A tiny tier-lookup helper reading `COMPANY_LIST.md`

After that, every `python scripts/score_jobs.py` run will:
1. Score the JDs as before
2. Write `_local/scored_results.json` (unchanged)
3. **NEW:** Append rows to your Sheet, then re-sort newest-first by score

---

## Troubleshooting

**Error: "FileNotFoundError: \_local/google\_sheets\_key.json"**
The key isn't where the `.env` says it is. Check Step 5 — the file should be at `_local/google_sheets_key.json` exactly.

**Error: "PermissionError" or "The caller does not have permission"**
The Sheet wasn't shared with the service account. Re-do Step 7. Make sure the role is "Editor", not "Viewer".

**Error: "APIError: \[403\] Google Sheets API has not been used in project..."**
The Sheets API isn't enabled. Re-do Step 2.

**Error: "ImportError: No module named gspread"**
The `pip install -r requirements.txt` didn't run, or your virtual environment isn't activated. Re-run:
```
source .venv/bin/activate && pip install -r requirements.txt
```

**Error: "google.auth.exceptions.MalformedError: Could not deserialize key data"**
The JSON key file got corrupted (e.g., opened in a text editor that re-saved it with a different encoding). Go back to Step 4 and download a fresh key.

---

## Security notes

- **`_local/google_sheets_key.json` must never be committed.** The `.gitignore` already covers `_local/`, but double-check by running `git status` — the key file should not appear.
- **If the key ever leaks** (committed by accident, shared in a screenshot, etc.): go to Cloud Console → Service Accounts → your service account → Keys tab → delete the leaked key, then create a new one (Step 4) and update `_local/google_sheets_key.json`.
- **The service account has access only to Sheets you explicitly share with it.** It can't see your other Google Drive files, your inbox, or anything else. If you decide to nuke the whole setup, deleting the service account in Cloud Console revokes all access in one click.

---

**Last updated:** 2026-05-07 (Phase C setup, initial)
