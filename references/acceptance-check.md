# Check

If the user refused a tool, or if you removed it (rule 11), write that result for the item. Such an item is complete.

Each group of items starts with the name of a list in SETUP.md. That list has the test of each item in the group. Do the test again. An item under "No list in SETUP.md" is its own test.

An item marked "(log)" needs a record in the setup log, not a new test. If the setup log has no record for it, the item is open. Report it. Write it in the setup log. Do not run the test in the check. Name the "After restart" list in SETUP.md that has the test.

## Part 1: environment

Phase 1, "After restart":

- [ ] `/mcp`
- [ ] `claude plugin list`
- [ ] `/model` and `/advisor`
- [ ] `CLAUDE_CODE_SUBAGENT_MODEL`
- [ ] `git check-ignore`
- [ ] (log) the test call of `scout`

Phase 2, "After restart":

- [ ] `seq 1 20000` gives a file path and a preview (B2); not applicable while a plugin or a hook that changes Bash output is enabled; write that in the log
- [ ] `bd --version`, `graphify --help` and `xerj --version`
- [ ] (log) prompt-improver
- [ ] (log) `markitdown`
- [ ] (log) `/handoff`
- [ ] (log) the implementer quote test: in a git repository, `implementer` gets the task of SETUP.md (phase 2, "After restart"): no Read, no Skill, no file change, no commit, quote rule 2 of its preloaded ponytail skill word for word, or reply none. The quote matches rule 2 of `~/.claude/skills/ponytail/SKILL.md`, and the reply or the transcript shows no Read or Skill tool call

Phase 3, "After restart":

- [ ] the vault MCP server in `claude mcp list`
- [ ] check 1 of Basic Memory
- [ ] (log) a brain-writer test passed, as in Phase 3 (a note in a test folder of the vault, validator without warning, folder deleted)
- [ ] (log) a search check passed, as in Phase 3 (checksum of a note unchanged after `bm project add`, `scout` found the note with `bm_search` and not with the grep fallback (with `project` and the status filter), a test project removed), and the `/context` weight of `basic-memory`

No list in SETUP.md:

- [ ] `env` in `~/.claude/settings.json` has no `bashOutputMaxChars` or `BASH_MAX_OUTPUT_LENGTH` that the user did not keep on purpose (B2)
- [ ] `~/.claude/CLAUDE.md` has a maximum of 40 lines and no `@import`, and `~/.claude/rules/` has no rules without `paths`
- [ ] Each line in `~/.claude/CLAUDE.md` and in the subagents names only installed tools, with the exception of rule 13
- [ ] The ponytail skill: `sha256sum ~/.claude/skills/ponytail/SKILL.md` gives the pinned hash of D2, the file has no `disable-model-invocation`, `~/.claude/agents/implementer.md` has `skills` with `ponytail`, and `~/.claude/CLAUDE.md` has the ponytail line
- [ ] The user has the report: for each tool, its status and the open questions

## Part 2: one project

Part 2, "Verify":

- [ ] `md_budget.py`
- [ ] the quiet commands in the project CLAUDE.md (B1)
- [ ] `bd ready` and `.beads/`
- [ ] `graphify hook status` and `GRAPH_REPORT.md`
- [ ] the block `# xerj-hook-start`, `xerj status` and `xerj search`
- [ ] the prefix in the project CLAUDE.md
- [ ] the vault folder, `permissions.additionalDirectories` and `bm project list`

Part 2, "After restart":

- [ ] the start text and `.beads/PRIME.md`
- [ ] `/hooks` and the kept hooks in the setup log

No list in SETUP.md:

- [ ] The project CLAUDE.md has the commands and the invariants, and the procedures are in skills or docs
- [ ] `graphify-out/` is in `.gitignore`
