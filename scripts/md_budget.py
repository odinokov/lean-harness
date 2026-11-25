#!/usr/bin/env python3
"""Measure the always-loaded md files of a Claude Code project (section A1).

Limits:
  project CLAUDE.md (with CLAUDE.local.md)   max 60 lines
  ~/.claude/CLAUDE.md                        max 40 lines
  CLAUDE.md files in parent directories      counted in the total
  rules without a `paths` field              0 files
  all always-loaded files together           max 100 lines
  @import lines                              0

Usage:
  python3 md_budget.py [--project DIR] [--home DIR] [--json]

Exit code: 0 if all limits are satisfied, 1 if one is not, 2 on a usage error.
Standard library only. The script reads files and changes nothing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LIMIT_PROJECT = 60
LIMIT_USER = 40
LIMIT_TOTAL = 100
MAX_IMPORT_DEPTH = 5

# A token such as @docs/api.md or @~/.claude/extra.md. An e-mail address does
# not match, because a word character comes before its "@".
IMPORT_RE = re.compile(r"(?<![\w`@])@(~?[\w.\-]*[/.][\w./\-]*)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
CODE_SPAN_RE = re.compile(r"`[^`]*`")


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def find_imports(path: Path, home: Path) -> tuple[list[tuple[int, str, Path]], list[tuple[int, str]]]:
    """Return (imports that resolve to a file, tokens that look like imports but do not)."""
    real, unresolved = [], []
    in_fence = False
    for number, line in enumerate(read_lines(path), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in IMPORT_RE.finditer(CODE_SPAN_RE.sub("", line)):
            token = match.group(1).rstrip(".,;:)")
            if token.startswith("~"):
                target = home / token[1:].lstrip("/")
            elif token.startswith("/"):
                target = Path(token)
            else:
                target = path.parent / token
            if target.is_file():
                real.append((number, token, target))
            else:
                unresolved.append((number, token))
    return real, unresolved


def is_pattern(value: str) -> bool:
    """A quoted non-empty string, or an unquoted value that YAML reads as a plain string."""
    value = value.strip()
    if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
        inner = value[1:-1].strip()
        return bool(inner) and value[0] not in inner
    return bool(value) and value.lower() not in ("null", "~", "{}", "[]") and value[0] not in "*&!%@`{[" and ": " not in value


def has_paths_field(path: Path) -> bool:
    """True only for a closed header whose `paths` names a pattern; every other case counts as always loaded. A heuristic, not a YAML parser."""
    lines = read_lines(path)
    if not lines or lines[0].strip() != "---":
        return False
    end = next((i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if end is None:
        return False
    block = lines[1:end]
    for number, line in enumerate(block):
        match = re.match(r"^paths\s*:(.*)$", line)
        if not match:
            continue
        value = re.sub(r"(^|\s)#.*$", "", match.group(1)).strip()
        if value.startswith("[") and "]" not in value:
            for more in block[number + 1 :]:
                value += " " + re.sub(r"(^|\s)#.*$", "", more).strip()
                if "]" in more:
                    break
            else:
                return False
        if value.startswith("[") and value.endswith("]"):
            items = [i for i in value[1:-1].split(",") if i.strip()]
            return bool(items) and all(map(is_pattern, items))
        if value:
            return is_pattern(value)
        items = []
        for item in block[number + 1 :]:
            text = item.strip()
            if not text or text.startswith("#"):
                continue
            if not re.match(r"-(\s|$)", text):
                break
            items.append(re.sub(r"(^|\s)#.*$", "", text[1:]))
        return bool(items) and all(map(is_pattern, items))
    return False


def collect(project: Path, home: Path) -> dict:
    files = []  # each: path, role, lines
    imports = []  # each: file, line, token
    warnings = []
    seen: set[Path] = set()

    def add(path: Path, role: str, depth: int = 0) -> None:
        resolved = path.resolve()
        if resolved in seen or not path.is_file():
            return
        seen.add(resolved)
        files.append({"path": str(path), "role": role, "lines": len(read_lines(path))})
        real, unresolved = find_imports(path, home)
        for number, token in unresolved:
            warnings.append(f"{path}:{number}: '@{token}' looks like an import, but the file was not found")
        for number, token, target in real:
            imports.append({"file": str(path), "line": number, "token": "@" + token})
            if depth < MAX_IMPORT_DEPTH:
                add(target, "imported", depth + 1)

    for candidate in (project / "CLAUDE.md", project / ".claude" / "CLAUDE.md", project / "CLAUDE.local.md"):
        add(candidate, "project")
    add(home / ".claude" / "CLAUDE.md", "user")
    for parent in project.resolve().parents[:-1]:
        for name in ("CLAUDE.md", "CLAUDE.local.md"):
            add(parent / name, "parent directory")

    rules_without_paths = []
    for rules_dir in (project / ".claude" / "rules", home / ".claude" / "rules"):
        if not rules_dir.is_dir():
            continue
        for rule in sorted(rules_dir.rglob("*.md")):
            if not has_paths_field(rule):
                rules_without_paths.append(str(rule))
                add(rule, "rule without paths")

    project_lines = sum(f["lines"] for f in files if f["role"] == "project")
    user_lines = sum(f["lines"] for f in files if f["role"] == "user")
    total_lines = sum(f["lines"] for f in files)
    checks = [
        {"name": "project CLAUDE.md lines", "value": project_lines, "limit": LIMIT_PROJECT,
         "ok": project_lines <= LIMIT_PROJECT},
        {"name": "~/.claude/CLAUDE.md lines", "value": user_lines, "limit": LIMIT_USER,
         "ok": user_lines <= LIMIT_USER},
        {"name": "rules without paths", "value": len(rules_without_paths), "limit": 0,
         "ok": not rules_without_paths},
        {"name": "@import lines", "value": len(imports), "limit": 0, "ok": not imports},
        {"name": "all always-loaded lines", "value": total_lines, "limit": LIMIT_TOTAL,
         "ok": total_lines <= LIMIT_TOTAL},
    ]
    if not any(f["role"] == "project" for f in files):
        warnings.append(f"no CLAUDE.md found in {project}")
    return {
        "ok": all(c["ok"] for c in checks),
        "checks": checks,
        "files": files,
        "imports": imports,
        "rules_without_paths": rules_without_paths,
        "warnings": warnings,
    }


def print_report(report: dict) -> None:
    print("Always-loaded md files")
    for f in report["files"]:
        print(f"  {f['lines']:5d}  {f['role']:<19} {f['path']}")
    if not report["files"]:
        print("  (none)")
    print()
    print("Limits")
    for c in report["checks"]:
        mark = "ok  " if c["ok"] else "OVER"
        print(f"  {mark}  {c['name']:<26} {c['value']:>4} / {c['limit']}")
    if report["imports"]:
        print()
        print("@import lines (replace each with the path without '@')")
        for i in report["imports"]:
            print(f"  {i['file']}:{i['line']}  {i['token']}")
    if report["warnings"]:
        print()
        print("Warnings")
        for w in report["warnings"]:
            print(f"  {w}")
    print()
    print("Result:", "all limits are satisfied" if report["ok"] else "one or more limits are not satisfied")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--project", default=".", help="project root (default: current directory)")
    parser.add_argument("--home", default=str(Path.home()), help="home directory (default: your home)")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args()

    project = Path(args.project)
    if not project.is_dir():
        print(f"error: {project} is not a directory", file=sys.stderr)
        return 2
    report = collect(project, Path(args.home))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
