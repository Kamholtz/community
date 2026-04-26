#!/usr/bin/env python3
"""Run Talon startup-error scan and print a triage summary."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

EXC_RE = re.compile(r"^(?P<exc>[A-Za-z_][A-Za-z0-9_.]*)(?::\s*(?P<msg>.*))?$")
IN_SCRIPT_RE = re.compile(r"^\s*in script at (?P<path>.+?):(?P<line>\d+):")
FRAME_RE = re.compile(r"(?P<path>(?:[A-Za-z]:)?[^\s|:]+(?:[\\/][^\s|:]+)*):(?P<line>\d+)\|")


@dataclass
class ErrorBlock:
    summary_line: str
    lines: list[str]


@dataclass
class Triage:
    exception_line: str
    frame: str
    checks: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Talon startup scan and summarize likely first troubleshooting steps.",
    )
    parser.add_argument(
        "--log-path",
        type=Path,
        default=None,
        help="Optional path to talon.log (defaults to ~/.talon/talon.log).",
    )
    parser.add_argument(
        "--show-raw",
        action="store_true",
        help="Also print raw error blocks from the scanner output.",
    )
    return parser.parse_args()


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "my-config/scripts/talon_errors_since_startup.py").exists():
            return parent
    raise SystemExit("Could not locate repo root containing my-config/scripts/")


def run_scanner(scanner_path: Path, log_path: Path | None) -> str:
    cmd = [sys.executable, str(scanner_path)]
    if log_path is not None:
        cmd.extend(["--log-path", str(log_path)])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        if proc.stdout.strip():
            print(proc.stdout.rstrip())
        if proc.stderr.strip():
            print(proc.stderr.rstrip(), file=sys.stderr)
        raise SystemExit(proc.returncode)
    return proc.stdout


def parse_blocks(raw: str) -> list[ErrorBlock]:
    blocks: list[ErrorBlock] = []
    current_summary: str | None = None
    current_lines: list[str] = []
    for line in raw.splitlines():
        if line.startswith("TALON-ERROR: "):
            if current_summary is not None:
                blocks.append(ErrorBlock(summary_line=current_summary, lines=current_lines))
            current_summary = line
            current_lines = []
            continue
        if current_summary is not None:
            current_lines.append(line)
    if current_summary is not None:
        blocks.append(ErrorBlock(summary_line=current_summary, lines=current_lines))
    return blocks


def detect_exception_line(lines: list[str]) -> str:
    for line in reversed(lines):
        candidate = line.strip()
        if not candidate:
            continue
        if EXC_RE.match(candidate):
            return candidate
    return "Unknown exception"


def detect_frame(lines: list[str]) -> str:
    script_frames: list[str] = []
    generic_frames: list[str] = []
    for line in lines:
        stripped = line.strip()
        script_match = IN_SCRIPT_RE.search(stripped)
        if script_match:
            script_frames.append(f"{script_match.group('path')}:{script_match.group('line')}")
            continue
        frame_match = FRAME_RE.search(line)
        if frame_match:
            generic_frames.append(f"{frame_match.group('path')}:{frame_match.group('line')}")
    if script_frames:
        return script_frames[0]
    if generic_frames:
        for frame in generic_frames:
            normalized = frame.replace("\\", "/")
            if "/.talon/user/" in normalized or normalized.startswith("user/"):
                return frame
        return generic_frames[0]
    return "No actionable stack frame found"


def checks_for_exception(exception_line: str) -> list[str]:
    exc_type = exception_line.split(":", 1)[0].strip()
    mapping = {
        "ModuleNotFoundError": [
            "Verify package is installed in Talon's Python environment.",
            "Check import module name and local file/module shadowing.",
        ],
        "ImportError": [
            "Verify symbol exists in the imported module.",
            "Check for circular imports and stale renamed modules.",
        ],
        "AttributeError": [
            "Confirm object type at failing line matches expected API.",
            "Check for renamed attributes/functions after refactors.",
        ],
        "KeyError": [
            "Verify key exists in the config/list/dict at runtime.",
            "Check input normalization and default/fallback logic.",
        ],
        "ValueError": [
            "Validate assumptions about parsed values and ranges.",
            "Check CSV/settings entries consumed at startup.",
        ],
        "SyntaxError": [
            "Open the reported file/line and fix syntax first.",
            "Re-run scan before attempting deeper debugging.",
        ],
        "IndentationError": [
            "Fix indentation at the exact line reported.",
            "Re-run scan before any semantic debugging.",
        ],
        "RuntimeError": [
            "Inspect raising condition and required runtime preconditions.",
            "Confirm context activation/app state/external process requirements.",
        ],
    }
    return mapping.get(
        exc_type,
        [
            "Open the top actionable user-code frame from the traceback.",
            "Form a minimal hypothesis from exception text, patch, and re-run scan.",
        ],
    )


def triage_block(block: ErrorBlock) -> Triage:
    exception_line = detect_exception_line(block.lines)
    return Triage(
        exception_line=exception_line,
        frame=detect_frame(block.lines),
        checks=checks_for_exception(exception_line),
    )


def print_summary(blocks: list[ErrorBlock], show_raw: bool) -> None:
    if not blocks:
        print("No startup errors found since the most recent Talon startup marker.")
        return

    print(f"Found {len(blocks)} startup error(s) since the latest Talon startup marker.")
    print()
    for index, block in enumerate(blocks, start=1):
        triage = triage_block(block)
        print(f"{index}. {block.summary_line}")
        print(f"   Exception: {triage.exception_line}")
        print(f"   Stack frame: {triage.frame}")
        print("   First checks:")
        for check in triage.checks:
            print(f"   - {check}")
        if show_raw:
            print("   Raw block:")
            for line in block.lines:
                print(f"   {line}")
        print()


def main() -> None:
    args = parse_args()
    repo_root = find_repo_root()
    scanner_path = repo_root / "my-config/scripts/talon_errors_since_startup.py"
    raw_output = run_scanner(scanner_path, args.log_path)
    if "No errors recorded since the last Talon startup marker." in raw_output:
        print("No startup errors found since the most recent Talon startup marker.")
        return
    blocks = parse_blocks(raw_output)
    print_summary(blocks, args.show_raw)


if __name__ == "__main__":
    main()
