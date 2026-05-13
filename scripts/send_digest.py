"""
send_digest.py — Phase D email digest sender.

What this file does, in plain English:
  1. Reads the most recent scoring run from _local/scored_results.json (the
     primary output of scripts/score_jobs.py).
  2. Filters to roles with final_score >= DIGEST_SCORE_THRESHOLD (default 6,
     overridable via .env). Roles below the threshold stay in the Sheet only.
  3. Sorts the survivors by score DESC and renders a plain-text email body
     with two sections — STRONG (>=8) and MODERATE (6-7) — each role showing
     score / verdict / per-dim breakdown / 1-line reason / H1B note / apply URL.
  4. Sends the email to DIGEST_RECIPIENT_EMAIL via Resend's REST API
     (no Resend Python SDK required — it's a single POST).
  5. If 0 roles meet the threshold, no email is sent (logs a console note
     instead of mailing an empty digest).

Standalone CLI:
    python scripts/send_digest.py            # send (skipped if already sent for this scoring run)
    python scripts/send_digest.py --dry-run  # print body to stdout, don't send, don't update marker
    python scripts/send_digest.py --force    # bypass the already-sent guard

Idempotency: after a successful send, writes _local/last_sent_digest.json
with the scored_results.json mtime + Resend ID. The next run compares the
current mtime against the marker and skips if scored_results.json hasn't
changed since (i.e., score_jobs.py hasn't run since the last digest). This
prevents accidentally re-emailing the same digest if the chained one-liner
is run twice or if score_jobs.py errored mid-pipeline. Pass --force to
override (e.g., recipient never received the first send).

Reads from .env:
    RESEND_API_KEY            (required for actual send)
    DIGEST_RECIPIENT_EMAIL    (required for actual send)
    DIGEST_FROM_EMAIL         (optional; default 'Job Matcher <onboarding@resend.dev>')
    DIGEST_SCORE_THRESHOLD    (optional; default 6)
    GOOGLE_SHEET_ID           (optional; if set, top of email links to the Sheet)

Why Resend's `onboarding@resend.dev` as the default sender: Resend pre-verifies
that domain so emails ship without DNS setup. Deliverability is OK for personal
inboxes; verify your own domain later if you want a custom From address.

V1 scope intentionally excludes resume/cover-letter snippets — those are the
V2 Resume Agent's job per project_v2_resume_agent memory.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCORED_RESULTS_PATH = PROJECT_ROOT / "_local" / "scored_results.json"
LAST_SENT_MARKER_PATH = PROJECT_ROOT / "_local" / "last_sent_digest.json"
DEFAULT_FROM = "Job Matcher <onboarding@resend.dev>"
DEFAULT_THRESHOLD = 6
RESEND_URL = "https://api.resend.com/emails"

VERDICT_CHIP = {"prioritize": "🟢", "apply": "🟡", "weak": "⚪"}


def _is_valid_apply_url(url: str | None) -> bool:
    return isinstance(url, str) and url.startswith(("http://", "https://"))


def render_role(r: dict[str, Any], idx: int) -> str:
    s = r.get("scores", {})
    chip = VERDICT_CHIP.get(r.get("verdict", ""), "•")
    lines = [
        f"{idx}. {chip} {r['company']} — {r['title']} — {r.get('location', 'unknown')}",
        f"   Score: {r['final_score']}/10  •  Verdict: {r.get('verdict', '?')}  •  H1B: {r.get('h1b_status', 'unknown')}",
        "",
        f"   Per-dim:  Domain {s.get('domain', '?')}  •  Skills {s.get('skills', '?')}  •  Level {s.get('level', '?')}  •  Team needs {s.get('team_needs', '?')}",
        "",
        "   Reasoning:",
        f"     {r.get('reason_short', '(none)')}",
    ]
    if r.get("h1b_note"):
        lines += ["", f"   H1B note: {r['h1b_note']}"]
    if _is_valid_apply_url(r.get("posting_url")):
        lines += ["", f"   Apply: {r['posting_url']}"]
    else:
        lines += ["", "   Apply: (no public URL — see MANUAL_JDS.md or the Sheet for full JD)"]
    return "\n".join(lines)


def render_email_body(roles: list[dict[str, Any]], sheet_id: str | None, threshold: int) -> str:
    strong = [r for r in roles if r["final_score"] >= 8]
    moderate = [r for r in roles if threshold <= r["final_score"] < 8]
    parts: list[str] = []
    if sheet_id:
        parts += [f"📊 Open Sheet: https://docs.google.com/spreadsheets/d/{sheet_id}/edit", ""]
    parts += [
        "=" * 65,
        f"🟢 STRONG MATCHES (≥ 8/10) — {len(strong)} role(s)",
        "=" * 65,
        "",
    ]
    if strong:
        for i, r in enumerate(strong, 1):
            parts += [render_role(r, i), ""]
    else:
        parts += ["(none this run)", ""]
    parts += [
        "=" * 65,
        f"🟡 MODERATE MATCHES ({threshold}–7/10) — {len(moderate)} role(s)",
        "=" * 65,
        "",
    ]
    if moderate:
        for i, r in enumerate(moderate, 1):
            parts += [render_role(r, i), ""]
    else:
        parts += ["(none this run)", ""]
    parts += [
        "---",
        f"Generated by score_jobs.py at {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Threshold: only roles ≥ {threshold}/10 in this email. Lower-score roles are in the Sheet.",
    ]
    return "\n".join(parts)


def render_subject(roles: list[dict[str, Any]], threshold: int) -> str:
    strong = sum(1 for r in roles if r["final_score"] >= 8)
    moderate = sum(1 for r in roles if threshold <= r["final_score"] < 8)
    total = strong + moderate
    return f"[Job Matcher] {total} new Platform PM role(s) — {strong} strong, {moderate} moderate"


def send_via_resend(api_key: str, sender: str, recipient: str, subject: str, body: str) -> dict:
    resp = requests.post(
        RESEND_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"from": sender, "to": [recipient], "subject": subject, "text": body},
        timeout=30,
    )
    if resp.status_code >= 300:
        raise RuntimeError(f"Resend HTTP {resp.status_code}: {resp.text}")
    return resp.json()


def _score_or_zero(r: dict[str, Any]) -> int:
    """Coerce missing / null final_score to 0 so filter + sort can't crash on
    a malformed Claude response or a parser-fallback entry."""
    s = r.get("final_score")
    return s if isinstance(s, int) else 0


def _read_last_sent_marker() -> dict | None:
    if not LAST_SENT_MARKER_PATH.exists():
        return None
    try:
        with open(LAST_SENT_MARKER_PATH) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _write_last_sent_marker(scored_mtime: float, n_roles: int, resend_id: str) -> None:
    LAST_SENT_MARKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LAST_SENT_MARKER_PATH, "w") as f:
        json.dump(
            {
                "sent_at": datetime.now().isoformat(timespec="seconds"),
                "scored_results_mtime": scored_mtime,
                "n_roles_in_email": n_roles,
                "resend_id": resend_id,
            },
            f,
            indent=2,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Send Phase D email digest of scored roles.")
    parser.add_argument("--dry-run", action="store_true", help="Print subject + body to stdout instead of sending")
    parser.add_argument("--force", action="store_true", help="Send even if this scored_results.json was already emailed")
    args = parser.parse_args()

    load_dotenv()

    if not SCORED_RESULTS_PATH.exists():
        print(f"❌ {SCORED_RESULTS_PATH} not found. Run scripts/score_jobs.py first.", file=sys.stderr)
        sys.exit(1)

    scored_mtime = SCORED_RESULTS_PATH.stat().st_mtime
    last_sent = _read_last_sent_marker()
    if not args.dry_run and not args.force and last_sent and scored_mtime <= last_sent.get("scored_results_mtime", 0):
        print(
            f"ℹ️  Skipping — this scoring run was already emailed at {last_sent.get('sent_at')} "
            f"({last_sent.get('n_roles_in_email')} role(s)). "
            f"Re-run scripts/score_jobs.py to produce new results, or pass --force to re-send."
        )
        return

    with open(SCORED_RESULTS_PATH) as f:
        all_roles = json.load(f)

    threshold = int(os.environ.get("DIGEST_SCORE_THRESHOLD", DEFAULT_THRESHOLD))
    survivors = sorted(
        [r for r in all_roles if _score_or_zero(r) >= threshold],
        key=lambda r: -_score_or_zero(r),
    )

    if not survivors:
        print(f"No roles with final_score >= {threshold} in last run ({len(all_roles)} total scored). No email sent.")
        return

    sheet_id = os.environ.get("GOOGLE_SHEET_ID") or None
    body = render_email_body(survivors, sheet_id, threshold)
    subject = render_subject(survivors, threshold)

    if args.dry_run:
        print(f"=== Subject ===\n{subject}\n\n=== Body ===\n{body}")
        return

    api_key = os.environ.get("RESEND_API_KEY")
    recipient = os.environ.get("DIGEST_RECIPIENT_EMAIL")
    sender = os.environ.get("DIGEST_FROM_EMAIL", DEFAULT_FROM)
    if not api_key or not recipient:
        print(
            "❌ RESEND_API_KEY and DIGEST_RECIPIENT_EMAIL must be set in .env. See docs/PHASE_D_SETUP.md",
            file=sys.stderr,
        )
        sys.exit(1)

    result = send_via_resend(api_key, sender, recipient, subject, body)
    resend_id = result.get("id", "?")
    _write_last_sent_marker(scored_mtime, len(survivors), resend_id)
    print(f"✅ Sent to {recipient} — Resend ID: {resend_id}")
    print(f"   Subject: {subject}")
    print(f"   Roles in email: {len(survivors)} (threshold={threshold})")


if __name__ == "__main__":
    main()
