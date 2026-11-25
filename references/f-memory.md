# F. Long-term memory

Two memory layers: project knowledge in the vault, and preferences with feedback in auto memory. `brain-writer` writes decisions to the vault. Section F2 says when auto memory also keeps decisions. Basic Memory is the search over the project knowledge. It is not a third store (section F3).

| Layer | Tool | What it keeps | How it gets data |
| --- | --- | --- | --- |
| Project knowledge | second brain: a vault of markdown notes | product facts, decisions, contracts | the `brain-writer` subagent, on triggers |
| Search over project knowledge | Basic Memory | an index of the same notes | the MCP server `basic-memory`, which watches the folder |
| Preferences and feedback | Claude Code auto memory | preferences and feedback | automatically |

## F1. Second brain (item 12)

The default candidate is [obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain): a Claude Code plugin with an MIT license that keeps memory in plain markdown files. The selection uses its README, not independent tests. Get the approval of the user for this selection.

Criteria, if you select a different tool:

- the notes are plain markdown files on the disk;
- the permanent text that the tool adds to the context is a maximum of 200 tokens;
- the tool has a search that does not read the full vault;
- the tool marks old and contradictory notes and does not only collect them;
- the project has active maintenance and operates without a cloud service.

```bash
claude plugin marketplace add eugeniughelbur/obsidian-second-brain
claude plugin install obsidian-second-brain@obsidian-second-brain --scope user
```

These are the shell forms of the `/plugin` commands (rule 5).

- Use one vault for all projects. Get its path from the user, for example `~/vaults/brain`. Keep the vault out of the code repository.
- `OBSIDIAN_VAULT_PATH` is a user-scope setting. After approval, set it in `env` in `~/.claude/settings.json`.
- Ask the user to start one session in the vault folder and to run `/obsidian-second-brain:obsidian-init` there.
- Keep the notes of this project in one folder of the vault: `Projects/<project>/`.
- In Part 2, add this folder to `permissions.additionalDirectories` in `.claude/settings.local.json` of the project. Then `brain-writer` can write notes without a permission question.
- The plugin adds approximately 49 commands, hooks and an MCP server for the vault. After the installation, disable the parts that you do not use (section A2).
- Permanent weight (version 0.20.0): 49 commands, none with `disable-model-invocation`, about 2,000 tokens per session (an estimate from the description text; measure with `/context`). This is above the criterion of 200 tokens. Tell the user before the approval.
- SessionStart hook: about 80 tokens outside the vault. Inside the vault it also loads the vault `_CLAUDE.md`, up to 10,000 characters.
- PostToolUse validator: only `.md` files inside `OBSIDIAN_VAULT_PATH`, and only for the Write and Edit tools (matcher `Write|Edit|MultiEdit|NotebookEdit|create_file`). A note that Bash writes, for example with a shell redirect, gets no check.
- The recall hook and the background PostCompact agent are off by default. The PostCompact agent is inert unless `OBSIDIAN_BG_AGENT_ENABLED=1`.
- CAUTION: The PostCompact agent operates with `--dangerously-skip-permissions`. Do not set `OBSIDIAN_BG_AGENT_ENABLED=1` without the approval of the user.
- MCP server name for `deniedMcpServers`: `plugin:obsidian-second-brain:vault`.
- Research commands call external services (xAI, Perplexity, Gemini, YouTube, Whisper, Firecrawl) when their keys exist.

Record these note types automatically:

| Note type | Content | Trigger |
| --- | --- | --- |
| `fact` | a confirmed fact about the product or its behavior | the code or the user confirms the fact |
| `decision` | an accepted decision and its cause | the user makes or confirms the decision |
| `rejected` | a rejected option and the cause | the user rejects the option and gives a cause |
| `contract` | an interface between services: endpoints, events, schemas, owner | an API, an event or a schema changes |

- Record an item immediately when its trigger occurs. Also record open items before you start `/handoff`, before you ask the user to run `/compact` or `/clear`, and when you close a task.
- Do not ask for approval for each note.
- Method: give a list of 3 to 10 lines and the project name to the `brain-writer` subagent. It writes with the Write and Edit tools, so the validator checks each note. It finds the applicable note, updates it or makes a new note, and returns only the paths.
- One note contains one statement. Its frontmatter has `type`, `status` (`active` or `superseded`), `date` and `source` (a task, a PR or a file). `brain-writer` also writes `permalink: <project>-brain/<file name without .md>`, and puts a frontmatter value that contains `: ` in quotes (section F3 gives the cause).
- Only `brain-writer` writes notes of these four types. Use the write commands of the plugins (for example `/obsidian-save`) only when the user tells you.
- If the user replaces a decision, tell `brain-writer` which note the new item replaces. It sets the old note to `superseded`.
- If an item contradicts an active note and the user did not replace that note, do not change the note. Ask the user.
- Do not record secrets, personal data or raw logs. Do not record a guess as a fact.
- Before you make a plan or change a service interface, give `scout` a Basic Memory search of the project for decisions and contracts on the topic (section F3). The search skips notes with `status: superseded`.
- The validator of the vault plugin needs `tags`, `ai-first: true` and the `## For future agent` preamble in each note.

## F2. Text at the start of a session

Two tools of this guide add text at the start of a session: `bd prime` (section E2) and the SessionStart hook of the vault plugin (section F1). A plugin that this guide does not install can add more (section A2, step 5). Keep this text short.

- If the start of a session becomes long, decrease `bd prime` (`.beads/PRIME.md`, section E2).
- Keep auto memory on (section A1, step 8). It holds preferences and feedback. Auto memory keeps decisions only when the project has no `$OBSIDIAN_VAULT_PATH/Projects/<project>/` folder. Before you tell the user, count the memory files in `~/.claude/projects/*/memory/`.
- If the vault and auto memory disagree, the vault wins.

## F3. Basic Memory: search of the project knowledge (item 12)

[Basic Memory](https://docs.basicmemory.com/integrations/claude-code) (version 1.0.0, AGPL-3.0-or-later) makes a local index of the notes in `Projects/<project>/`. Claude Code reaches the index through the MCP server `basic-memory`, registered at user scope. `scout` searches with the tool `bm_search`. This design does not use the Claude Code plugin.

```bash
uv tool install --python 3.12 basic-memory
bm config set ensure_frontmatter_on_sync false
bm config set auto_update false
bm config set cloud_promo_opt_out true
bm project list
claude mcp add basic-memory -s user -e BASIC_MEMORY_NO_PROMOS=1 -- basic-memory mcp
```

- Python 3.12 or later is necessary. `bm` is the short name of `basic-memory`. Check with `bm --version`.
- uv 0.11.8 resolves version 1.0.0 with no `--prerelease=allow` flag (test of 2026-11-23). If `bm --version` shows an older version, install again with `--prerelease=allow`.
- No account, login or API key is necessary. Do not run `bm cloud login`.
- A new configuration has `auto_update` true and a check interval of 24 hours (`update_check_interval` 86400).
- `BASIC_MEMORY_NO_PROMOS=1` turns off the cloud promo messages and their analytics events. The `-e` option sets it for the server. Add it to `env` in `~/.claude/settings.json` too, for CLI calls.
- Size: 468 MB for the tool environment and 65 MB for the embedding model. The first index downloads the model, so it needs the network.
- The first run creates `~/.basic-memory/` (configuration, index database, model) and an empty `~/basic-memory/` (default project `main`).
- `bm project list` creates the database `~/.basic-memory/memory.db`. Let it finish before `claude mcp add`: two first runs at the same time break the new database (`table _alembic_tmp_relation already exists`). Fix: stop all Basic Memory processes, delete the empty `~/.basic-memory/memory.db*` and run `bm project list` again.
- Make one Basic Memory project for each `Projects/<project>/` folder. Do not add the root of the vault, because Basic Memory can write into notes.
- Write the project name in lower case. Version 1.0.0 stores the name in lower case in `config.json`.
- `bm project add` makes the first index: 37 seconds and about 750 MB of memory for 34 notes.
- Make projects only with `bm project add` in the shell (Part 2). The tool `bm_project` is denied.
- To remove a project, run `bm project remove "<project>-brain"`. Do not use `--delete-notes`: the notes stay in the vault.

In Part 2, in each project:

```bash
bm project add "<project>-brain" "$OBSIDIAN_VAULT_PATH/Projects/<project>"
```

The MCP server:

- After the installation, ask the user to start Claude Code again. `claude mcp list` then shows `basic-memory` as connected. The server needs 5 to 10 seconds to start.
- Basic Memory 1.0.0 has 12 tools; 7 are read-only. Deny the 5 tools that are not read-only in `permissions.deny` of `~/.claude/settings.json`: `mcp__basic-memory__bm_write`, `mcp__basic-memory__bm_edit`, `mcp__basic-memory__bm_move`, `mcp__basic-memory__bm_delete` and `mcp__basic-memory__bm_project`. `brain-writer` is the only writer (section F1), and `bm_project` can make a project at the root of the vault.
- Permanent weight: about 480 tokens of server instructions in each session, and up to about 8,200 tokens of tool schemas if all of them load (the raw size of the tool list). Ask the user to run `/context` and record the real number.
- The server is one process for each session. It watches the folders of the projects that existed when it started: a new note in such a project is searchable in about 3 seconds with no manual index.
- A running server searches a project that `bm project add` made later. Its watcher does not watch the new folder at once: the setting `watch_project_reload_interval` is 300 seconds. For a new note in the same session, run `bm project index "<project>-brain"`.
- Do not add `basic-memory` to `deniedMcpServers` (section A2).
- The names of the MCP tools changed between versions. Get them from `/mcp`.

Basic Memory 1.0.0 can write into notes:

- A note that has no `permalink:` changes. Basic Memory adds `permalink:`, removes the last newline and wraps long frontmatter values. `ensure_frontmatter_on_sync false` does not stop this. The server changes a new note with no `permalink:` in a folder that it watches in 5 seconds or less.
- A note that has `permalink:` and valid YAML frontmatter stays unchanged. For this reason `brain-writer` writes `permalink: <project>-brain/<file name without .md>` in each note.
- A note with invalid YAML frontmatter is missing from a search with `filters` or `note_types`. The usual cause is a value with `: ` and no quotes, for example in `title`. `brain-writer` puts such a value in quotes.
- Before the first `bm project add` of a folder that already has notes, this command must print no file. If it prints files, give those notes to `brain-writer` for repair first. It parses the header of each note with PyYAML, the YAML library of Basic Memory 1.0.0. It prints a note that has no closed header, a header that does not parse, a YAML alias or merge key, or no `permalink` value in the header. It also prints a note that is not UTF-8. It does not read hidden folders.

```bash
uv run --no-project --with 'pyyaml>=6' python3 - "$OBSIDIAN_VAULT_PATH/Projects/<project>" <<'EOF'
import pathlib, re, sys, yaml
root = pathlib.Path(sys.argv[1])
for note in sorted(root.rglob("*.md")):
    if any(part.startswith(".") for part in note.relative_to(root).parts):
        continue
    try:
        found = re.match(r"(?:[ \t]*\n)*---[ \t]*\n(.*?)\n---[ \t]*(\n|$)", note.read_text(encoding="utf-8-sig"), re.S)
        header = yaml.safe_load(found.group(1)) if found else None
        tokens = yaml.scan(found.group(1)) if found else []
        banned = any(isinstance(t, yaml.AliasToken) or (isinstance(t, yaml.ScalarToken) and t.plain and t.value == "<<") for t in tokens)
        bad = banned or not isinstance(header, dict) or not header.get("permalink")
    except (yaml.YAMLError, UnicodeDecodeError):
        bad = True
    if bad:
        print(note)
EOF
```

`scout` calls the tool `mcp__basic-memory__bm_search` with `query` "<topic>", `project` "<project>-brain", `filters` {"status": "active"}, `compact` true and `page_size` 5.

- `project` is necessary. With no `project`, the tool returns an error.
- The default mode is hybrid (words and meaning). `mode` "text" is for exact words. `mode` "semantic" is for a question in other words.
- `note_types` ["decision"] limits the search to one note type.
- A result line is `- <path in the project folder> | <title> | score <number>`. Read the note with the Read tool at `$OBSIDIAN_VAULT_PATH/Projects/<project>/<path>`.
- One search takes about 3 seconds.
- If the tool is not available or fails, grep `$OBSIDIAN_VAULT_PATH/Projects/<project>/` and skip notes with `status: superseded`.

From the shell (the manual route and the setup checks):

```bash
bm project index "<project>-brain"
bm tool search "<topic>" --project "<project>-brain" --filters '{"status":"active"}' --compact --page-size 5
```

- The CLI does not index before a search. Run `bm project index` first when no server runs.
- One CLI search takes 7 to 26 seconds. Do not use `--json`: it gives 3 to 18 kB.
- The docs show `bm tool search-notes` with `--vector`. Version 1.0.0 does not have this form. Get the options from `bm tool search --help`.

Part that this design does not use: the Claude Code plugin (`bm install claude-code`). It adds a briefing at the start of a session, a checkpoint before compaction and skills that write notes. `brain-writer` writes the notes. Install the plugin only if the user asks, and then apply section F2.
