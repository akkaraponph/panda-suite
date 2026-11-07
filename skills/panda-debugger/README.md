# PANDA DEBUGGER

PANDA DEBUGGER is an Agent Skill for investigating software defects from evidence before changing code. It guides an agent through **Understand → Reproduce → Trace → Root Cause → Fix → Verify** and produces a report that separates observed results from untested explanations.

It works across programming languages and frameworks using the tools available to your agent, such as tests, a browser, logs, and traces. When evidence is missing, it says what still needs to be checked.

## Install

### Codex marketplace

Add this repository as a marketplace source on your machine, then install its plugin:

```sh
codex plugin marketplace add akkaraponph/panda-debugger
codex plugin add panda-debugger@panda-debugger
```

### Claude Code marketplace

Add the same repository as a marketplace source in Claude Code, then install its plugin:

```sh
claude plugin marketplace add akkaraponph/panda-debugger
claude plugin install panda-debugger@panda-debugger
```

Start a new Codex or Claude Code session after installing.

### Manual skill copy

Run these commands from the directory where you want to clone the repository. They install the Skill for Codex and Claude Code without the plugin commands:

```sh
git clone https://github.com/akkaraponph/panda-debugger.git
cd panda-debugger

PANDA_CODEX_SKILLS="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$PANDA_CODEX_SKILLS/panda-debugger" "$HOME/.claude/skills/panda-debugger"
rsync -a skills/panda-debugger/ "$PANDA_CODEX_SKILLS/panda-debugger/"
rsync -a skills/panda-debugger/ "$HOME/.claude/skills/panda-debugger/"
```

To update a manual installation, run `git pull --ff-only` in the clone, then repeat the `PANDA_CODEX_SKILLS`, `mkdir`, and `rsync` commands above. Start a new agent session to use the updated files.

## Use

1. Open the project that has the bug in a new Codex or Claude Code session.
2. Start your request with the name that matches your installation:

   | Agent and installation | Start your request with |
   | --- | --- |
   | Codex (plugin or manual copy) | `$panda-debugger` |
   | Claude Code plugin | `/panda-debugger:panda-debugger` |
   | Claude Code manual copy | `/panda-debugger` |

3. Describe the bug. Include what you expected, what happened instead, and how to reproduce it. Add an error message, failing test, log, screenshot, or relevant file path if you have one. You can still start with an incomplete report; the agent will inspect the available project files and say what evidence is missing.

For an investigation without code changes, copy this prompt and replace the example details:

```text
$panda-debugger Investigate the search results bug. When I type a new query,
results from the previous query sometimes replace the newer results.
Expected: results always match the latest query.
Reproduce: type two different queries quickly on the search page.
Find the cause, show the evidence, and propose a fix. Do not edit code yet.
```

The example uses the Codex name. In Claude Code, replace the first word with the matching name from the table.

If you want the agent to make the fix as part of the same request, say so explicitly:

```text
$panda-debugger Investigate and fix this bug: when I type two search queries
quickly, results from the first query sometimes replace the latest results.
Expected: results always match the latest query.
Reproduce: type two different queries quickly on the search page.
Add a regression test, run the relevant checks, and report what passed.
```

The agent reports the cause with a confidence label, the evidence it found, and the checks it actually ran. An investigation-only request ends with a proposed fix for your approval. A request to fix the bug authorizes the agent to edit and verify the code. If a check cannot run or the cause remains uncertain, the report should say so. For a complex execution path, you can also ask for a Mermaid flowchart.
