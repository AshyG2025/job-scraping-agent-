"""
Phase C connection-check — Google Sheets.

Run this after completing the Phase C setup steps (see docs/PHASE_C_SETUP.md)
to confirm the script can authenticate as the service account and open the
"Job Scraping Outcomes" Sheet.

Usage:
    source .venv/bin/activate
    python scripts/check_sheets.py

Expected output:
    ✅ Connected. Sheet title: Job Scraping Outcomes

If this errors, see the "Troubleshooting" section at the bottom of
docs/PHASE_C_SETUP.md.

Reads two values from .env:
    GOOGLE_SHEETS_KEY_PATH — path to the service account JSON key
    GOOGLE_SHEET_ID        — the Sheet ID copied from the URL during setup
"""

import os
import sys

try:
    import gspread
    from google.oauth2.service_account import Credentials
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependency: {e.name}")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)


def main() -> None:
    load_dotenv()

    key_path = os.environ.get("GOOGLE_SHEETS_KEY_PATH")
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")

    if not key_path:
        print("❌ GOOGLE_SHEETS_KEY_PATH is not set in .env")
        sys.exit(1)
    if not sheet_id:
        print("❌ GOOGLE_SHEET_ID is not set in .env")
        sys.exit(1)
    if not os.path.exists(key_path):
        print(f"❌ Key file not found at: {key_path}")
        print("   Re-check Step 5 of docs/PHASE_C_SETUP.md")
        sys.exit(1)

    creds = Credentials.from_service_account_file(
        key_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1
    print(f"✅ Connected. Sheet title: {sheet.spreadsheet.title}")


if __name__ == "__main__":
    main()
