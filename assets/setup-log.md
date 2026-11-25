# Lean harness setup log

Keep this file short. Write results and decisions, not tool output.

## Settings
- Guide path: <absolute path of the directory that contains SETUP.md>
- Vault path: <path, or "not set">
- Plan and billing notes: <for example: Fable consent given, or refused>

## Prerequisites
| Tool | Result |
| --- | --- |
| git | |
| Node.js (optional, for Beads) | |
| uv | |
| python3 | |
| curl | |
| Claude Code (2.1.331 or later) | |
| Homebrew (optional, for Beads) | |
| `bashOutputMaxChars`, `BASH_MAX_OUTPUT_LENGTH` (B2) | |

## Tools

| Phase | Item | Found in phase 1 | Status | Notes |
| --- | --- | --- | --- | --- |
| 1 | A2 user-level MCP servers and plugins | n/a | open | <local MCP servers of other projects> |
| 1 | A1 `~/.claude/CLAUDE.md`, skill descriptions, rules | | open | |
| 1 | D model, advisor, subagents, global gitignore | | open | |
| 2 | handoff | | open | |
| 2 | ponytail skill (D2) | | open | |
| 2 | Beads CLI | | open | |
| 2 | prompt-improver | | open | |
| 2 | B1, B2 quiet commands and output limit (user level) | n/a | open | |
| 2 | MarkItDown | | open | |
| 2 | Graphify CLI | | open | |
| 2 | XERJ | | open | |
| 3 | second brain | | open | |
| 3 | Basic Memory | | open | |
| 4 | check and report | n/a | open | |

Status values: open, waiting for the user, done, refused by the user, removed (rule 11).

## After restart

- <the checks of the last phase that need a new session>

## Onboarded projects

| Date | Project path | Done | Skipped |
| --- | --- | --- | --- |

## Approvals and refusals

- <date>: <what the user approved or refused; for an MCP server, the command that undoes it>

## Next action

<one action: the phase, or what is necessary from the user>
