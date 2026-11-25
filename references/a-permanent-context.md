# A. Permanent context

Claude Code loads the permanent context into each session before the first message, and each request pays for it. For this reason, decrease it first, before you install tools.

## A1. Diet for md files (item 3)

Claude Code loads these items into each session:

- All levels of CLAUDE.md: managed, `~/.claude/CLAUDE.md`, `./CLAUDE.md` or `./.claude/CLAUDE.md`, and `./CLAUDE.local.md`, and the `CLAUDE.md` and `CLAUDE.local.md` files of each parent directory of the project. Claude Code adds the files together. One file does not replace a different file.
- All files that an `@import` line names. Imports put the text in order, but they do not decrease its cost.
- The files in `.claude/rules/` and `~/.claude/rules/` that have no `paths` field.
- Auto memory: the first 200 lines or 25 KB of `MEMORY.md`.
- The descriptions of skills (a maximum of 1,536 characters for each skill), the names of MCP tools, and the output of SessionStart hooks.

The limits in this guide are smaller than the limit in the documentation, which is 200 lines for each file:

- the project CLAUDE.md: a maximum of 60 lines;
- `~/.claude/CLAUDE.md`: a maximum of 40 lines, because it holds the harness protocol and the routing;
- rules without `paths`: zero;
- all these files together: a maximum of 100 lines.

Write these files in English. Cyrillic text usually uses more tokens for the same content.

| Content | New location | When Claude Code loads it |
| --- | --- | --- |
| Build and test commands, 5 to 10 invariants, the routing table | CLAUDE.md | always |
| Procedures with many steps: release, migration, review | a skill: `.claude/skills/<name>/SKILL.md` | when the skill starts |
| Rules for one part of the code base | `.claude/rules/<name>.md` with `paths:` | when you read a file that matches |
| Reference material: architecture, API | `docs/…`; write the path without `@` | when you read the file |
| Instructions for a role | a subagent: `.claude/agents/<name>.md` | only in the context of the subagent |
| Facts, decisions, contracts | the second brain (section F) | on request |
| Tasks and their status | Beads (section E) | on request |
| Actions that must always occur, for example before a commit | a hook | the harness does them, not the model |

Procedure:

1. Ask the user to run `/memory`. Write the list of loaded files in the setup log.
2. For each paragraph of CLAUDE.md, make a decision: is it necessary in each session? If it is not, move it as the table shows.
3. Delete the content that you can get from the code: the directory tree, the list of the stack, a summary of the README.
4. Replace each `@import` with the path of the file without `@`.
5. Add `paths` to each file in `.claude/rules/`, or move its text into CLAUDE.md.
6. Decrease each skill description to one or two lines. Put the primary trigger first.
7. Add `disable-model-invocation: true` to the skills that only the user starts. Then their descriptions do not go into the context. Do not add it to a skill that you start (handoff, graphify, prompt-improver). Such a skill keeps its description in the main session. Do not add it to `ponytail` either: the field blocks the preload into `implementer` (D2).
8. Keep auto memory on. It holds preferences and feedback. Section F2 says when it also keeps decisions.
9. Ask the user for the recommendations in `/usage`. A line such as `Trim …/CLAUDE.md` shows a file with a high cost.

Do this check again after each tool that you install in Part 1:

- Compare `~/.claude/CLAUDE.md` and `~/.claude/settings.json` with the copies from rule 10. In a project, use `git diff` to examine CLAUDE.md, `AGENTS.md` and `.claude/settings.json`. If these files are gitignored, make a marker file before the tool runs and list the new files with `find . -newer <marker> -type f -not -path './.git/objects/*'`.
- If the tool added text to these files, decrease the text to one routing line or move it into a skill.

Do not add this guide to CLAUDE.md and do not import it. Rule 4 tells you which parts to read in each session.

## A2. Disable unnecessary MCP servers (item 11)

The main session keeps only the MCP servers that most tasks use. All other tools operate as CLI commands or stay in a subagent.

1. Ask the user to run `/mcp`. Run `claude mcp list`. Write the list of servers in the setup log.
2. For each server, select one of three decisions:
    - A CLI is available (`gh`, `aws`, `gcloud`, `markitdown`, `xerj`, `bd`): use the CLI. Remove the server only after the CLI operates.
    - Only one role uses the server: put its definition inline in the `mcpServers` field of that subagent. Then the server connects only while the subagent operates, and its tools do not go into the main context. A server with a key stays where it is (rule 8).
    - Most tasks use the server: keep it.
3. To remove a server, run `claude mcp remove <name> -s user` (user scope) or `claude mcp remove <name> -s local` (project-local scope). To deactivate a server in all projects, for example a claude.ai connector or a plugin server, add `{"serverName": "<name>"}` to `deniedMcpServers` in `~/.claude/settings.json`. A plugin server name has the form `plugin:<plugin>:<server>`. Take the name from `claude mcp list`, and run `claude mcp list` again to verify that the server is gone. `/mcp` deactivates a server only in the current project. `"disableClaudeAiConnectors": true` deactivates all claude.ai connectors. Rule 7 applies.
4. Note: Claude Code defers MCP tool definitions by default, but the tool names and the server instructions stay in the context.
5. Plugins. A plugin can add skill descriptions, hooks and text at the start of a session (section A1). Run `claude plugin list`. For each enabled plugin that this guide does not install, write in the setup log: its version, its scope, its hook events and the count of its skills and commands. The plugin folder is `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`. It can have `skills/` and `commands/`. Its hooks are in `hooks/hooks.json`, or under the `hooks` key of `.claude-plugin/plugin.json`. That key can name another file. Write "none" for a part that the plugin does not have. Take the version and the scope from `claude plugin list`, because the cache can keep old versions. A SessionStart hook adds text to each session. You cannot add `disable-model-invocation` to a skill of a plugin, because an update replaces the plugin files. For each plugin, recommend one decision to the user: keep it if most sessions use it, or disable it. The user decides. To disable a plugin, run `claude plugin disable <plugin>@<marketplace> -s <scope>`. Rule 7 applies. This step does not apply to the plugins that this guide installs: prompt-improver and the second-brain plugin. `claude plugin details <plugin>@<marketplace>` shows the components of a plugin and its projected token cost.

At the end of this setup, the main session keeps the servers that most tasks use (step 2). The MCP server `basic-memory` (section F3) stays on: it adds about 480 tokens of instructions to each session, and its tools that are not read-only are in `permissions.deny`. The second-brain plugin also has an MCP server for the vault, but this design does not use it. Deactivate it as step 3 tells. Then make sure that the plugin commands that you use continue to operate.
