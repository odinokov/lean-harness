# Overlaps and licenses

## Overlaps

| Tools | Division of work |
| --- | --- |
| Quiet commands and subagents | A quiet command keeps short output small in the main session (B1). A test run, a log or a dump that you need only as a summary goes to `test-runner` or `log-digester` (section D) |
| The saved output of Claude Code and subagents | A successful result above the output limit becomes a file (B2). Search it, or read parts of it, when you use it more than one time. If a summary is sufficient, give the path to `log-digester` |
| Graphify and XERJ | Graphify gives structure and relations. XERJ gives passages |
| Second brain, auto memory, `bd remember` | Use the functions in section F. `brain-writer` writes decisions to the vault. Section F2 covers auto memory. |
| XERJ and Basic Memory | XERJ searches the code repository. Basic Memory searches the vault project folder. Do not index the vault with XERJ or the repository with Basic Memory |
| Beads and the built-in task list | Beads keeps tasks between sessions. The built-in list keeps them in one session |
| handoff and `/compact` | handoff gives explicit next steps. `/compact` is for work in the same session |
| Text at the start of a session from Beads and the vault | The sources use one budget (section F2) |
| A skill and the system prompt of a subagent | The system prompt has priority |
| The ponytail skill and the main session | Only `implementer` preloads the skill (D2). The CLAUDE.md line keeps the main session from loading it. The guide does not use the plugin |
| prompt-improver nudges, CLAUDE.md and the system prompt of a subagent | CLAUDE.md and the system prompt have priority. Section E4 gives the rule for each nudge |
| Hooks of prompt-improver | The hooks only add text. No hook that this guide installs changes a tool call. Plugin hooks also operate in subagents |

Tell the user about these licenses before an installation in a commercial project:

- XERJ: the engine has Apache-2.0, and the release binaries since rc.101 include proprietary Query-1 crates;
- Basic Memory: AGPL-3.0-or-later.

Earlier versions of this guide also named Context Mode (Elastic License 2.0) and RTK (the engine and the proxy daemon have BUSL-1.1). This version does not install them.
