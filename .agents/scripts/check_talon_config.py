#!/usr/bin/env python3
"""Run repository gates for Talon config maintenance."""

from __future__ import annotations

import argparse
import importlib.util
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "stored_state"}
TEXT_SUFFIXES = {".talon", ".talon-list", ".md", ".yaml", ".yml", ".toml", ".sh"}


def iter_files(*suffixes: str):
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if not suffixes or path.suffix in suffixes:
            yield path


def git_paths(scope: str) -> list[Path] | None:
    if scope == "all":
        return None
    command = ["git", "diff", "--name-only"]
    if scope == "staged":
        command.insert(2, "--cached")
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        print(result.stderr, file=sys.stderr)
        return []
    paths = []
    for line in result.stdout.splitlines():
        path = ROOT / line
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            paths.append(path)
    return paths


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def check_skill_docs() -> int:
    skills_root = ROOT / ".agents" / "skills"
    if not skills_root.is_dir():
        return fail("missing .agents/skills")
    nested = skills_root / "skills"
    if nested.exists():
        return fail("skills must live directly under .agents/skills, not .agents/skills/skills")
    status = 0
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            print(f"FAIL: {skill_dir.relative_to(ROOT)} is missing SKILL.md", file=sys.stderr)
            status = 1
            continue
        text = skill_file.read_text(encoding="utf-8")
        expected_name = f"name: {skill_dir.name}"
        checks = {
            expected_name: expected_name in text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else False,
            "description:": "description:" in text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else False,
            "## When to Use": any(line.strip() == "## When to Use" for line in text.splitlines()),
        }
        for label, ok in checks.items():
            if not ok:
                print(f"FAIL: {skill_file.relative_to(ROOT)} missing {label}", file=sys.stderr)
                status = 1
    return status


def compile_python() -> int:
    status = 0
    for path in sorted(iter_files(".py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as error:
            print(f"FAIL: {path.relative_to(ROOT)}: {error.msg}", file=sys.stderr)
            status = 1
    return status


def lint_repository_text(scope: str) -> int:
    status = 0
    paths = git_paths(scope)
    if paths is None:
        paths = list(iter_files(*TEXT_SUFFIXES))
    if not paths:
        print(f"SKIP: no {scope} text files")
        return 0
    for path in sorted(paths):
        data = path.read_bytes()
        relative = path.relative_to(ROOT)
        if b"\x00" in data:
            print(f"FAIL: {relative} contains NUL bytes", file=sys.stderr)
            status = 1
        text = data.decode("utf-8", errors="replace")
        if "<<<<<<<" in text or "=======" in text or ">>>>>>>" in text:
            print(f"FAIL: {relative} contains merge conflict markers", file=sys.stderr)
            status = 1
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                print(f"FAIL: {relative}:{line_number} has trailing whitespace", file=sys.stderr)
                status = 1
    return status


def run_pytest() -> int:
    if not (ROOT / "test").is_dir():
        print("SKIP: no test/ directory")
        return 0
    if importlib.util.find_spec("pytest") is None:
        print("SKIP: pytest is not installed")
        return 0
    if shutil.which("python3") is None:
        return fail("python3 not found")
    return subprocess.run(["python3", "-m", "pytest", "test/"], cwd=ROOT).returncode


def check_recent_talon_errors() -> int:
    script = ROOT / ".agents" / "skills" / "talon-startup-error-troubleshooter" / "scripts" / "scan_and_triage.py"
    if not script.exists():
        return fail(f"missing {script.relative_to(ROOT)}")
    return subprocess.run(["python3", str(script.relative_to(ROOT)), "--since-last-file-change"], cwd=ROOT).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-tests", action="store_true", help="skip pytest gate")
    parser.add_argument("--scope", choices=("changed", "staged", "all"), default="changed", help="text lint scope")
    parser.add_argument("--talon-errors", action="store_true", help="also scan recent Talon reload/startup errors")
    args = parser.parse_args()

    gates = [
        ("skill docs", check_skill_docs),
        ("text lint", lambda: lint_repository_text(args.scope)),
        ("python compile", compile_python),
    ]
    if not args.skip_tests:
        gates.append(("pytest", run_pytest))
    if args.talon_errors:
        gates.append(("recent Talon errors", check_recent_talon_errors))

    status = 0
    for name, gate in gates:
        print(f"==> {name}")
        result = gate()
        if result:
            status = result
    return status


if __name__ == "__main__":
    raise SystemExit(main())
