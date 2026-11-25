"""Cases of the `paths` heuristic of md_budget.py.
The heuristic is not a YAML parser: a rule without a readable `paths` counts as always loaded.
The known gaps are listed at the end of this file.
Run from the repo root: python3 scripts/test_md_budget.py (exit 0 when all cases pass)."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_budget import has_paths_field  # noqa: E402


def rule(*lines: str) -> str:
    return "\n".join(["---", *lines, "---", "body", ""])


CASES = [
    ("block list, one quoted pattern", rule("paths:", '  - "src/**"'), True),
    ("block list, two quoted patterns", rule("paths:", '  - "src/**"', '  - "lib/**"'), True),
    ("brace pattern in quotes", rule("paths:", '  - "src/**/*.{ts,tsx}"'), True),
    ("inline list of quoted patterns", rule('paths: ["src/**", "lib/**"]'), True),
    ("inline list, one pattern", rule('paths: ["**/*.ts"]'), True),
    ("comma string in quotes", rule('paths: "src/**, lib/**"'), True),
    ("unquoted comma string", rule("paths: src/**, lib/**"), True),
    ("unquoted single pattern", rule("paths: src/**"), True),
    ("single quotes", rule("paths: 'src/**'"), True),
    ("braces in quotes", rule('paths: "{src,lib}/**"'), True),
    ("comment between key and item", rule("paths:", "  # note", '  - "src/**"'), True),
    ("hash inside quotes", rule("paths:", '  - "src/#x/**"'), True),
    ("flow list over several lines", rule("paths: [", '  "src/**",', '  "lib/**"', "]"), True),
    ("flow list over several lines with comment", rule("paths: [", '  "src/**", # a', '  "lib/**"', "]"), True),
    ("no header", "body\n", False),
    ("unclosed header with pattern", "---\npaths:\n  - \"src/**\"\nbody\n", False),
    ("empty paths, no items", rule("paths:"), False),
    ("empty list", rule("paths: []"), False),
    ("null", rule("paths: null"), False),
    ("tilde", rule("paths: ~"), False),
    ("empty map", rule("paths: {}"), False),
    ("Null", rule("paths: Null"), False),
    ("other key only", rule("description: x"), False),
    ("paths then next key", rule("paths:", "description: x"), False),
    ("paths indented under another key", rule("meta:", '  paths: "src/**"'), False),
    ("only item is empty string", rule("paths:", '  - ""'), False),
    ("unquoted star pattern", rule("paths: **/*.ts"), False),
    ("unquoted star item", rule("paths:", "  - **/*.ts"), False),
    ("inline list, unquoted star", rule("paths: [**/*.ts]"), False),
    ("quoted then unquoted item", rule("paths:", '  - "src/**"', "  - **/*.ts"), False),
    ("unquoted then quoted item", rule("paths:", "  - **/*.ts", '  - "src/**"'), False),
    ("quoted item then empty item", rule("paths:", '  - "src/**"', '  - ""'), False),
    ("unquoted braces", rule("paths: {src,lib}/**"), False),
    ("unclosed [ and header ends", rule('paths: ["src/**"'), False),
    ("two quoted strings", rule('paths: "a", "b"'), False),
    ("mapping value", rule("paths: a: b"), False),
    ("flow list never closes", rule("paths: [", '  "src/**",', '  "lib/**"'), False),
    ("flow list with unquoted star element", rule("paths: [", '  "src/**",', "  **/*.ts", "]"), False),
]


def main() -> int:
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, text, expected in CASES:
            path = Path(tmp) / "rule.md"
            path.write_text(text, encoding="utf-8")
            got = has_paths_field(path)
            if got != expected:
                failed += 1
                print(f"FAIL {name}: expected {expected}, got {got}")
    print(f"{len(CASES) - failed} of {len(CASES)} cases passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

# Known gaps: the heuristic counts these as a pattern, but PyYAML 6.0.2 cannot read the header.
# - an unclosed quote: paths: "src/**
# - text after a closing quote: paths: "a" b
# - a value that starts with `,`, `]` or `|`
# Known false alarms, on the safe side: in a bracket list over several lines, a `]` inside
# a quoted pattern or inside a comment ends the list early, so the rule counts as always loaded.
