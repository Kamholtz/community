#!/usr/bin/env python3
"""Commit generated Talon list/bookmark churn before an agent edits code."""

from __future__ import annotations

import subprocess
import sys


PATHS = ["*.talon-list", "*.csv", ".vscode/bookmarks.json"]
COMMIT_MESSAGE = "feat: update *.talon-list"


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(args))
    return subprocess.run(args, check=check, text=True)


def main() -> int:
    run(["git", "add", "--", *PATHS])

    diff = run(["git", "diff", "--quiet", "--cached", "--", *PATHS], check=False)
    if diff.returncode == 0:
        print("No generated list/bookmark changes to commit.")
        return 0
    if diff.returncode != 1:
        return diff.returncode

    run(["git", "commit", "-m", COMMIT_MESSAGE, "--", *PATHS])
    run(["git", "push"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
