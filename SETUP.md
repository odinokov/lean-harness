# Lean harness: setup guide

You are Claude Code. This guide sets up the Claude Code work environment of the user: the user-level configuration in `~/.claude/` and the CLI tools that all projects use. Follow it step by step. It has 16 methods in 6 classes (`references/ontology.md`).

The guide has two parts:

- Part 1, the environment: four phases, one phase in each session. The user starts Claude Code again between the phases, because Claude Code loads plugins, hooks and `env` only at the start of a session. New skills and subagents can appear during a session, but test them after the restart.
- Part 2, project onboarding: one session for each project that the user wants to prepare.

## How the user starts a session

| Work | Directory | Prompt |
| --- | --- | --- |
| Part 1 | `<guide>` | `Read SETUP.md and do the next phase.` |
| Part 2 | the project root | `Read <guide>/SETUP.md and onboard this project.` |
| Check | any | `Read <guide>/SETUP.md and do the check.` |

`<guide>` is the absolute path of the directory that contains this file. Paths that start with `references/`, `assets/` or `scripts/` are relative to `<guide>`.

The setup keeps its own files outside all projects:

| Path | Content |
| --- | --- |
| `~/.claude/lean-harness/setup-log.md` | the inventory, the status of each tool, the onboarded projects, the approvals and the next action |
| `~/.claude/lean-harness/backup/` | copies of the user configuration (rule 10) and of the project files that a commit does not hold (rule 9) |

Do not copy this guide into a project, do not add it to a CLAUDE.md file and do not import it.

## Session procedure

1. Read `~/.claude/lean-harness/setup-log.md`. If it does not exist and the user asked for a phase, this is the first session: do phase 1. If it does not exist and the user asked for the check or for Part 2, stop. Do not create the log. Tell the user to do phase 1 first: the prompt of Part 1, in `<guide>`.
2. Do the open items in the "After restart" section of the log first. If a check fails, fix it, or write the failure and tell the user. If the user asks for the check (section Check), skip this step. `references/acceptance-check.md` says what the check does with an open item.
3. Do the next phase of Part 1, the onboarding of Part 2 or the check (section Check).
4. Before you change the user configuration, do rule 10.
5. Show the user the plan: the tools, the exact commands and the files that change. Get one approval for the plan. The actions in the list of rule 7 need their own approval.
6. If the setup log shows a tool as installed, do not install it again. Check its version and its configuration, and add only what is missing.
7. If an action needs the user (a built-in command, a key, a decision) and the user did not give it, stop. Tell the user exactly what is necessary. Write "waiting for the user" in the setup log. Do not guess values.
8. Update the setup log: the status of each tool, the approvals and refusals, the "After restart" checks and the next action.
9. Tell the user, in this sequence: the built-in commands to run now, to start Claude Code again, and the exact prompt for the next session. Tell the user to start Claude Code in a new terminal and to start a new conversation, not `claude -c`.

## 0. Rules

Terms:

- Permanent context: the text that Claude Code loads into each session before the first message.
- Permanent weight: the text that one tool adds to the permanent context: MCP tool names, hook output at the start of a session, skill descriptions.
- Main session: the session in which the user gives you work. In this session you are the orchestrator.
- Subagent: an agent with its own context window that the orchestrator starts.
- Vault: the folder of markdown notes of the second brain.
- Setup log: the file `~/.claude/lean-harness/setup-log.md`.

Rules:

1. Do the phases of Part 1 in sequence. Do one phase in one session.
2. Part 2 needs phase 1. Skip the items of Part 2 for tools that are not installed.
3. Start each session from the setup log. End each session with an update of the log.
4. Read only this file, the setup log, the reference sections of the current phase and the templates that its steps name.
5. You cannot run built-in slash commands. Examples are `/context`, `/memory`, `/mcp`, `/model`, `/advisor`, `/plugin`, `/hooks`, `/usage`, `/clear` and `/compact`. Ask the user to run the command and to give you the result. If a shell command does the same work, use it: `claude mcp list`, `claude plugin install`. You can start skills yourself, for example `/handoff` and `/graphify`. If a plugin command does not start, ask the user to run it.
6. Before you install a tool, get the current install command from its README. From phase 2, give this work to the `web-researcher` subagent, because a README can be very long. The quiet forms of B1 are examples that this guide did not test. `references/sources.md` gives the date of each test. For a Python tool, use `uv tool install` (CLI) or `uv run --no-project --with '<package>>=<version>'` (library). In a project with a `pyproject.toml`, uv without `--no-project` writes `.venv` and `uv.lock` into the project. Without a minimum version, uv can reuse an older cached release. Do not use `pip install` in the system Python.
7. Get a separate approval of the user before each of these actions:
    - the run of an install script of the type `curl … | sh`;
    - the addition, removal or deactivation of an MCP server or a plugin;
    - the entry of an API key or a license key, or the creation of an account;
    - the install of a tool from source or from a release binary, outside a package manager;
    - the setup of a tool that sends data to an external service (the usage metrics of Beads);
    - a change to the md files that are in a project now.
8. Keep secrets out of md files, memory and the vault. Use environment variables, or the login or config command of the tool. The user enters each key in an own terminal. When you write an MCP server command or definition in the setup log, write a placeholder in place of each key or token. A server whose definition holds a key, or refers to one with `${VAR}`, stays where it is: do not move it into a subagent file. Tell the user.
9. Before you change the md files of a project, commit the current state of the project. Move content to a new location. Delete only the content that you can get from the code (section A1, step 3). The commit does not hold gitignored files, untracked files, the git hooks (their folder is `git rev-parse --git-path hooks`), `.git/config` and `.git/info/exclude`. Examples are `.claude/settings.local.json`, `.mcp.json` and `.beads/PRIME.md`. Before you change one of them, copy it to `~/.claude/lean-harness/backup/<date>-part2-<project>/`. Rule 10 says what to do when the folder exists. If the folder holds the files of another project with the same name, use a folder with a number at the end.
10. Before each phase, copy each of these items that exists: `~/.claude/settings.json`, `~/.claude/CLAUDE.md`, `~/.claude/agents/`, `~/.claude/rules/`, the global ignore file (`git config --global core.excludesFile`; if it is empty, `~/.config/git/ignore`), and each skill folder that the phase changes to `~/.claude/lean-harness/backup/<date>-phase<N>/`. Do not copy `~/.claude.json` (account data): write the remove command of each MCP server that the phase adds in the setup log. Use the copies to find changes and to remove a tool. If the backup folder exists, it holds the original state: copy only the items that it does not hold, and do not replace an item that it holds. The backup folder can hold keys. Keep it private: `chmod 700 ~/.claude/lean-harness/backup`. Do not commit it and do not share it. `<date>` has the form YYYY-MM-DD.
11. A tool stays only if it operates and the user wants it (`references/overlaps.md` shows the overlaps and the licenses). If the user refuses a tool, skip it. If its verification fails and you cannot fix it, recommend its removal. Remove it after approval. Write the result and the cause in the setup log.
12. Install at user scope: plugins with `--scope user`, MCP servers with `-s user`, skills in `~/.claude/skills/`, subagents in `~/.claude/agents/`, settings in `~/.claude/settings.json`, CLIs with `uv tool install` or `npm install -g`. Only Part 2 changes the files of a project. The one exception to the skill path: `graphify install --project` writes the Graphify skill into `.claude/skills/` of the project (C1, Part 2).
13. A line in `~/.claude/CLAUDE.md` or in a subagent can name only a tool that is installed. Add the line in the phase that installs the tool. If you remove the tool, remove the line. The exception: a sentence that only forbids the use of a tool can stay.

## Part 1. Environment

### Phase 1. Inventory and core configuration

No installs in this phase.

- Read: `references/a-permanent-context.md` and `references/d-delegation.md`.
- Separate approvals (rule 7): each removal or deactivation of an MCP server or a plugin (step 5), and each move of an MCP server into a subagent (step 7).
- Do:
    1. If `~/.claude/lean-harness/setup-log.md` does not exist, copy `assets/setup-log.md` to it. Then write the guide path in "Settings". If the log exists, keep it. Continue this phase from the rows with the status "open".
    2. Run each check and write the result, as a version or "not found": `git --version`, `node --version`, `uv --version`, `python3 --version`, `curl --version`, `claude --version` (2.1.331 or later; `omitClaudeMd` needs 2.1.271 or later), `brew --version`. Homebrew and Node.js are optional: only Beads (E2) uses them, and one of the two is enough. If a required tool is missing or too old, stop and tell the user what to install. If the operating system is not Linux, stop and tell the user.
    3. Take the inventory: `claude plugin list`, `claude mcp list`, `ls ~/.claude/skills ~/.claude/agents`, the hook names in `~/.claude/settings.json`, and `command -v bd markitdown graphify xerj`. Write the values of `bashOutputMaxChars` and of `BASH_MAX_OUTPUT_LENGTH` in `env` (B2), if they are set. Write the local MCP servers of other projects (`projects.*.mcpServers` in `~/.claude.json`) in the log. For each tool of the guide, write in the log what you found. If a hook or a plugin changes Bash commands or Bash output (for example RTK or Context Mode), write it in the log and tell the user that this guide does not use such a tool (B, "Why this guide does not use RTK and Context Mode"). The user decides. Get the removal steps from the README of the tool. Rule 7 applies.
    4. Do rule 10.
    5. A2 for the user-level MCP servers and the plugins. Show the table: server or plugin, decision. After approval, run `claude mcp remove <name> -s user` for a server in the user configuration. Add a claude.ai connector or a plugin server to `deniedMcpServers` (A2, step 3). Disable a plugin with the command of A2, step 5.
    6. A1 for the user level: make `~/.claude/CLAUDE.md` from `assets/claude-md.user.md` (rule 13). Leave `doc-converter` out of the list of subagents. Leave the ponytail line out (rule 13): phase 2 adds it. Add `disable-model-invocation: true` to the skills in `~/.claude/skills/` that only the user starts (A1, step 7). Add `paths` to each file in `~/.claude/rules/`.
    7. D: ask the user to run `/model opus` and `/advisor fable` (D1). If the user chooses another model or no advisor, write the choice in the D row of the setup log. With no advisor, remove the advisor line from `~/.claude/CLAUDE.md`. Add `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` to `env` in `~/.claude/settings.json` (D2). Make the subagents `scout`, `log-digester`, `test-runner`, `web-researcher`, `implementer` and `reviewer` in `~/.claude/agents/`. Make `implementer` without the `skills` field and with the body sentence "Obey CLAUDE.md.": phase 2 adds the skill. Remove the lines for tools that are not installed: in `scout`, the `xerj` and `graphify` commands, the tool `mcp__basic-memory__bm_search` in `tools` and the three lines about past decisions (Basic Memory, phase 3). Move each MCP server that only one role uses into the `mcpServers` field of that subagent, unless rule 8 keeps it in place.
    8. Global gitignore: if `git config --global core.excludesFile` is empty, set it to `~/.config/git/ignore`. Add `.agent-out/`, `HANDOFF.md` and `.beads/` to the file that `core.excludesFile` names.
- Verify: `python3 scripts/md_budget.py --project .` gives exit code 0 and shows `~/.claude/CLAUDE.md` with a maximum of 40 lines.
- After restart: ask the user to run `/model`, `/advisor` and `/mcp` (rule 5). The main model is opus and the advisor is fable, or they are the choice of the user that the setup log records. Only the approved servers are listed. `claude plugin list` shows as enabled only the plugins that this guide installs and the plugins that the user approved. `CLAUDE_CODE_SUBAGENT_MODEL` is set in `~/.claude/settings.json`. `git check-ignore -v .agent-out/x HANDOFF.md .beads/x` in a git repository matches all three. A test call of `scout` (message from `assets/delegation-message.txt`, with an output file in `.agent-out/`) returns a maximum of 10 lines and a path in `.agent-out/`.

### Phase 2. Process, input compression and navigation

- Read: `references/a-permanent-context.md` (the A1 re-check and A2, step 3), `references/d-delegation.md`, `references/e-process.md`, `references/b-input-compression.md`, `references/c-navigation.md` and the licenses in `references/overlaps.md`.
- Separate approvals (rule 7): the handoff skill (git clone), the ponytail skill (download from GitHub), the plugin prompt-improver, the install script or the release binary of XERJ, and the first bd command (E2). Tell the user about the license of XERJ.
- Do, one tool after the other:
    1. handoff (E3). Add the "Compact instructions" section of `assets/claude-md.user.md` and the line about `/handoff` to `~/.claude/CLAUDE.md`.
    2. ponytail skill (D2). Do the install, the preload and the CLAUDE.md line of D2.
    3. Beads CLI (E2): install it with the command of E2. `bd init --stealth` and `bd setup claude --stealth` are in Part 2. Add its line to "Harness protocol".
    4. prompt-improver (E4), with `--scope user`. Add its item to "Harness protocol" (`assets/claude-md.user.md`).
    5. Quiet commands and the output limit (B1, B2). Add the routing line for shell output from `assets/claude-md.user.md` to `~/.claude/CLAUDE.md`. If phase 1 found a value of `bashOutputMaxChars` or of `BASH_MAX_OUTPUT_LENGTH`, tell the user and recommend its removal (B2). The user decides. Record the decision in the row of `bashOutputMaxChars` in the prerequisites table of the setup log. The quiet commands of each project are in Part 2.
    6. MarkItDown (B3). Make the `doc-converter` subagent from the pattern `assets/agents/scout.md`. Add `doc-converter` to the list of subagents in "Harness protocol" and add its routing line.
    7. Graphify CLI (C1): install it with the command of C1. The skill and the graph are in Part 2.
    8. XERJ (C2). Without the install script, use the release tarball with its sha256. Set `XERJ_DISABLE_FEEDBACK=true` in `env`. `env` loads at the next session, so in this session give the variable inline to the install script and to each `xerj` command. The index is in Part 2.
    9. Add the graphify and xerj commands to `scout`, and the routing line for scout (`assets/claude-md.user.md`) to `~/.claude/CLAUDE.md`.
- After restart: `seq 1 20000` in Bash gives a file path and a preview, not the numbers (B2; not applicable while a plugin or a hook that changes Bash output is enabled; write that in the log). The user sends the prompt `fix the error`, and prompt-improver asks questions. `markitdown` converts a test PDF (the user gives it) into `.agent-out/md/`. `bd --version`, `graphify --help` and `xerj --version` operate. `/handoff` makes `HANDOFF.md` with five sections. In a git repository, give `implementer` this task: "Do not read files, do not start a skill, do not change files and do not commit. Quote rule 2 of your preloaded ponytail skill word for word, or reply none." Compare the reply with rule 2 of `~/.claude/skills/ponytail/SKILL.md` ("2. Already in this codebase ..."). They must match. If the reply is not "none", check in the reply or the transcript that it used no Read or Skill tool call.

### Phase 3. Memory

- Read: `references/f-memory.md`, `references/a-permanent-context.md` (the A1 re-check and A2, step 3) and `references/d-delegation.md`.
- Separate approvals (rule 7): the plugin obsidian-second-brain, the deactivation of its vault MCP server, the selection of the second-brain tool and the vault path, and Basic Memory. Tell the user these facts about Basic Memory (F3): the license, the size, the permanent weight of the MCP server and the deny of its tools that are not read-only.
- Do:
    1. Second brain (F1), with `--scope user`. Set `OBSIDIAN_VAULT_PATH` in `env` in `~/.claude/settings.json`. Before the approval, tell the user the permanent weight of the plugin (F1). Deactivate the vault MCP server of the plugin with `{"serverName": "plugin:obsidian-second-brain:vault"}` in `deniedMcpServers` (A2, step 3).
    2. Make the `brain-writer` subagent from `assets/agents/brain-writer.md`. Add three lines from `assets/claude-md.user.md` to `~/.claude/CLAUDE.md`: its line in "Harness protocol", the line "If memories disagree, the vault wins over auto memory." and the routing line for past decisions. Its notes must pass the validator of the vault plugin.
    3. Keep auto memory on. Tell the user why (F2).
    4. Basic Memory (F3):
        1. Install Basic Memory and register the server with the commands of F3, in the order of F3.
        2. Add `BASIC_MEMORY_NO_PROMOS=1` to `env` in `~/.claude/settings.json`.
        3. Add the tools that are not read-only to `permissions.deny` in the same file (F3). If `bm --version` is not 1.0.0, take the tool names from `/mcp`.
        4. Add the tool `mcp__basic-memory__bm_search` to `tools:` of `scout`, and add the three lines about past decisions from `assets/agents/scout.md` to its body.
        5. The memory projects are in Part 2.
- After restart: ask the user to run `/obsidian-second-brain:obsidian-init` in a session in the vault folder. If the folder `Projects/harness-test/`, the Basic Memory project `harness-test-brain` (`bm project list`) or the file `~/.claude/lean-harness/harness-test.sha` exists, stop. Ask the user for other names, or for the approval to delete what an earlier run of this test left. Use the other names in place of these names in the checks below. Make the folder `Projects/harness-test/` in the vault. The user approves the write prompt for that folder. Do not add a global `additionalDirectories` entry. `brain-writer` writes a test note there with the project name `harness-test`, and the validator shows no warning for it. `claude mcp list` does not show `plugin:obsidian-second-brain:vault`. Then do the checks of Basic Memory in this order (F3):
    1. `claude mcp list` shows `basic-memory` as connected, and `permissions.deny` in `~/.claude/settings.json` has its tools that are not read-only (F3).
    2. `(cd "$OBSIDIAN_VAULT_PATH/Projects/harness-test" && sha256sum *.md > ~/.claude/lean-harness/harness-test.sha)`
    3. `bm project add harness-test-brain "$OBSIDIAN_VAULT_PATH/Projects/harness-test"`
    4. `(cd "$OBSIDIAN_VAULT_PATH/Projects/harness-test" && sha256sum -c --quiet ~/.claude/lean-harness/harness-test.sha)` prints nothing: Basic Memory did not change the note.
    5. Give `scout` a search for a word of the test note. It must call `bm_search` with `project` "harness-test-brain" and the status filter, and must return the test note. Tell `scout` to say which route it used. The grep fallback is a fail of this check. The shell form of the same check is `bm tool search "<word>" --project harness-test-brain --filters '{"status":"active"}' --compact --page-size 5`.
    6. `bm project remove harness-test-brain`. Do not use `--delete-notes`. Then delete the folder `Projects/harness-test/` and the `.sha` file.
    7. Ask the user to run `/context` and record the weight of the `basic-memory` server.
    8. Write the result (pass or fail, and that the test folder was deleted) in the setup log.

### Phase 4. Check and report

No installs in this phase. Do the "After restart" checks of phase 3, then the check (section "Check", Part 1 items). Give the report to the user: for each tool, its status and the open questions. Then tell the user how to start Part 2.

## Part 2. Project onboarding

The user starts the session in the project root. If it is not a git repository, stop.

- Read: sections A1, A2 and B1, and the sections of the installed tools: E2, C1, C2, F1, F3.
- Approval: the change to the md files of the project, and each MCP server removal of step 6 (rule 7).
- Before: do rule 9. If the project gitignores `.claude/` or CLAUDE.md, make a marker file (A1).
- Do. `<project>` is the folder name of the project root.
    1. A1 for the project: bring the project CLAUDE.md to the structure of `assets/claude-md.project.md`, with a maximum of 60 lines. Keep the commands and the invariants. Write the build, test and lint commands in their quiet forms (B1). Run the build and lint commands one time, and give the test command to `test-runner`. Do not copy the lines of `~/.claude/CLAUDE.md` into the project. Leave the line "XERJ prefix" out: step 4 adds it.
    2. Beads: `bd init --stealth`, then `bd setup claude --stealth`. Examine CLAUDE.md and `.claude/settings.json`. Remove the Beads block (E2). Write `.beads/PRIME.md` (E2).
    3. Graphify: `graphify install --project`, then remove its CLAUDE.md text and, unless the user wants them, its Claude hooks (C1). Then run `graphify hook install` for the git hooks (C1). Add `graphify-out/` to `.gitignore`. Commit `.gitattributes` and only the lines that you added to `.gitignore` (C1). For the LLM part, ask the user to start `/graphify .` in a separate session (C1).
    4. XERJ: choose a short `<prefix>` that no other project uses. Start the node (C2). Preview with `xerj autoindex map . --prefix <prefix>`, then run `xerj autoindex . --prefix <prefix>`. Install the hook block of C2 for the refresh. Write the prefix in the "Done" column of the setup log and in the project CLAUDE.md (the line "XERJ prefix" of `assets/claude-md.project.md`).
    5. Vault: make `Projects/<project>/` in the vault and add it to `permissions.additionalDirectories` in `.claude/settings.local.json`. If the folder already has notes, run the note check of F3 first. Then run `bm project add "<project>-brain" "$OBSIDIAN_VAULT_PATH/Projects/<project>"` with the project name in lower case (F3). Notes that `brain-writer` writes in the same session need `bm project index "<project>-brain"` (F3).
    6. A2 for the local MCP servers of the project in `~/.claude.json` and for the servers in `.mcp.json` of the project (rule 7). For a server of `.mcp.json`, run `claude mcp remove <name> -s project`. Write the add command of each removed server in the setup log.
- Verify: `python3 <guide>/scripts/md_budget.py --project .` gives exit code 0. The commands of the project CLAUDE.md are in their quiet forms, the build and lint commands operated in this session, and `test-runner` ran the test command (B1). `bd ready` operates and `git status --short` shows no file in `.beads/`. `graphify hook status` shows the four hooks `installed`, and `post-commit`, `post-merge`, `post-checkout` and `post-rewrite` each hold the block `# xerj-hook-start`. `xerj status --prefix <prefix>` shows `verdict: fresh`, and `xerj search "<topic>" --prefix <prefix>` returns passages with paths. The project CLAUDE.md names the prefix. The vault has `Projects/<project>/`, `permissions.additionalDirectories` in `.claude/settings.local.json` lists it, and `bm project list` shows `<project>-brain`. To test the hooks without a commit, run `sh "$(git rev-parse --git-path hooks)/post-commit"`. The logs are `~/.cache/graphify-rebuild.log` and `~/.cache/xerj-autoindex.log`. `graphify-out/GRAPH_REPORT.md` exists after the first commit that changes a code or Markdown file, because the hook builds it. If no such commit has happened, report "not applicable yet".
- After restart: tell the user to start a new session in the project and to give a work prompt, not the prompt of Part 2. Then the start text shows the lines of `.beads/PRIME.md`. Tell the user to run `/hooks` and to confirm the project hooks that you kept. Write these checks in the setup log with the project path. In this session, write the kept project hooks there too, so that the check can compare them with `/hooks` (section Check).
- Log: add a row to "Onboarded projects". Tell the user which project files changed. Tell the user that these parts have an undo command: the blocks of Graphify and XERJ in the git hooks (C1, C2), the XERJ index (C2) and the memory project (F3). The index and the memory project have no copy. Do not push.

## Check

If the user asks for the check, do the items in `references/acceptance-check.md`: the Part 1 items, and the Part 2 items if the session runs in an onboarded project. Report the result of each item. Write each failure in the setup log. Change only the setup log. The check needs no plan approval and no restart.

## File map

| Section | File |
| --- | --- |
| 1. Ontology of methods | [references/ontology.md](references/ontology.md) |
| A. Permanent context (A1, A2) | [references/a-permanent-context.md](references/a-permanent-context.md) |
| B. Compression of incoming data (B1 to B3) | [references/b-input-compression.md](references/b-input-compression.md) |
| C. Navigation (C1, C2) | [references/c-navigation.md](references/c-navigation.md) |
| D. Delegation (D1 to D4) | [references/d-delegation.md](references/d-delegation.md) |
| E. Process and session hygiene (E1 to E4) | [references/e-process.md](references/e-process.md) |
| F. Long-term memory (F1 to F3) | [references/f-memory.md](references/f-memory.md) |
| Overlaps, licenses | [references/overlaps.md](references/overlaps.md) |
| Check | [references/acceptance-check.md](references/acceptance-check.md) |
| Sources | [references/sources.md](references/sources.md) |

## Templates

| File | Destination |
| --- | --- |
| `assets/setup-log.md` | `~/.claude/lean-harness/setup-log.md` |
| `assets/claude-md.user.md` | the structure of `~/.claude/CLAUDE.md` |
| `assets/claude-md.project.md` | the structure of the project `CLAUDE.md` |
| `assets/agents/scout.md` | `~/.claude/agents/scout.md` |
| `assets/agents/web-researcher.md` | `~/.claude/agents/web-researcher.md` |
| `assets/agents/implementer.md` | `~/.claude/agents/implementer.md` |
| `assets/agents/reviewer.md` | `~/.claude/agents/reviewer.md` |
| `assets/agents/brain-writer.md` | `~/.claude/agents/brain-writer.md` |
| `assets/delegation-message.txt` | the message that you send to a subagent |

The templates show the final state, after phase 3. Before that phase, apply rule 13. The templates are in English because the model reads them in each session or at each delegation. Replace the values in angle brackets and keep the size.

Make `doc-converter`, `log-digester` and `test-runner` from the pattern `assets/agents/scout.md`. Change the description, the tools and the first three lines of the body. Remove the three lines about past decisions, because only `scout` searches Basic Memory. If a model does not support the `effort` value, remove the field. If the Claude Code build has no Grep and Glob tools (D2), remove them from `tools`.

## Script

`scripts/md_budget.py` measures the limits of section A1: the lines of `~/.claude/CLAUDE.md`, of the project CLAUDE.md files and of the CLAUDE.md files in its parent directories, the rules without `paths`, and the `@import` lines:

```bash
python3 <guide>/scripts/md_budget.py --project <project root>
```

The exit code is 0 when all limits are satisfied, and 1 when one is not. It is 2 on a usage error, for example a project path that is not a directory. The script only reads files. The script shows two types of warning, and a warning does not change the exit code. The first is a possible `@import` whose file it did not find: examine it yourself. The second is `no CLAUDE.md found in <project>`. A rule counts as a rule with `paths` only when its header is closed and `paths` has a pattern. An unquoted pattern that starts with `*` does not count, because YAML cannot read it: put the pattern in quotes. This check is a heuristic, not a YAML parser. `python3 <guide>/scripts/test_md_budget.py` runs its cases. Its known gaps are in a comment at the end of that file.
