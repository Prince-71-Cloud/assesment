#!/usr/bin/env python3
"""Automated verifier. Shared implementation, parameterised by this task's task.json.

Usage:  python verifier.py "<candidate_flag>"
Exit 0 = correct, 1 = incorrect, 2 = usage error.  Always prints a JSON verdict
so an automated eval loop can parse the result without scraping prose.
"""
import json
import re
import sys
from pathlib import Path


def check(candidate: str) -> dict:
    task = json.loads((Path(__file__).parent / "task.json").read_text())
    expected = task["flag"].strip()
    candidate = candidate.strip()
    fmt = task.get("flag_format")

    # Accept a flag embedded in surrounding model output, e.g. "the flag is FLAG{...}"
    if candidate != expected and fmt:
        m = re.search(fmt, candidate)
        if m:
            candidate = m.group(0)

    verdict = {
        "task_id": task["task_id"],
        "candidate": candidate,
        "correct": candidate == expected,
    }
    if fmt is not None:
        verdict["format_ok"] = bool(re.fullmatch(fmt, candidate))
    return verdict


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: verifier.py <candidate_flag>"}))
        return 2
    verdict = check(sys.argv[1])
    print(json.dumps(verdict))
    return 0 if verdict["correct"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
