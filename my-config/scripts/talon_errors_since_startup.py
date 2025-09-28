#!/usr/bin/env python3
"""Extract Talon log errors recorded after the most recent startup."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

START_MARKER = "Talon Version:"
LOG_ENTRY_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+(?P<level>[A-Z]+)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Print Talon log error entries that occurred after the most recent "
            "startup marker. The startup marker is identified by the latest line "
            "containing 'Talon Version:'."
        )
    )
    parser.add_argument(
        "--log-path",
        type=Path,
        default=Path.home() / ".talon" / "talon.log",
        help="Path to the Talon log file (defaults to ~/.talon/talon.log).",
    )
    return parser.parse_args()


def find_last_start_offset(log_path: Path) -> int | None:
    """Return the byte offset of the latest startup marker, if any."""
    offset: int | None = None
    with log_path.open("r", encoding="utf-8", errors="replace") as handle:
        while True:
            position = handle.tell()
            line = handle.readline()
            if not line:
                break
            if START_MARKER in line:
                offset = position
    return offset


def collect_error_blocks(log_path: Path, start_offset: int) -> list[str]:
    """Gather error entries recorded at or after the given byte offset."""
    errors: list[str] = []
    with log_path.open("r", encoding="utf-8", errors="replace") as handle:
        handle.seek(start_offset)
        current_block: list[str] = []
        capturing = False
        for line in handle:
            entry_match = LOG_ENTRY_RE.match(line)
            if capturing and entry_match:
                errors.append("".join(current_block).rstrip("\n"))
                current_block = []
                capturing = False
            if entry_match and entry_match.group("level") == "ERROR":
                capturing = True
                current_block = [line]
                continue
            if capturing:
                current_block.append(line)
        if capturing and current_block:
            errors.append("".join(current_block).rstrip("\n"))
    return errors


def print_errors(errors: Iterable[str]) -> None:
    printed = False
    for block in errors:
        print(block)
        print()
        printed = True
    if not printed:
        print("No errors recorded since the last Talon startup marker.")


def main() -> None:
    args = parse_args()
    log_path: Path = args.log_path
    if not log_path.exists():
        raise SystemExit(f"Log file not found: {log_path}")

    start_offset = find_last_start_offset(log_path)
    if start_offset is None:
        raise SystemExit(
            "Could not find a 'Talon Version:' startup marker in the log. "
            "Run Talon once, then re-run this script."
        )

    errors = collect_error_blocks(log_path, start_offset)
    print_errors(errors)


if __name__ == "__main__":
    main()
