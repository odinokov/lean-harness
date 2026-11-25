# E. Process and session hygiene

One session does one task, or one group of independent tasks in parallel subagents. Then the session stops. Files move the state between sessions: the plan, the tasks in Beads and `HANDOFF.md`.

## E1. Plan in one session, tasks in other sessions (item 8)

1. Start a plan session with Opus and the advisor. Do not change code in this session.
2. Get the inputs. Give the questions about architecture and code to `scout`, which uses `GRAPH_REPORT.md` and XERJ. Give `scout` the Basic Memory search for decisions and contracts on the topic (section F3).
3. Ask the user to set plan mode (Shift+Tab). Make the plan and get the approval of the user. Then go out of plan mode.
4. Write the plan in `docs/plans/<slug>.md`: the goal, the limits, the accepted and rejected decisions, and the risks.
5. Divide the plan into tasks in Beads and add their dependencies. Each task must be complete in itself:
    - the goal in one sentence;
    - the files and modules that the task changes;
    - the acceptance criteria and the verification command, in its quiet form (section B1);
    - links to the plan and to notes in the vault;
    - a size that one session can complete without compaction.
6. Send the decisions of the plan to `brain-writer`.
7. Stop the plan session. All necessary data is in files.
8. Do each task in a new session. In that session, the orchestrator claims the task (`bd update <id> --claim`) and gives the full task text to `implementer`, which operates in an isolated worktree.
9. You can do independent tasks at the same time. Start them as subagents of one session, because local Beads permits only one writer.
10. After `implementer` replies, do these steps in sequence:
    - read the verification result in the reply and the output file in the worktree's `.agent-out/`, before you remove the worktree;
    - give the branch and the worktree path to `reviewer`;
    - if `reviewer` rejects the work, start `implementer` again with the findings, then give the branch and the worktree path to `reviewer` again. Repeat until `reviewer` approves;
    - in the worktree, merge the branch of the user into the worktree branch. If the merge has a conflict, abort it, give `implementer` the two branches to merge, then repeat from the review;
    - give the verification command and the worktree path to `test-runner`. If the verification fails, start `implementer` again with the failure, then repeat from the review;
    - if the user gave no instruction to merge, ask for it. If the user refuses, keep the branch, send the decisions to `brain-writer` and stop: the task stays open (E3);
    - if the branch of the user has a new commit since the verification (compare the commit ids), repeat from the merge into the worktree branch;
    - merge the worktree branch into the branch of the user. If the merge fails, stop and tell the user. Then remove the worktree;
    - run `bd close <id>`, only after a passed verification and this merge;
    - send the decisions to `brain-writer`.

## E2. Local Beads (item 13)

[Beads](https://github.com/steveyegge/beads) is a CLI task tracker for agents with a dependency graph. The repository is now `gastownhall/beads`. The old link goes to the same repository.

```bash
brew install beads          # or: npm install -g @beads/bd
bd init --stealth           # local: no commits to the main repository
bd setup claude --stealth   # hooks and settings for Claude Code
```

- `npm install -g @beads/bd`: npm 11 skips the postinstall script (allowScripts warning). `bd --version` still works because the package has the native binary.
- Part 1 installs the CLI. `bd init --stealth` and `bd setup claude --stealth` run in Part 2, in each project.
- "Local" means: the `--stealth` mode, the embedded Dolt database in `.beads/embeddeddolt/`, and no `bd dolt push` or `bd dolt pull`.
- The embedded mode permits one writer. Only the orchestrator changes Beads. Subagents give their status in their last message.
- Work cycle: `bd ready`, `bd show <id>`, `bd update <id> --claim`, `bd close <id>`. To make a task: `bd create "Title" -p 0`. To add a dependency: `bd dep add <child> <parent>`.
- Each bd command sends usage metrics that bd calls anonymous: the command name, the bd version and the OS platform, with a machine-derived ID, to `https://gastownhall-eventsapi.com/mp/collect`. `bd --version` sends them too. `bd metrics` shows "Anonymous usage metrics: ON" by default. Rule 7 applies: before the first bd command, get the approval of the user to run it, and ask whether to turn the metrics off. If the user agrees, run `bd metrics off`. Write the decision in the setup log.
- `bd init --stealth` writes only `.git/info/exclude`, `beads.role` in `.git/config`, and `.beads/`. It writes no `AGENTS.md`, no hooks and no Claude Code setup (bd 1.3.4).
- `bd setup claude --stealth` writes the SessionStart hook `bd prime --stealth --hook-json` to `.claude/settings.json` of the project. It also makes CLAUDE.md, or appends to it, a block of 54 lines (with the markers) between `<!-- BEGIN BEADS INTEGRATION ... -->` and `<!-- END BEADS INTEGRATION -->`. The block says "Use `bd remember` for persistent knowledge", which this section forbids. Plain `bd setup claude` writes the same files with the hook `bd prime --hook-json`.
- Remove the Beads block from the project CLAUDE.md. If Beads made the file, delete it. `~/.claude/CLAUDE.md` has the line about Beads.
- In CLI mode, `bd prime` prints about 5 KB at each SessionStart (4,955 bytes; 5,513 bytes with `--hook-json`, bd 1.3.4). A file `.beads/PRIME.md` replaces the default text (`bd prime --help`). `.beads/` is excluded from git, so the file stays local. To keep the start text short (section F2), write `.beads/PRIME.md` with this text. With it, the hook output was 478 bytes:

    ```
    Beads holds the tasks of this project. Only the orchestrator changes Beads.
    Work cycle: `bd ready`, `bd show <id>`, `bd update <id> --claim`, `bd close <id>`.
    New task: `bd create "Title" -p 0`. Dependency: `bd dep add <child> <parent>`.
    Do not use `bd remember`: knowledge goes to brain-writer. Do not commit or push without an instruction.
    ```
- Do not use `bd remember`. Knowledge goes to the vault. Beads keeps only tasks.

## E3. Do not go back to old sessions: handoff or /compact (item 9)

An old long session has two costs. Each request sends the full history. Also, the first message after a long stop processes the full context again, because the cache is expired.

Use the first row that applies:

| Condition | Action |
| --- | --- |
| The task is complete | `/clear` |
| The user tells you to stay in this session | `/compact <what to keep>` |
| The task is not complete, and the /context value shows that more than half of the window is in use | `/handoff`, then a new session |
| The task is not complete, and you or the user stop work | `/handoff`, then `/clear` |
| The user tells you to continue a session of an earlier day | a new session that starts from `HANDOFF.md` or from the task in Beads |

`/handoff` is a skill, and you start it. `/clear` and `/compact` are built-in commands, and the user runs them (rule 5). You cannot read the size of the context yourself. Ask the user for the `/context` value when a session becomes long.

Install the [handoff](https://github.com/odinokov/handoff) skill at user scope:

```bash
git clone https://github.com/odinokov/handoff.git ~/.claude/skills/handoff
```

- After the installation, ask the user to start Claude Code again.
- `/handoff` writes or updates `./HANDOFF.md`. The file has five sections: Goal, Current Progress, What Worked, What Didn't Work, Next Steps.
- Add `HANDOFF.md` to the global gitignore. It is session state, not project content.
- Start the new session from the same repository root. The first instruction is: `Read ./HANDOFF.md, start at §5 Next Steps`.
- `/compact` reads the full conversation. For this reason, it is an expensive request when the context is large. `/clear` has no cost.
- Add a `Compact instructions` section of two lines to `~/.claude/CLAUDE.md`: what to keep and what to remove.

## E4. Clear prompts: prompt-improver (item 23)

[prompt-improver](https://github.com/severity1/claude-code-prompt-improver) is a Claude Code plugin with hooks and one skill. Its hook adds an evaluation text to each prompt of the user. If the prompt is clear, the work continues. If the prompt is not clear, you start the `prompt-improver` skill and ask the user a maximum of six questions with the AskUserQuestion tool. For this reason, you do not do work on an incorrect task.

```bash
claude plugin marketplace add severity1/severity1-marketplace
claude plugin install prompt-improver@severity1-marketplace --scope user
```

These are the shell forms of the `/plugin` commands (rule 5). After the installation, ask the user to start Claude Code again.

- Requirements: Claude Code 2.0.22 or later, and `python3`. The license is MIT.
- The plugin has hooks for three events: UserPromptSubmit, PreToolUse (for EnterPlanMode and Bash) and SubagentStart. Each hook only adds text to the context. The README calls this text a nudge. A nudge does not stop or change a tool call.
- Plugin hooks also operate in subagents. For this reason, the PreToolUse hook runs before each Bash command of a subagent.
- A prompt that starts with `*` gets no evaluation. Slash commands and prompts that start with `#` also go through without change.
- Tell the user to put `*` before a prompt that is complete, for example a task text from Beads.
- You start the `prompt-improver` skill. For this reason, do not add `disable-model-invocation` to it (section A1, step 7).
- Test: ask the user to send the prompt `fix the error`. The evaluation text must come with the prompt, and you must ask questions.

Prompt weight:

- The hook text is not in the permanent context, but each prompt of the user pays for it. Each notification of a finished background subagent also gets the text (version 0.6.1, Claude Code 2.1.330, observed on 2026-11-23).
- The evaluation text of version 0.6.1 has a minimum of 1,118 characters and a copy of the prompt (test of 2026-11-23, with one nudge). Other nudges can add more text.

The nudges give general advice about the method of work. CLAUDE.md and the system prompt of a subagent are specific to this project, and they have priority. Use this table:

| Nudge | What it adds | Rule in this harness |
| --- | --- | --- |
| `improve` | questions for a prompt that is not clear | Use it. The skill sends its search work to the built-in Explore agent, which uses the model of the main session (section D2). Give code search to `scout` and web search to `web-researcher`. Do not use Explore. |
| `ask-user-question` | a question to the user when the user must make the decision | Use it. It agrees with rule 7. |
| `output-readability` | the conclusion first, then sections and tables | Use it. |
| `background-exec` | a long command runs in the background | Use it. |
| `approach-assessment` | a selection of the method: a subagent or direct work | The rules for the orchestrator in section D1 stay. You do not change project code yourself. |
| `workflow` | a plan first, and a model for each stage | Section E1 gives the plan procedure. Do not set the `model` parameter in a subagent call (section D2). |
| `plan-mode` and `plan` | plan mode, and a short plan without the decision history | Use them in a plan session. The plan file in `docs/plans/` keeps the decisions (section E1, step 4). In a task session, the task from Beads has a plan: do not make a second plan. |
| `subagent-routing` | text at the start of a research or planning subagent | The system prompt of the subagent has priority. |

- Put one item in the "Harness protocol" section of `~/.claude/CLAUDE.md`, as the template `assets/claude-md.user.md` shows. It gives the priority and the search rule.
- The README gives no setting that disables one nudge. Do not change the files of the installed plugin, because an update replaces them.
- If a nudge has an effect that this section does not permit, write it in the setup log. Then the user decides: keep the tool or remove it (rule 11).
