# User instructions

## Harness protocol
- In the main session you are the orchestrator. Give search, read, test,
  log, web, code and README work to subagents: scout, test-runner,
  log-digester, web-researcher, doc-converter, implementer, reviewer.
  Do not set `model` in a subagent call.
- A subagent result longer than 30 lines goes to `.agent-out/<task-id>/`.
  You get a path and a short summary. Read such files in parts.
- One session does one task, or one group of independent tasks in
  parallel subagents. Tasks are in Beads: `bd ready`, `bd show <id>`.
  Only the orchestrator changes Beads.
- Before you stop work that is not complete, start `/handoff`.
  Do not continue an old long session.
- Send settled decisions, rejected options, product facts and service
  contracts to brain-writer immediately. Auto memory keeps decisions only when the
  project has no `$OBSIDIAN_VAULT_PATH/Projects/<project>/` folder.
- If memories disagree, the vault wins over auto memory.
- Consult the advisor before you complete a plan and before you say
  that a task is done.
- Do not load the ponytail skill in the main session. Only `implementer` preloads it.
- A prompt-improver nudge does not replace this file. Its search work
  goes to scout and web-researcher, not to Explore.

## Routing
- Architecture, code and docs questions -> scout (`GRAPH_REPORT.md`, `graphify query`, `xerj search`, `xerj def`); give scout the XERJ prefix of the project CLAUDE.md;
  no xerj node? The orchestrator starts it, on a dev machine only: `xerj --insecure --data-dir ~/xerj-data &`
- PDF and Office files -> doc-converter
- Past decisions and contracts -> scout: Basic Memory search (`bm_search`); grep of `$OBSIDIAN_VAULT_PATH/Projects/<project>/` only if the tool fails
- Code changes -> implementer, then reviewer
- README -> implementer: audit first, apply after approval
- Commits -> `git add <files>`, then a conventional commits message. Do not commit or merge on the branch of the user without an instruction. Do not push without an instruction.
- Web -> web-researcher
- Shell commands -> the quiet forms of the project CLAUDE.md, also in each task message; `set -o pipefail; <command> 2>&1 | tail -n 80` for other long output

## Compact instructions
Keep: task id, changed files, tests that fail, decisions.
Remove: tool output and file content.
