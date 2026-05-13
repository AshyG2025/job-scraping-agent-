"""
check_resend.py — Phase D Resend connection diagnostic.

What this file does, in plain English:
  Sends one short test email via Resend to confirm your API key + recipient
  + from-address are all wired correctly. Run after completing
  docs/PHASE_D_SETUP.md, the same way you'd run check_sheets.py after Phase C.

Reads from .env:
    RESEND_API_KEY
    DIGEST_RECIPIENT_EMAIL
    DIGEST_FROM_EMAIL (optional; default 'Job Matcher <onboarding@resend.dev>')

Output:
    ✅ Sent successfully to <recipient> — Resend ID: <id>
or:
    ❌ <specific error from Resend's API>
"""
from __future__ import annotations

import os
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

DEFAULT_FROM = "Job Matcher <onboarding@resend.dev>"
RESEND_URL = "https://api.resend.com/emails"


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("RESEND_API_KEY")
    recipient = os.environ.get("DIGEST_RECIPIENT_EMAIL")
    sender = os.environ.get("DIGEST_FROM_EMAIL", DEFAULT_FROM)

    if not api_key:
        print("❌ RESEND_API_KEY missing from .env. See docs/PHASE_D_SETUP.md.", file=sys.stderr)
        sys.exit(1)
    if not recipient:
        print("❌ DIGEST_RECIPIENT_EMAIL missing from .env. See docs/PHASE_D_SETUP.md.", file=sys.stderr)
        sys.exit(1)

    print(f"Sending test email from {sender} to {recipient}...")
    resp = requests.post(
        RESEND_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "from": sender,
            "to": [recipient],
            "subject": "[Job Matcher] Test email — Phase D wired up ✓",
            "text": (
                f"This test email confirms your Resend setup is working.\n\n"
                f"Sent at: {datetime.now().isoformat(timespec='seconds')}\n"
                f"From:    {sender}\n"
                f"To:      {recipient}\n\n"
                f"Next step: run `python scripts/send_digest.py --dry-run` to preview\n"
                f"the digest body, then drop --dry-run to send the real thing.\n"
            ),
        },
        timeout=30,
    )
    if resp.status_code >= 300:
        print(f"❌ Resend returned HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)
    print(f"✅ Sent successfully — Resend ID: {resp.json().get('id', '?')}")
    print(f"   Check {recipient} in 5–10 sec.")


if __name__ == "__main__":
    main()
