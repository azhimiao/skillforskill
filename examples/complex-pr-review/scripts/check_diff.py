#!/usr/bin/env python3
"""Lightweight diff checker for PR review skill."""

from __future__ import annotations

import sys
from pathlib import Path

SECRET_PATTERNS = ("AKIA", "SECRET", "password=", "api_key", "token=")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_diff.py <file> [file...]", file=sys.stderr)
        return 2

    issues = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"WARN missing file: {path}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pat in SECRET_PATTERNS:
            if pat.lower() in text.lower():
                print(f"CRITICAL possible secret in {path}: matched '{pat}'")
                issues += 1
    print(f"OK checked {len(sys.argv) - 1} files, {issues} critical pattern(s)")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
