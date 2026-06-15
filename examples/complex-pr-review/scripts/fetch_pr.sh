#!/usr/bin/env bash
# Fetch PR diff metadata. Requires gh CLI or git fallback.
set -euo pipefail
PR="${1:?Usage: fetch_pr.sh <pr_number>}"
REPO="${2:-.}"

if command -v gh >/dev/null 2>&1; then
  gh pr diff "$PR" --repo "$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")"
  gh pr view "$PR" --json title,files --jq '{title: .title, files: [.files[].path]}'
else
  echo "gh not found — use git fetch origin pull/${PR}/head" >&2
  exit 2
fi
