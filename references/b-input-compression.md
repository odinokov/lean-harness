# B. Compression of incoming data

Keep the output of each tool small before it goes into the context. Output stays in the context for all later turns of the session, and each turn reads it again. Three methods do this for three inputs: shell output, large tool results and binary documents. B1 and B2 use no hook and no extra tool. They use the quiet forms of commands and the output limit of Claude Code.

## B1. Quiet commands: shell command output (item 1)

Output below the inline limit of B2 stays in the context for the rest of the session. An example is a test run that prints 400 lines of passed tests. Use the quiet form of each command that runs often.

- Write the quiet forms of the build, test and lint commands in the "Commands" section of the project CLAUDE.md (Part 2, step 1). Claude Code loads that file in each session. The main session, `implementer` and `reviewer` read it.
- `test-runner` and the other subagents with `omitClaudeMd: true` do not read CLAUDE.md. The orchestrator copies the quiet form into the delegation message and into the verification command of each Beads task (section E1, step 5).
- Keep the error visible. Claude Code shows a failed command as an excerpt of about 10,000 characters from its head and its tail, with no file (B2). Use the flags that print failures in short form. Use `tail` for a log whose end holds the result.
- Before you write a form into CLAUDE.md, examine `--help` of the tool and run the command one time. Give the test command to `test-runner`. If a form fails or hides the error, keep the old form.
- If the project already uses a quiet form, keep it.

The rows are examples that this guide did not test. Check each one with `--help` of the tool in the project:

| Tool | Quiet form |
| --- | --- |
| pytest | `pytest -q --tb=short` |
| Vitest | `npx vitest run --reporter=dot` |
| Jest | `npx jest --silent` |
| npm scripts | `npm run <script> --silent` |
| Cargo | `cargo build -q`, `cargo test -q` |
| Go | `go test ./...` (without `-v`) |
| Maven, Gradle | `mvn -q -B <goal>`, `./gradlew <task> -q` |
| git | `git status -sb`, `git log --oneline -20`, `git diff --stat` |
| make | `make -s <target>` |
| A long log | `set -o pipefail; <command> 2>&1 \| tail -n 80` |

- A pipe returns the exit code of its last command, so `<command> 2>&1 | tail -n 80` exits 0 when the command fails, and Claude Code treats the failure as a success. `set -o pipefail;` first makes the pipe return the failure.
- This method has no hook. If the agent often runs the long form of a command, tell the user. The user can decide to add a PreToolUse hook for that one command. This guide does not install it.

## B2. The output limit of Claude Code: large tool results (item 17)

Claude Code keeps large Bash output out of the context by itself (Claude Code documentation, Tools reference, "Output limits"):

| Result | What goes into the context |
| --- | --- |
| Success | Up to about 30,000 characters. Above that: the path of a file in the session directory and a preview of up to 2,000 characters. Claude reads or searches the file when it needs more |
| Failure | Up to about 10,000 characters. Above that: an excerpt of that size from the head and the tail, with no file |

- Exit code 1 counts as a success only for `grep`, `rg`, `egrep`, `fgrep`, `find`, `diff`, `test`, `[`, `git diff` and `git grep`. Each other command that exits with 1 counts as a failure.
- `bashOutputMaxChars` (a setting, Claude Code 2.1.261 or later, up to 128,000) sets the inline limit of a successful command and the read-back window. `BASH_MAX_OUTPUT_LENGTH` (`env`, default 30,000, up to 150,000) sets only the read-back window. When `bashOutputMaxChars` is set, Claude Code ignores `BASH_MAX_OUTPUT_LENGTH`.
- Keep the defaults. A higher limit puts more output into the context for the rest of the session. If phase 1 found a higher value in `~/.claude/settings.json` (`bashOutputMaxChars`, or `BASH_MAX_OUTPUT_LENGTH` in `env`), tell the user and recommend its removal. The user decides.
- To use a large result more than one time, search the file with Grep or grep, or read parts of it with Read and its `offset` and `limit` parameters. If a summary is sufficient, give the file path to `log-digester`.
- Logs, test runs, dumps and web pages go to subagents (section D). Their output stays in the context of the subagent. For one short command, a subagent costs more than the command, because the subagent loads its own prompt and tools. Run a short command in the main session, in its quiet form (B1).
- Check: run `seq 1 20000` in Bash. Its output has 108,894 characters. The result must be a file path and a preview, not the numbers. If the numbers come inline, the limit is higher than the default. If a plugin or a hook changes Bash output (for example Context Mode), it catches this output, and this check shows its behavior, not that of Claude Code: not applicable while a plugin or a hook that changes Bash output is enabled; write that in the log.

## B3. MarkItDown: documents (item 7)

[MarkItDown](https://github.com/microsoft/markitdown) converts PDF, Word, Excel, PowerPoint and other formats to Markdown.

```bash
uv tool install 'markitdown[all]'
markitdown input.pdf -o .agent-out/md/input.md
```

- Do not read a binary document directly. Convert it first.
- Give the conversion to the `doc-converter` subagent (section D). It returns the path and the table of contents, not the text.
- Then read only the necessary parts with Grep, or with Read and its `offset` and `limit` parameters.
- If MarkItDown is already installed in another environment (for example conda) with the PDF and Office extras, keep it.
- Install the CLI, not `markitdown-mcp`. The CLI adds nothing to the permanent context.
- MarkItDown reads files and URLs with the permissions of the current process. Convert only files from the user or from the work directory.

## Why this guide does not use RTK and Context Mode

Earlier versions of this guide installed RTK in B1 and Context Mode in B2. This version replaces them for these causes (`references/sources.md` gives the sources, read on 2026-11-25):

- Third-party measurements of complete tasks did not show a lower cost for RTK, and showed more tokens for Context Mode:
    - RTK: +13% total cost on 100 SWE-bench Verified tasks ([Dasein](https://github.com/daseinlabs/code-compression-bench)).
    - RTK: +7.6% median cost per task at low effort and +0.1% at high effort (p=0.99), on 80 clean pairs of 86 SkillsBench tasks ([JetBrains](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/)).
    - RTK: an estimate, not a measurement. A counterfactual replay of 500 sessions of its author estimated that RTK saves about 0.5% of spend. The page computed it from the published per-command rates of RTK (60 to 99 percent, depending on the command). It did not measure task success ([Codepointer](https://codepointer.dev/p/cutting-llm-token-costs-with-rtk)).
    - Context Mode: workload tokens rose 94% and 46% on the tasks of Stet, with Codex CLI. These are tokens, not cost ([Stet](https://www.stet.sh/blog/gpt-56-token-saving-modes)).
- The output that these tools compress is a small part of the cost. Each turn reads the full context again from the cache, so the number of turns and the size of the context set the cost (Marmelab, Anthropic).
- The two tools install PreToolUse hooks for Bash, and both can change the command. When two hooks return `updatedInput` for one call, the hook that finishes last wins ([issue 83353](https://github.com/anthropics/claude-code/issues/83353), reported on Claude Code 2.1.220, closed).
- This guide tested Context Mode itself (version 2.2.1, Claude Code 2.1.330, 2026-11-23). Its hooks redirected WebFetch, curl and large reads. In the main session, it cut a full Read of a 7.5 KB file. In subagents, it cut long Bash output. These are causes of robustness, not of cost.
- Context Mode has the Elastic License 2.0, and the engine and the proxy of RTK have BUSL-1.1. Context Mode needed Node.js 24.15.
