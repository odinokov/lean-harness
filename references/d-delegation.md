# D. Delegation

In the main session you are the orchestrator, and your model is Opus. The orchestrator makes plans, gives work to subagents and accepts their results. Subagents on low-cost models do the search, read, test, log and web work, and they write the code.

## D1. Opus orchestrator and advisor (item 10)

```text
/model opus
/advisor fable
```

The user runs these two commands. The user can choose another main model or no advisor (SETUP.md, phase 1, step 7).

- The advisor must not be weaker than the main model. For Opus 5 and Opus 5.5, the documentation permits Fable, or Opus 5 or later.
- Access to Fable is necessary. On some plans, a one-time agreement to pay for Fable with usage credits is also necessary. The sequence is: `/model fable`, accept, `/model opus`, `/advisor fable`. This is a decision about money, and the user makes it.
- The `/advisor` command saves the selection in the user settings as `advisorModel`. Do not write this setting yourself. For one session, the user can start `claude --advisor fable`.
- The advisor operates only through the Anthropic API. The feature flags of Claude Code are also necessary. If the environment variable `DISABLE_TELEMETRY` is set, the advisor stays off.
- Each advisor call reads the full conversation again, without a cache. A short session decreases the cost of each call.
- The model selects the moment of the call. To control it, put one line in `~/.claude/CLAUDE.md`: consult the advisor before you complete a plan and before you say that a task is done.
- Subagents get the advisor from the main session. In the prompts of `scout`, `doc-converter`, `log-digester`, `test-runner` and `brain-writer`, write: "Do not consult the advisor."

Rules for the orchestrator:

- Do not read more than 200 lines of a file in one call. For more, give the work to a subagent.
- Do not run tests and do not change project code yourself. Give this work to subagents.
- Changes to the configuration files of the harness are the exception. You make them yourself.
- Keep only the plan, the task status and the decisions in your context.
- Give paths to subagents, not file content.

## D2. Many subagents with a low-cost model and effort (item 4)

Each subagent is a file `~/.claude/agents/<name>.md`, so that all projects have it. A project can replace one with its own `.claude/agents/<name>.md`. Its frontmatter has the fields `model` and `effort`.

| Subagent | Work | model | effort | CLAUDE.md | Tools | Preloaded skill |
| --- | --- | --- | --- | --- | --- | --- |
| `scout` | search in code, graph and index | haiku | low | no | Read, Grep, Glob, Bash, Write, `mcp__basic-memory__bm_search` | none |
| `doc-converter` | conversion with MarkItDown | haiku | low | no | Bash, Write | none |
| `log-digester` | logs, dumps, CI output | haiku | low | no | Bash, Read, Write | none |
| `test-runner` | test runs | haiku | low | no | Bash, Write | none |
| `brain-writer` | notes in the vault | haiku | low | no | Read, Write, Edit, Bash | none |
| `web-researcher` | web search and web pages | sonnet | medium | no | WebSearch, WebFetch, Bash, Write | none |
| `implementer` | code for one task | sonnet | medium | yes | all | `ponytail` |
| `reviewer` | review of a diff, static check | sonnet | high | yes | Read, Grep, Glob, Bash, Write | none |

- Values of `model`: `haiku`, `sonnet`, `opus`, `fable`, a full model ID, or `inherit`. Values of `effort`: `low`, `medium`, `high`, `xhigh`, `max`. The model sets which effort values are available.
- Claude Code selects the model in this sequence: the parameter of the call, the frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL`, the model of the main session. Do not set the parameter of the call, because it replaces the model of the frontmatter.
- Set `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` in `env` in `~/.claude/settings.json`. Then a subagent without a `model` field does not get Opus.
- This variable does not change the built-in Explore and Plan agents. They use the model of the main session, which is Opus. For a search, use `scout`.
- Keep the `description` of each subagent to one line. Use `maxTurns` to set a limit on a subagent with a bounded job: the templates set it for `scout`, `brain-writer` and `web-researcher`, not for `implementer` and `reviewer`.
- Some Claude Code builds (2.1.330 here) have no Grep and Glob tools. A subagent that searches must have Bash. It uses grep and find.

The ponytail skill of `implementer`:

- The skill has rules for the smallest complete change. `implementer` writes less code and less text.
- JetBrains measured ponytail 4.8.4 on 80 paired tasks: the median cost was 10.3% lower and the code 15.4% shorter (9 tasks worse, 6 better, 65 the same). The test injected the ruleset into a main session. This guide installs v5.3.3. JetBrains did not measure the preload into a subagent.
- Install at user scope (rule 12): `mkdir -p ~/.claude/skills/ponytail`, then `curl -fsSL https://raw.githubusercontent.com/DietrichGebert/ponytail/v5.3.3/skills/ponytail/SKILL.md -o ~/.claude/skills/ponytail/SKILL.md`. `sha256sum ~/.claude/skills/ponytail/SKILL.md` must give `9badd22a32e19cb884e46dfa8d3aae82bb81dfa5484105b8b4f0262df823a509`. If the hash differs, stop and tell the user.
- If `~/.claude/skills/ponytail/SKILL.md` exists with the same hash, keep it (session procedure, step 6). If it exists with another hash, do not overwrite it. Tell the user, and download only after their approval (session procedure, step 6).
- Preload: add `skills:` with `- ponytail` to `~/.claude/agents/implementer.md`. Change "Obey CLAUDE.md." in its body to the form of `assets/agents/implementer.md`. Do not add `disable-model-invocation` to the skill, because it blocks the preload.
- Main session: add the line of `assets/claude-md.user.md` that keeps ponytail out of the main session. The description of the skill stays in the skill list.
- Install the skill, not the plugin: its SessionStart hook adds the ruleset to every main session. Do not use `npx skills add`: it installs six skills and has no documented pin.
- If the user refuses the skill, `implementer` stays as phase 1 made it (no `skills` field, body "Obey CLAUDE.md."), and `~/.claude/CLAUDE.md` gets no ponytail line.
- Removal: delete `~/.claude/skills/ponytail/`, the `skills` field of `implementer`, the body sentence and the CLAUDE.md line.

## D3. Subagents with no context (item 5)

A subagent starts with a clean context window. It does not get the conversation, the files that you read, or the system prompt of Claude Code. By default it gets the CLAUDE.md files and a snapshot of git status.

These settings apply to the subagents that have "no" in the CLAUDE.md column of the D2 table:

- `omitClaudeMd: true` removes the user, project and local CLAUDE.md files. Claude Code v2.1.271 or later is necessary.
- A short `tools` list also removes the MCP tools that the subagent gets from the main session.
- A `tools` list without `Skill` also stops the use of other skills. The templates in `assets/agents/` use this method.
- Keep the `skills` field empty.
- Keep the body of the system prompt to a maximum of 15 lines. `brain-writer` is exempt, because its note format must be present at runtime.
- Write all that the subagent must know in the delegation message: the goal, the input paths, the output file, the reply format and the stop condition.

The subagents with "yes" in that column do not use these settings, because the project conventions are necessary for their work.

## D4. Large results go to a file, not to the output (item 6)

If a result is longer than 30 lines, the subagent writes it to a file.

- Task results go to the folder `.agent-out/<task-id>/`. The delegation message gives the path of each output file: the full path, except for `implementer`. For `implementer`, give a path relative to its worktree root, because its Write tool refuses paths outside the worktree. Read the file before you remove the worktree.
- Converted documents go to `.agent-out/md/`. All tasks use them.
- Add `.agent-out/` to the global gitignore (`git config --global core.excludesFile`).
- The last message of a subagent has a maximum of 10 lines: status, file path, a maximum of five findings, open questions.
- Read the file in parts: use Grep or grep in Bash, or Read with `offset` and `limit`.
- In a sequence of subagents, give the path to the next subagent, not the text.
- This is a rule in the prompt, not a built-in function. The subagent must have the Write tool, and its system prompt must contain the rule.
