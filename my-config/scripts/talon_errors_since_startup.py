#!/usr/bin/env python3
"""Extract Talon log errors recorded after the most recent startup."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

START_MARKER = "Talon Version:"
LOG_ENTRY_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+(?P<level>[A-Z]+)"
)
IN_SCRIPT_RE = re.compile(r"^\s*in script at (?P<path>.+?):(?P<line>\d+):")
STACK_FRAME_RE = re.compile(
    r"(?P<path>(?:[A-Za-z]:)?[^\s|:]+(?:[\\/][^\s|:]+)*):(?P<line>\d+)\|"
)
EXCEPTION_MESSAGE_RE = re.compile(r"^(?P<type>[A-Za-z][A-Za-z0-9_.]+):\s*(?P<message>.*)$")
TALON_HOME = Path.home() / ".talon"
DEFAULT_LOG_FILE = TALON_HOME / "talon.log"
USER_ROOT = TALON_HOME / "user"


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


@dataclass
class ProblemSummary:
    path: Path | None
    line: int | None
    message: str


def normalize_path(raw_path: str | None) -> Path | None:
    """Interpret a raw Talon log path as an absolute Path when possible."""
    if not raw_path:
        return None
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    base = TALON_HOME if raw_path.startswith(("talon/", "user/")) else Path.cwd()
    return (base / raw_path).resolve(strict=False)


def is_user_path(path: Path | None) -> bool:
    if not path:
        return False
    try:
        path.relative_to(USER_ROOT)
        return True
    except ValueError:
        return False


def find_error_location(lines: list[str]) -> tuple[str | None, int | None]:
    """Pick a file/line pair from a Talon error block."""
    for line in lines:
        stripped = line.strip()
        match = IN_SCRIPT_RE.search(stripped)
        if match:
            return match.group("path").strip(), int(match.group("line"))
    stack_candidates: list[tuple[str, int]] = []
    for line in lines:
        match = STACK_FRAME_RE.search(line)
        if match:
            stack_candidates.append((match.group("path").strip(), int(match.group("line"))))
    if not stack_candidates:
        return None, None
    for raw_path, raw_line in stack_candidates:
        normalized = normalize_path(raw_path)
        if is_user_path(normalized):
            return raw_path, raw_line
    return stack_candidates[0]


def extract_error_message(lines: list[str]) -> str:
    """Derive a short message for the error summary."""
    fallback: str | None = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        exc_match = EXCEPTION_MESSAGE_RE.match(stripped)
        if exc_match:
            exc_type = exc_match.group("type")
            exc_message = exc_match.group("message").strip()
            if exc_message:
                return f"{exc_type}: {exc_message}"
            return exc_type
        log_match = LOG_ENTRY_RE.match(line)
        if log_match and log_match.group("level") == "ERROR":
            rest = line[log_match.end():].strip()
            if rest and "|" not in rest:
                return rest
        if fallback is None and "|" not in line:
            fallback = stripped
    return fallback or "Unknown Talon error"


def summarize_error_block(block: str) -> ProblemSummary:
    lines = block.splitlines()
    raw_path, raw_line = find_error_location(lines)
    summary_path = normalize_path(raw_path) or DEFAULT_LOG_FILE
    summary_line = raw_line if raw_line is not None else 1
    return ProblemSummary(
        path=summary_path,
        line=summary_line,
        message=extract_error_message(lines),
    )


def format_summary_line(summary: ProblemSummary) -> str:
    path = summary.path or DEFAULT_LOG_FILE
    line = summary.line or 1
    return f"TALON-ERROR: {path}:{line}: {summary.message}"


def print_errors(errors: Iterable[str]) -> None:
    printed = False
    for block in errors:
        summary = summarize_error_block(block)
        print(format_summary_line(summary))
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
