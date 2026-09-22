#!/usr/bin/env python3
"""Sort vocabulary entries, preserving headers, then commit them."""

from __future__ import annotations

import csv
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
PATHS = [":(glob)**/*.talon-list", "settings/words_to_replace.csv"]


def sort_contents(content: str, *, is_csv: bool) -> str:
    """Preserve line endings, headings, blank lines and comment positions."""
    lines = content.splitlines(keepends=True)
    if not lines:
        return content
    if is_csv:
        # Keep quoted multiline CSV records together, retaining their raw text.
        records = []
        previous = 0
        for row in (reader := csv.reader(lines, strict=True)):
            records.append((row, "".join(lines[previous:reader.line_num])))
            previous = reader.line_num
        if not records:
            return content
        header = records[0][1]
        body = records[1:]
        positions = [i for i, (row, _) in enumerate(body) if row]
        ordered = sorted((body[i] for i in positions), key=lambda item: item[0][0].casefold())
        for i, record in zip(positions, ordered):
            body[i] = record
        chunks = [header, *(raw for _, raw in body)]
    else:
        separator = next((i for i, line in enumerate(lines) if line.strip() == "-"), None)
        if separator is None:
            raise ValueError("Talon list has no header separator")
        positions = [i for i in range(separator + 1, len(lines))
                     if lines[i].strip() and not lines[i].lstrip().startswith("#")]
        # Stable sorting preserves precedence for repeated list keys.
        ordered = sorted((lines[i] for i in positions), key=lambda line: line.split(":", 1)[0].strip().casefold())
        for i, line in zip(positions, ordered):
            lines[i] = line
        chunks = lines
    # A final entry without a newline may have moved into the middle.
    newline = "\r\n" if "\r\n" in content else "\n"
    result = "".join(chunk if chunk.endswith(("\n", "\r")) else chunk + newline for chunk in chunks)
    if not content.endswith(("\n", "\r")):
        result = result.removesuffix(newline)
    return result


def main() -> None:
    paths = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", *PATHS],
        cwd=ROOT,
    ).decode("utf-8").split("\0")
    updates = []
    for name in dict.fromkeys(filter(None, paths)):
        path = ROOT / name
        if not path.is_file():
            continue
        raw = path.read_bytes()
        bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
        content = raw[len(bom):].decode("utf-8")
        updated = bom + sort_contents(content, is_csv=path.suffix == ".csv").encode("utf-8")
        if updated != raw:
            updates.append((path, updated))
    for path, updated in updates:
        path.write_bytes(updated)
        print(f"Sorted {path.relative_to(ROOT)}", flush=True)
    subprocess.run(["git", "add", "--", *PATHS], cwd=ROOT, check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet", "--", *PATHS], cwd=ROOT)
    if diff.returncode == 0:
        print("No vocabulary changes to commit.")
        return
    if diff.returncode != 1:
        diff.check_returncode()
    subprocess.run(["git", "commit", "-m", "feat: update *.talon-list", "--", *PATHS], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
