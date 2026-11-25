# Sources

Claude Code documentation, read on 2026-11-21:

- [Advisor](https://code.claude.com/docs/en/advisor)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Memory and CLAUDE.md](https://code.claude.com/docs/en/memory)
- [Skills](https://code.claude.com/docs/en/skills)
- [Manage costs](https://code.claude.com/docs/en/costs)
- [Preload skills into subagents](https://code.claude.com/docs/en/sub-agents.md) (a skill with `disable-model-invocation: true` cannot be preloaded)

Tool sources, read on 2026-11-21:

- RTK: https://github.com/rtk-ai/rtk
- Context Mode: https://github.com/mksglu/context-mode
- MarkItDown: https://github.com/microsoft/markitdown
- Graphify: https://pypi.org/project/graphifyy/
- XERJ: https://github.com/xerj-org/xerj, https://xerj.org/get
- XERJ licenses, read on 2026-11-24: https://github.com/xerj-org/xerj/blob/main/README.md and https://github.com/xerj-org/xerj/releases/tag/v1.0.0-rc.101 (the engine source is Apache-2.0; the Query-1 crates in release binaries since rc.101 are proprietary)
- handoff: https://github.com/odinokov/handoff
- Beads: https://github.com/steveyegge/beads
- prompt-improver: https://github.com/severity1/claude-code-prompt-improver
- obsidian-second-brain: https://github.com/eugeniughelbur/obsidian-second-brain
- Basic Memory, read on 2026-11-23: https://docs.basicmemory.com/reference/configuration, https://docs.basicmemory.com/reference/migrating-to-1-0, https://docs.basicmemory.com/integrations/claude-code, https://docs.basicmemory.com/reference/cli-reference, https://github.com/basicmachines-co/basic-memory, https://pypi.org/pypi/basic-memory/json, https://docs.basicmemory.com/reference/mcp-tools-reference

Tests run on 2026-11-22 (Graphify 0.9.114, XERJ 1.0.0-rc.104 with a stub `xerj` binary, Beads 1.3.4):

- `graphify hook install` and `uninstall`: the four hook blocks, the `.gitattributes` line, the detached rebuild with its log, the skip in linked worktrees, the build at the first commit that changes a code file, and the nodes that survive a rebuild.
- `xerj autoindex --help` and `xerj status --help`: the default prefix `ax`, `autoindex remove`, and no hook installer. Two real `autoindex` runs on this repository: 85.6 s and 76.1 s, 144 records live, 0 records submitted (the log says "already indexed; nothing new to send"). The `verdict:` line has padded spaces (observed in a review run, not a test of the freshness logic).
- The XERJ hook block of C2 in scratch repositories with a stub `xerj`: a fast commit, the lock, the skip on `verdict: fresh`, the skip in a worktree and on a file checkout, and a hook that stays after `graphify hook uninstall`.
- `bd hooks install` uses marker blocks, like Graphify.
- `claude mcp remove --help`, Claude Code 2.1.330, read on 2026-11-22: the option `-s, --scope <scope>` takes `local`, `user` or `project`.
- `xerj --help`, XERJ 1.0.0-rc.104, and the install script `https://xerj.org/get`, read on 2026-11-22: the options `--insecure` and `--data-dir`, the node start `xerj --insecure --data-dir ~/xerj-data`, and `XERJ_DISABLE_FEEDBACK=true` (same as `--disable-feedback`).
- `graphify install --project` in an empty git repository, Graphify 0.9.114, 2026-11-22: it wrote `.claude/skills/graphify/`, `CLAUDE.md`, `.claude/CLAUDE.md` and `.claude/settings.json`. `~/.claude/CLAUDE.md` did not change.

Tests run on 2026-11-24:

- `claude --help`, Claude Code 2.1.331, read on 2026-11-24: the option `--effort <level>` ("Effort level for the current session") takes `low`, `medium`, `high`, `xhigh` or `max`.

Tested on the setup machine, 2026-11-21: the vault validator result.

Basic Memory 1.0.0 tests, 2026-11-21 and 2026-11-22 (setup log): the first-run race of the new database and the MCP registration command of section F3.

Basic Memory 1.0.0 tests, 2026-11-23 (uv 0.11.8, Python 3.12, a copy of 34 vault notes): the index and the search commands of section F3, the writes into notes with and without `permalink:`, the filter and the invalid YAML result, the sizes and times, the MCP server (12 tools, the read-only tools, the size of its text, the watcher, `bm_search` and `bm_read`), `bm project remove`, and the checksum check.

Claude Code 2.1.330, 2026-11-23: `claude plugin disable --help` (the form `claude plugin disable [plugin]` and the option `-s, --scope <scope>` with `user`, `project` or `local`), and `claude plugin list` (the version and the scope of each plugin). The plugin cache on the setup machine: `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` with `hooks/hooks.json`, `skills/` (superpowers 7.0.2, codex 1.0.6) and `commands/` (obsidian-second-brain 0.20.0, codex 1.0.6), and two versions of one plugin in the cache. Context Mode 2.2.1 has no `hooks/hooks.json`: the `hooks` key of its `.claude-plugin/plugin.json` names `./hooks/claude-code.json`.

Claude Code documentation, read on 2026-11-23: the page [Subagents](https://code.claude.com/docs/en/sub-agents), section "Scope MCP servers to a subagent" (an entry of `mcpServers` is an inline definition or the name of a server of the session, and a name shares the connection of the parent session), and the page [MCP](https://code.claude.com/docs/en/mcp) (environment variable expansion in `.mcp.json` and in the server entries of `~/.claude.json`). A search of both pages found no statement that the expansion applies to a subagent file.

prompt-improver 0.6.1, 2026-11-23: `scripts/engine.py UserPromptSubmit` with three test events (prompts of 13, 500 and 1,507 characters). The added text had 1,118 characters and a copy of the prompt. In a session of Claude Code 2.1.330, each notification of a finished background subagent came with the evaluation text.

Earlier versions of this guide used Context Mode. Context Mode 2.2.1, 2026-11-23: one line at the start of a session of Claude Code 2.1.330 (it tells Claude to call `ctx_resume`), and the file `hooks/claude-code.json` with the events PostToolUse, PreToolUse, SessionStart and UserPromptSubmit. The README of the plugin (its tools table) and the tool list of a session of Claude Code 2.1.330 name the batch tool `ctx_batch`. The file `server.mjs` of the plugin has no `ctx_batch_execute`. In the main session, its hooks redirected WebFetch, curl and large reads, and a full Read of a 7.5 KB file came back cut (observed once). In subagents, long Bash output came back cut.

XERJ 1.0.0-rc.104, 2026-11-24, two indexed projects: `xerj status` with no `--prefix`, run in the folder of the second project, printed `prefix: ax` and the root of the first project. `xerj status --prefix <prefix>` printed the `root:` of that prefix. A search with no prefix, run in the folder of the second project, returned paths of the first project, and the search with the prefix of the second project returned paths of the second project.

Claude Code documentation, read on 2026-11-24: the page [Memory](https://code.claude.com/docs/en/memory), sections "Path-specific rules" and "Rule frontmatter reference". `paths` accepts a YAML list or a comma-separated string. If the header does not parse, Claude Code loads the rule as if it had no `paths`. The page does not say what a missing closing `---` or an empty `paths` does. The cases of the `paths` check are in `scripts/test_md_budget.py`. PyYAML 6.0.2 raised a `ScannerError` (while scanning an alias) for `paths: **/*.ts` on 2026-11-24.

Basic Memory 1.0.0, the installed package, read on 2026-11-24: python-frontmatter 1.3.0 and PyYAML 6.0.4; the header loader is a subclass of `yaml.SafeLoader` that also rejects aliases and merge keys. The note check of section F3 was tested on 2026-11-24 (uv 0.11.8, PyYAML 6.0.2, Python 3.10.16) with scratch notes for each case that its sentence names. A reviewer compared the command with the header parser of Basic Memory 1.0.0 on 28 notes: they agreed on all 28. `bm project remove --help` (1.0.0), read on 2026-11-24: removing a local project stops tracking it, and its files stay on disk unless `--delete-notes` is passed.

Tests run on 2026-11-25 (uv 0.11.8), for rule 6 of SETUP.md:

- `uv run python -c 'print(1)'` in an empty folder writes no file. In a folder with a `pyproject.toml`, the same command writes `.venv` and `uv.lock`. So uv without `--no-project` writes these files only in a project.

Read on 2026-11-25, for B1 and B2:

- Claude Code documentation: [Tools reference](https://code.claude.com/docs/en/tools-reference), section "Output limits" (about 30,000 characters inline for a success, then a file and a preview of up to 2,000 characters; about 10,000 characters of head and tail for a failure, with no file; the exit code 1 list), [All settings](https://code.claude.com/docs/en/settings-reference) (`bashOutputMaxChars`, clamped to 4,000 to 128,000, Claude Code 2.1.261 or later; when it is set, Claude Code ignores `BASH_MAX_OUTPUT_LENGTH`) and [Environment variables](https://code.claude.com/docs/en/env-vars) (`BASH_MAX_OUTPUT_LENGTH`, default 30,000, up to 150,000; when `bashOutputMaxChars` is set, it is ignored). The Tools reference says that `BASH_MAX_OUTPUT_LENGTH` enlarges only the read-back window: "It doesn't raise the inline ceilings".
- Anthropic, [Maximizing the value of your Claude Code sessions](https://claude.com/resources/articles/maximizing-the-value-of-your-claude-code-sessions): each turn reads the history from the cache; quiet flags or `tail`, and quiet commands in CLAUDE.md; subagents for output that you do not need to keep, and their cost on small jobs.
- Claude Code 2.1.331: `claude plugin --help` and `claude plugin details --help`. `details` shows the components of a plugin and its projected token cost (A2, step 5).
- RTK (https://github.com/rtk-ai/rtk, commit e87da19): `INSTALL.md`, section "Uninstalling" (read, not run). SETUP.md, phase 1, step 3, says to get the removal steps from the README of such a tool.
- RTK, +13% total cost on 100 SWE-bench Verified tasks: [Dasein, code-compression-bench](https://github.com/daseinlabs/code-compression-bench).
- RTK, +7.6% median cost at low effort and +0.1% at high effort (p=0.99), 80 clean pairs of 86 SkillsBench tasks: [JetBrains](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/).
- RTK, about 0.5% of spend saved: [Codepointer](https://codepointer.dev/p/cutting-llm-token-costs-with-rtk). An estimate, not a measurement. It is a counterfactual replay of 500 sessions of its author, computed from the published per-command rates of RTK (60 to 99 percent, depending on the command). It did not measure task success.
- Context Mode, workload tokens +94% and +46% on the tasks of Stet (Codex CLI; tokens, not cost): [Stet](https://www.stet.sh/blog/gpt-56-token-saving-modes).
- Marmelab, [Cutting the Coding Agent Bill](https://marmelab.com/blog/2026/08/27/which-agent-based-plugin-should-you-use-in-2026.html): cache reads drive the cost; Bash was 6.4% of the tool-result tokens.
- An overview of these measurements, not the source of a number: [Context Engineering: Tools and Ecosystem](https://cc.bruniaux.com/guide/context-engineering-tools/).
- The race of two `updatedInput` hooks: [Claude Code issue 83353](https://github.com/anthropics/claude-code/issues/83353) (the hook that finishes last wins; reported on Claude Code 2.1.220, closed).
- Exit code of a pipe, bash, tested on 2026-11-25: `false 2>&1 | tail -n 80` gives 0, and with `set -o pipefail;` first it gives 1.

Read on 2026-11-25, for D2 (ponytail):

- Repository [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), release v5.3.3 (tag commit 7801d06), license MIT ([LICENSE](https://github.com/DietrichGebert/ponytail/blob/v5.3.3/LICENSE)).
- File `skills/ponytail/SKILL.md`, [raw at v5.3.3](https://raw.githubusercontent.com/DietrichGebert/ponytail/v5.3.3/skills/ponytail/SKILL.md): 3,496 bytes, sha256 `9badd22a32e19cb884e46dfa8d3aae82bb81dfa5484105b8b4f0262df823a509`. It is byte-identical at v5.3.3 and at commit 96608e0, which was installed on 2026-11-21 on this machine. Its frontmatter has `name`, `description`, `argument-hint` and `license`, and no `disable-model-invocation`.
- The download command of D2 was tested on 2026-11-25 (Claude Code 2.1.332): exit 0, 3,496 bytes, the hash above.
- [INSTALL.md](https://github.com/DietrichGebert/ponytail/blob/v5.3.3/INSTALL.md) (read, not run): install `skills/ponytail/SKILL.md` as a skill by hand. Its `npx skills add DietrichGebert/ponytail` installs six skills and has no documented pin.
- [Subagents](https://code.claude.com/docs/en/sub-agents): for a skill in the `skills` field, "The full skill content is injected, not only the description." Finding of 2026-11-21 on this machine, from the same page: `disable-model-invocation: true` blocks the preload.
- [JetBrains, Ponytail skill tested](https://blog.jetbrains.com/ai/2026/07/ponytail-skill-claude-tested/): ponytail 4.8.4, 80 paired SkillsBench tasks, Claude Code 2.1.201, claude-sonnet-5. The median task cost was 10.3% lower (p=0.004), the code 15.4% shorter and the time 11% shorter. 9 tasks were worse, 6 better and 65 the same. The test injected the ruleset into a main session that wrote the code. A copy of SKILL.md in a skills folder did not start by itself in ten sessions. The preload into a subagent was not measured.
- The Ponytail plugin was rejected on 2026-11-25: its SessionStart hook adds the ruleset (about 2,900 characters) to every main session, and no setting was found that keeps it out (partial read of the repository).
- The implementer quote test of SETUP.md (phase 2, "After restart"), tested on 2026-11-25 on this machine (Claude Code 2.1.332, `implementer` with `skills: [ub-mode, ponytail]`): the reply quoted rule 2 of `SKILL.md` word for word, with 0 tool calls.

Read on 2026-11-25, for the opening paragraph of README.md (cost of a long session):

- [Prompt caching](https://code.claude.com/docs/en/prompt-caching), section "How the cache is organized": "Claude Code re-sends the full context: the system prompt, your project context, every prior message and tool result, and your new message." Tool definitions are in the system prompt layer; CLAUDE.md, auto memory and rules without `paths` are the project context layer. The page names no Claude Code version for this.
- Same page: caching is on by default and is turned off with `DISABLE_PROMPT_CACHING=1`. A change anywhere in the prefix recomputes everything after it. Breaks: a model change ("Each model has its own cache"), a change of effort on most models, adding or removing tool definitions, compaction, the first session after a Claude Code upgrade. Not breaks: an edit of CLAUDE.md in a running session (Claude Code reads it at the start), a skill call, a permission mode change.
- Same page, section "Cache lifetime": the main conversation has a 1 hour lifetime on a Claude subscription within the included usage, and 5 minutes on an API key, a cloud provider or usage credits. Subagents and compaction use 5 minutes. `promptCacheTtl` and `CLAUDE_CODE_PROMPT_CACHE_TTL` need Claude Code 2.1.242 or later.
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing), section "Prompt caching": a cache read costs a fraction of the base input price (0.1x on most models; lower on some). A cache write costs more than base input (1.25x for 5 minutes, 2x for 1 hour). The README gives no price or multiplier.
- [Manage costs](https://code.claude.com/docs/en/costs), section "Why usage climbs in a long session": each use of a tool sends another request with its results; Claude Code sends the full conversation with every request; `/compact` reads the conversation that it summarizes, so compaction of a large context is a large request. `/usage` shows a "Prompt cache (main)" line from Claude Code 2.1.251 (the cause text from 2.1.260).
- [MCP](https://code.claude.com/docs/en/mcp), section "Scale with MCP tool search": tool search is on by default; "Only tool names and server instructions load at session start". With `ENABLE_TOOL_SEARCH=auto`, tools load up front while their definitions total under 10% of the context window. The page names no version for the default. This is the source of A2, step 4.
- [Skills](https://code.claude.com/docs/en/skills) (partial read: the first 100,000 characters of the page): the descriptions load at the start, and the full content loads when the skill is used. The description and `when_to_use` together are cut at 1,536 characters for each skill. `disable-model-invocation: true` keeps the description out of the context. A subagent with a preloaded skill gets the full content at the start.
- [Context window](https://code.claude.com/docs/en/context-window): "Before you type anything: CLAUDE.md, auto memory, MCP tool names, and skill descriptions all load into context", with the system prompt and environment info. [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works): the first 200 lines or 25 KB of `MEMORY.md` load at the start while auto memory is on. [Hooks guide](https://code.claude.com/docs/en/hooks-guide): the output of a SessionStart hook is added to the context (the context-window page does not list it among the items before the first message).
- The Claude Code version in force when these pages were read is not stated on them. The guide's own tests used 2.1.332 on 2026-11-25.

The links to the repositories and pages of the tools are in sections A to F. The ponytail links for D2 are above. This guide does not include the saving values from the README files of the tools, because they are statements of the authors. Section B gives third-party measurements, with the sources above.
