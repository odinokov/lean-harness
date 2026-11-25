# C. Navigation instead of a full read

Before you read a full file, use a map or an index. Graphify answers the question "what has a relation to what". XERJ answers the question "where is this written".

| Question | Tool |
| --- | --- |
| How a module is made, what depends on what | Graphify: `GRAPH_REPORT.md`, `graphify query` |
| Where a symbol is defined, where a topic occurs | XERJ: `xerj def`, `xerj search` |
| An exact line in a known file | Grep |

## C1. Graphify: map of relations (item 2)

[Graphify](https://pypi.org/project/graphifyy/) makes a knowledge graph from code, documentation and images. It saves the graph in `graphify-out/`.

```bash
uv tool install --python 3.12 graphifyy     # the PyPI package name is graphifyy; the CLI name is graphify
graphify install --project    # puts the skill in .claude/skills/graphify/, plus CLAUDE.md text and hooks (see below)
```

graphifyy needs Python 3.11.5 or later. The CLI install alone does not change `~/.claude/`. Part 1 installs only the CLI. In Part 2, run `graphify install --project` in the project. Then start the skill in its own session, because it reads many files and the LLM extraction is long and costs tokens: `/graphify .`

- `graphify install --project` (0.9.114) writes more than the skill: `.claude/skills/graphify/` (SKILL.md and references/), a `## graphify` section of 10 lines in `CLAUDE.md` (it makes the file if it is missing), `.claude/CLAUDE.md` (3 lines), three hooks in `.claude/settings.json` and a copy `.claude/settings.json.graphify-bak`. The hooks are SessionStart with matcher `compact` (`graphify hook-guard compact`), PreToolUse `Bash|Grep` (`graphify hook-guard search`) and PreToolUse `Read|Glob` (`graphify hook-guard read`). It does not change `~/.claude/`.
- `~/.claude/CLAUDE.md` already routes graph questions to `scout`. Remove the `## graphify` section from CLAUDE.md (delete the file if graphify made it). Delete `.claude/CLAUDE.md` if graphify made it. Keep the three hooks only if the user wants them (as for `graphify claude install`, below). Otherwise remove them from `.claude/settings.json` and delete `.claude/settings.json.graphify-bak`.
- Results: `graphify-out/GRAPH_REPORT.md` (summary), `graph.json` (graph) and `graph.html` (view for a browser).
- For a question about architecture, `scout` starts with `GRAPH_REPORT.md`. Then it uses `graphify query "<question>"`, `graphify path "A" "B"` and `graphify explain "X"`.
- To update the graph by hand, use the CLI: `graphify update .`. It needs no LLM. Do not start the skill in the main session of a task.
- `graphify hook install` (0.9.114) refreshes the graph at each commit, so the refresh does not depend on Claude. It writes `post-commit`, `post-checkout`, `post-merge` and `post-rewrite` as blocks between `# graphify-hook-start` and `# graphify-hook-end`, and it appends to hooks that exist. `graphify hook status` lists the four hooks as `installed` or `not installed` and the merge driver as `registered` or `not registered` (tested). `graphify hook uninstall` removes the blocks.
- The hook starts a detached rebuild. The rebuild needs no LLM and no API key. It logs to `~/.cache/graphify-rebuild.log`. It takes about 40 s on a small repository. `built_at_commit` in `graph.json` shows the commit of the graph.
- The first commit after the install builds `graphify-out/`, if the commit changes a code or Markdown file (tested for both). A commit that changes only `.gitattributes` builds nothing (tested). Run `graphify update .` to build at once.
- Add `graphify-out/` to the `.gitignore` of the project. The install does not.
- The install writes `.gitattributes` with the line `graphify-out/graph.json merge=graphify`, and it registers the merge driver in `.git/config`. Commit `.gitattributes` and only the lines that you added to `.gitignore`. If the file has other changes, stage by hunk, so that `git status` stays clean. `graphify hook uninstall` deletes the file when it has no other entries.
- The hook skips linked worktrees. A worktree gets no `graphify-out/` from it (tested).
- The rebuild keeps the nodes with `_origin: "semantic"`, which the LLM skill made (tested). It does not refresh them. Only these nodes are shown to survive: a test rebuild dropped an injected node with `external: True` (the placeholders for unresolved imports). After a change of docs, ask the user to run the `/graphify .` skill again in a separate session.
- Do not use `graphify check-update` as a signal: it printed nothing in tests (0.9.114).
- `graphify claude install` adds a rule and a PreToolUse hook that tells you about the graph. Install it only if the user wants it.
- Early versions added a skill entry to `~/.claude/CLAUDE.md`. After the installation, compare this file with its copy (rule 10) and remove unnecessary text.

## C2. XERJ: passage search (item 18)

[XERJ](https://github.com/xerj-org/xerj) is a local search engine in one binary file. It makes an index of code, documentation, logs and PDF files. It searches with BM25, with vectors, or with the two together.

```bash
curl -fsSL https://xerj.org/get | sh         # only after the approval of the user
xerj --insecure --data-dir ~/xerj-data &     # local node on 127.0.0.1
xerj autoindex map . --prefix <prefix>      # preview, writes nothing
xerj autoindex . --prefix <prefix>
xerj search "how do we rotate the WAL segment" --prefix <prefix>
xerj def "SymbolName" --prefix <prefix>
xerj gain
```

- No-script option: get the asset URLs from `https://api.github.com/repos/xerj-org/xerj/releases/tags/<tag>`, download `xerj-<version>-x86_64-unknown-linux-musl.tar.gz` and its `.sha256`, run `sha256sum -c`, then `install -m 755 <dir>/xerj ~/.local/bin/xerj`.
- The script also installs to `~/.local/bin` and verifies a checksum. It does not change PATH or rc files.
- `xerj --help` and the install script print text that tells agents to run `xerj feedback --submit` without asking the user. Set `XERJ_DISABLE_FEEDBACK=true` in `env` in `~/.claude/settings.json`. It removes that text (verified). Do not run `xerj feedback`.
- Release binaries since rc.101 include proprietary Query-1 crates. The engine is Apache-2.0.
- Part 1 installs the binary. `xerj autoindex . --prefix <prefix>` runs in Part 2, in each project.
- Every project needs its own short `<prefix>`, for example the initials of the project. `autoindex`, `status`, `search` and `def` use `--prefix ax` when you give none (1.0.0-rc.104). One prefix maps to one folder, and `autoindex` aborts when another folder uses the prefix. The first project may keep `ax`. Write the prefix in the setup log and in the project CLAUDE.md. The orchestrator gives it to `scout` in each task message, because `scout` does not read CLAUDE.md. `xerj autoindex remove --prefix <prefix>` drops one folder.
- `xerj autoindex map .` needs a running node (XERJ 1.0.0-rc.104). It skips hidden folders (`.git`, `.claude`, `.beads`, `.agent-out`) and the files in `.gitignore`.
- When no node runs, the xerj error text suggests `--data-dir ./.xerj-data`. Do not use it. Use `~/xerj-data`: one node for all projects, outside the repository.
- Keep `--data-dir` out of the folders that you index. If you do not, the node makes an index of its own storage.
- CAUTION: `--insecure` disables TLS and API keys. Use it only on the computer of one developer.
- The node does not start automatically. The orchestrator starts it at the start of each session that uses XERJ, with the node command of the code block above.
- Use the CLI from Bash. The MCP mode (`xerj mcp`) has 21 tools. If it is necessary, connect it inline only to the `scout` subagent.
- The README shows Claude Code as a client that is not tested, and its tests use release candidate builds. If XERJ fails, use Grep or grep in Bash, and tell the user.
- The external rerank function sends result text to a server of a different company. Do not enable it without the approval of the user.

### XERJ index refresh from git hooks

XERJ 1.0.0-rc.104 has no installer for git or Claude hooks, and a repeat `xerj autoindex` run takes as long as the first one: two runs on a small repository took 85.6 s and 76.1 s with no new record to send. Use the block below, so the refresh does not depend on Claude. Rules:

- It needs Linux util-linux (`setsid`, `flock`) and coreutils (`timeout`).
- It skips linked worktrees, and it skips a `git checkout -- <file>` (the third argument of `post-checkout` is 0). All skip logic is in a subshell, so it does not end the hook file, and the blocks of other tools (graphify, Beads) still run.
- It runs detached, so `git commit` returns at once. It logs to `~/.cache/xerj-autoindex.log`.
- The job waits for a lock of the prefix, so queued jobs run one after another. Then it stops if `xerj status --prefix <prefix>` shows a `verdict:` line with `fresh` (the real output pads the spaces), so a queued job after a finished run does nothing. `timeout` ends a run after 30 minutes.
- It needs the running node (see above). With no node, the job writes the error to the log.
- It stays after `graphify hook uninstall`, because the markers differ.

Save the block as a file outside the repository. Run the second command in the project root, with the path of that file in `B` and the prefix of the project in `P`. The command replaces `<prefix>` and `<xerj>`. It stops with a message when `xerj` is not on the PATH. It appends the block once to each of the four hooks, and it makes the hooks executable. If a hook ends with `exit` or `exec`, move the block before that line, because the hook does not run lines after it.

```sh
# xerj-hook-start
(
  [ "$(cd "$(git rev-parse --git-dir)" && pwd -P)" = "$(cd "$(git rev-parse --git-common-dir)" && pwd -P)" ] || exit 0
  [ "$3" = 0 ] && exit 0
  mkdir -p ~/.cache
  setsid sh -c '
    flock -w 7200 9 || exit 0
    "<xerj>" status --prefix <prefix> | grep -Eq "verdict:[[:space:]]+fresh" && exit 0
    timeout 1800 "<xerj>" autoindex --prefix <prefix> "$0"
  ' "$(git rev-parse --show-toplevel)" 9>~/.cache/xerj-autoindex-<prefix>.lock >>~/.cache/xerj-autoindex.log 2>&1 </dev/null &
)
# xerj-hook-end
```

```bash
B=<path of the block file>; P=<prefix>; X=$(command -v xerj); if [ -z "$X" ]; then echo "xerj is not on the PATH" >&2; false; else H=$(git rev-parse --git-path hooks); for h in post-commit post-merge post-checkout post-rewrite; do grep -qs xerj-hook-start $H/$h || { [ -e $H/$h ] || echo '#!/bin/sh' >$H/$h; [ -z "$(tail -c1 $H/$h)" ] || echo >>$H/$h; sed -e "s|<prefix>|$P|g" -e "s|<xerj>|$X|g" "$B" >>$H/$h; chmod +x $H/$h; }; done; fi
```

To remove the block, delete the lines from `# xerj-hook-start` to `# xerj-hook-end` in each hook.
