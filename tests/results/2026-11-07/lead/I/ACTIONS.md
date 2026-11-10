# Actual actions and evidence

Evaluation context is shared across assigned cases; these are not independent samples. All operations use supplied local artifacts. Instructions were loaded by reading files, not by a programmatic skill invocation.

Relevant skill/reference paths read:
- skills/panda-lead/SKILL.md
- skills/panda-debugger/SKILL.md
- skills/panda-debugger/references/investigation-guide.md
- skills/panda-debugger/references/backend-evidence.md
- skills/panda-debugger/references/report-template.md

Initial case artifact SHA-256:
- TASK.txt: d9870f315afce677f5b4bfeec95fdd097881b94ad46886a441f48e98f61f5bb8
- README.md: 0a412a4a8ac541f5fc00936cdb867680c90cdc2867216c6ae0cfbcb100015869
- transfer.py: 3ee53bc14182ef1062307d5115fb4740513f14fbc3b707d602e189efede73caf
- test_transfer.py: 536f31ce03e7372c5fa62a7f361c807f017f818d4b2dc536c575bef8cc6b6d69

```sh
cat skills/panda-lead/SKILL.md skills/panda-debugger/SKILL.md skills/panda-debugger/references/investigation-guide.md skills/panda-debugger/references/backend-evidence.md skills/panda-debugger/references/report-template.md
```

Exit status: 0

```text
---
name: panda-lead
description: Coordinate engineering and product delivery when a request spans discovery, planning, implementation, review, or documentation, or the user wants help choosing a Panda workflow.
---

# Panda Lead

Select the smallest workflow that delivers the user's requested outcome. This
skill coordinates; specialists own their methods. A focused explanation or tiny
edit can be handled directly without another skill or a project plan.

## Route and act

1. Identify the requested outcome, evidence, constraints, and existing
   authorization. Inspect relevant current artifacts before asking for missing
   information. Ask only where ambiguity materially affects correctness or scope.
2. Respect an explicitly named specialist. Otherwise use the table below. For
   overlap, route by the artifact the user wants, not by a keyword in their prompt.
3. Load only the selected skill through the host's documented discovery or
   instruction-reading mechanism. Use native delegation when available,
   authorized, and helpful. Reading instructions is not programmatic invocation.
   If a skill is absent, say so and explain any ordinary assistance you can still
   provide; never claim that the absent skill ran.
4. For a compound request, order dependent activities and carry forward a compact
   [handoff](references/handoff.md). A feature build may need plan → execute;
   an existing approved plan needs execute. Add review or documentation when
   requested or required by the project's acceptance criteria. Run independent
   activities separately only when host capabilities and authorization permit.
5. Compare delivered artifacts and actual verification with the requested
   outcome. Report implemented, verified, partially verified, blocked, or not
   started work accurately. Include remaining decisions or risks.

| Requested outcome | Skill |
| --- | --- |
| Explore an idea, assumptions, alternatives | `panda-brainstorm` |
| Ordered implementation work and acceptance criteria | `panda-plan` |
| Implement authorized work | `panda-execute` |
| Diagnose unexpected behavior | `panda-debugger` |
| Find defects in a change | `panda-review` |
| Assess unnecessary complexity | `panda-simplify` |
| README, developer guide, runbook | `panda-write` |
| Technical contracts or design specification | `panda-spec` |
| User journey instructions | `panda-manual` |

Use `buddhist-method` only at a relevant uncertainty, repeated failure, pressure,
or complexity decision. Do not load it as a mandatory stage. For routing conflicts
or changed requests, read [routing decisions](references/routing.md).

Investigation, planning, review, and recommendations do not authorize source
changes. An explicit implementation request authorizes relevant reversible edits;
carry that permission forward without asking again. Destructive operations,
publication, deployment, production changes, and external side effects require
authorization covering those actions. A new request can narrow earlier scope.
---
name: panda-debugger
description: Investigate frontend and backend bugs across programming languages using available source, runtime, browser, log, and test evidence. Use for exceptions, failing tests, API errors, incidents, or unexpected behavior that needs a proven root cause.
---

# PANDA DEBUGGER — Debugging Investigator

Act as a senior software engineer investigating a defect. **Understand the problem first. Prove the root cause. Propose the fix; edit only when authorized.** Keep confirmed facts, hypotheses, and unknowns separate throughout the investigation.

## Workflow

Move through these phases in order. Record what was observed at each phase; a phase may be limited by unavailable access or evidence, but must not be silently skipped.

1. **Understand.** Establish expected and actual behavior, affected inputs and environment, onset, frequency, and scope. Inspect the repository and supplied artifacts before asking for information already available there. State initial hypotheses as hypotheses; do not propose a fix yet.
2. **Reproduce.** Find the entry point and existing tests. Attempt the smallest safe reproduction when feasible, recording the command or steps, environment, and actual result. If it cannot be run, say why and continue with the evidence available. Never label a static inference as an observed reproduction.
3. **Trace.** Follow data and control flow from input to failure, including validation, transformations, state changes, error handling, transaction boundaries, external calls, and concurrency where relevant. Distinguish the failure location from the origin of the defect. Cite precise file locations or supplied artifacts for material claims.
4. **Identify root cause.** Test each plausible explanation against supporting and contradicting evidence. Label a cause **CONFIRMED** only when evidence connects the proposed mechanism to the observed failure, such as a focused experiment or a complete observed trace supported by code. Reproducing the symptom alone does not confirm its cause. Use **LIKELY** when a key causal check is missing and **UNKNOWN** when evidence is insufficient. Separate the primary cause from contributing factors.
5. **Propose a fix and request approval.** After the cause analysis, describe the smallest change, affected files, why it addresses the cause, regression risks, and a verification plan. A request to debug or investigate is not permission to edit application code or tests. Ask the user to approve this concrete fix before editing. If the user has already explicitly asked to implement or fix this bug, that request counts as approval; do not ask again. If the cause is still UNKNOWN, ask for the missing evidence before proposing code edits. Avoid unrelated refactoring and silent business-rule changes.
6. **Verify after implementation.** Once implementation is authorized, add or update a regression test when it meaningfully captures the defect, run the original failure scenario and relevant tests, and check important edge cases. Record each actual command, result, and limitation. A proposed test is **Not Run** until executed; a fix is **verified** only after relevant checks pass.

Do not run destructive commands, change production data, or trigger external side effects without authorization. Never invent logs, source locations, behavior, reproduction, or test results. Revise the analysis when new evidence contradicts it. If evidence remains insufficient, state exactly what is needed to resolve the uncertainty.

## Language and tool adaptation

Use the same evidence gates for any programming language or framework. Discover the project's actual entry points, build and test commands, dependency setup, and runtime from its code and documentation. Do not assume commands from the examples in this Skill apply to the user's project.

Choose the most direct safe tools available in the current agent harness: source search and file reads for static tracing; the project's test runner or debugger for reproduction; a browser for observable UI behavior; and available logs, traces, database, queue, service, or connector tools for backend paths. Follow each tool's access rules; do not assume a shell or a named tool exists. A particular tool is never required just because it appears in an example. If a needed capability is missing, use existing artifacts, label the check **Not Run**, and explain the evidence gap. Do not claim the workflow can confirm a cause that the available tools cannot observe.

## Reporting

Write the report in clear B2-level English. Use short, direct sentences and common words. Keep code names exact, but explain technical terms when readers need them. Lead with a short **Root cause at a glance** bullet list: one plain-English sentence per cause, with its confidence label. Put the primary cause first. If the evidence supports several possible causes, list them as separate **possible causes** and name the check that would decide between them. Do not make a confirmed cause look like a guess.

Use [the report template](references/report-template.md) for a substantial investigation. Keep each section concise and mark unavailable evidence explicitly. For a small bug, compress the presentation while preserving the causal trace, confidence level, verification status, and remaining risk.

For a path with several components, branches, or asynchronous steps, include a small Mermaid flowchart in **Execution Flow** when it makes the cause easier to understand. Show only steps supported by evidence; label inferred steps. If a diagram could help but is not needed in the main report, end with a brief optional offer: “I can also draw a Mermaid flowchart of this path if useful.” Skip the diagram and offer for simple cases. Never let a diagram replace the root-cause explanation or evidence.

Read [the investigation guide](references/investigation-guide.md) when the defect involves multiple layers, transactions, asynchronous work, or conflicting evidence. It contains phase gates and examples of how to separate observations from inferences.

For a frontend issue with an accessible application, read [the browser investigation guide](references/frontend-browser.md) and use the available browser tools to observe the real page. For a backend issue that crosses storage, queues, or services, read [the backend evidence guide](references/backend-evidence.md). If access is unavailable, state which checks could not be performed instead of claiming a full runtime investigation.
# Investigation guide

Use this guide when a bug spans several components or the visible exception may be downstream of the defect.

## Evidence ledger

For each material statement, identify its basis:

| Kind | Meaning | Example |
|---|---|---|
| Observation | Directly seen in supplied artifacts or a command's output | A stack trace names `service.go:42`; a test failed with a specific assertion. |
| Inference | Follows from observations and code, but was not directly observed | A missing commit likely explains unchanged balances. |
| Hypothesis | A possible cause still needing a discriminating check | A duplicate worker may be processing the same job. |
| Unknown | Evidence or access is missing | The production database isolation level is unavailable. |

Quote only the relevant log lines and cite repository paths with line numbers where possible. Do not treat example snippets, comments, or an expected test result as proof of runtime behavior.

## Phase gates

### Understand → Reproduce

State what should happen, what happened, affected conditions, and which evidence supports those statements. If expected behavior is unclear, infer it only when code, tests, or a specification establishes it; otherwise ask a targeted question.

### Reproduce → Trace

Record exact steps or commands and outcomes. If reproduction is unsafe, unavailable, or too costly, say so. A stack trace supplied by the user is evidence of a reported failure, not a reproduction performed by the agent.

### Trace → Root cause

Map input → entry point → transformations and dependencies → failure. Inspect callers and producers of bad values, error propagation, and state transitions. For a database operation, inspect the start, use, commit or rollback, and error checks of a transaction. For asynchronous work, inspect delivery, deduplication, acknowledgement, and shared-state boundaries. Focus on the relevant boundaries rather than exhaustively tracing unrelated code.

### Root cause → Fix

For each candidate, ask: Does it explain the observed behavior? What evidence contradicts it? What check would distinguish it from competing explanations? Mark the cause CONFIRMED, LIKELY, or UNKNOWN. A LIKELY cause supports a conditional recommendation; it does not support a claim that the defect was proven.

For an investigation-only request, finish the causal explanation and a file-level fix and test plan, then ask for approval before editing. Do not use an approval question in place of investigation. If the user explicitly requested implementation, proceed under that authorization.

### Fix → Verify

Connect the change to the causal mechanism. Check the original failure, normal behavior, and the important boundary cases. Use existing test conventions. Report each test as Passed, Failed, Not Run, or Blocked with its actual command or reason. A static review may support a proposal, but cannot establish a runtime fix.

## If investigation stalls

Provide the current causal trace, confidence level, and the smallest missing artifact or experiment that would resolve the uncertainty. Do not fill gaps with invented implementation details or a generic list of possible causes.
# Backend evidence and confidence

Use this guide when a backend defect involves an API, database, queue, transaction, external service, or concurrent worker.

Adapt the boundary checks to the actual system. An entry point may be an HTTP request, RPC call, command, scheduled job, event, or embedded function; storage may not be a SQL database. Use the logs, traces, state tools, and test harness that the project actually provides.

## Follow one failing operation

1. Identify the request, job, or event ID and the input that triggered the failure. Correlate logs, traces, and database or queue observations for that operation when access is available.
2. Trace entry point → validation → service logic → state change or dependency → failure. Note where errors are handled and where the symptom becomes visible.
3. Inspect the relevant boundary: transaction begin and commit or rollback, affected rows, retries and acknowledgements, external side effects, locks or idempotency, and configuration differences. Check only boundaries that matter to this failure.
4. Name competing explanations and choose a safe check that separates them. A focused test, controlled reproduction, or observed trace can establish the causal chain. A matching stack trace or repeated symptom by itself cannot.

Do not inspect or change production records without authorization. When runtime access is missing, use source and supplied logs to narrow the cause, then state the smallest additional observation needed.

## Confidence labels

- **CONFIRMED:** The evidence shows how this mechanism produced the reported failure. Give the input, key state transition, and result, or cite a focused experiment that rules out the main alternative.
- **LIKELY:** The code and observations fit this mechanism, but an important causal step or competing explanation remains untested. Name that missing check.
- **UNKNOWN:** The available evidence cannot rank the explanations reliably. List the next useful observation without guessing.

The status of a symptom and the status of a cause can differ: a failure can be reproduced while its cause remains **LIKELY**. Separate the primary cause from factors that made the failure more likely or more damaging.
# Bug Investigation Report

Write in clear B2-level English. Prefer short sentences and familiar words. Keep code names exact. Explain a technical term briefly if it matters to the conclusion.

## Root cause at a glance

- **[CONFIRMED / LIKELY] Primary cause:** One plain-English sentence that explains why the bug happens. For LIKELY, name the missing check.
- **[UNKNOWN] Leading hypothesis:** Use this label when the cause is not established. State the check needed to decide.

Use one bullet per cause. Put a confirmed or likely primary cause first; if none is established, lead with a clearly labeled hypothesis. Do not show unused bullets in the final report.

## 1. Problem Summary

State the defect, affected path, and conditions. Mark any unverified user report as reported.

## 2. Expected vs Actual Behavior

| Expected | Actual | Basis |
|---|---|---|
| … | … | Specification, test, log, or direct observation |

## 3. Evidence

List the relevant log lines, stack frames, code locations, runtime observations, and test outputs. Separate facts from inferences.

## 4. Reproduction

Give steps or commands, environment, and observed result. If not reproduced, state **Not reproduced** and explain the limitation.

## 5. Execution Flow

`Input → entry point → processing → dependency or state change → failure location`

Identify where the defect originates and where the symptom appears.

If several components, branches, or asynchronous steps make the path hard to follow, add a small Mermaid flowchart here. Label any inferred step. Keep the written explanation and evidence alongside it.

## 6. Root Cause Analysis

Use one bullet per material cause, in the same order as the opening summary. Keep the first line short; add only the details needed to support it:

- **[CONFIRMED / LIKELY] Primary cause: …**
  - **Why this caused the bug:** …
  - **Evidence:** …
  - **What is still unclear:** … (omit if nothing remains unclear)
- **[LIKELY / UNKNOWN] Possible cause or leading hypothesis: …**
  - **Evidence for and against it:** …
  - **Check needed:** …

If a separate defect helped cause the failure, label it **Contributing factor**. Do not present possible causes as equal choices when the evidence identifies a primary cause.

## 7. Proposed Fix

Explain the smallest change, why it addresses the cause, affected files, relevant alternatives, regression risk, and verification plan. State **Approval needed** before editing for an investigation-only request. If the user already explicitly requested implementation, record that authorization and the change made.

## 8. Test Cases

| Test Case | Scenario | Expected Result | Status |
|---|---|---|---|
| TC-01 | Original failure | … | Not Run |
| TC-02 | Normal behavior | … | Not Run |
| TC-03 | Important edge case | … | Not Run |
| TC-04 | Regression scenario | … | Not Run |

Use only relevant rows; do not imply that proposed tests ran.

## 9. Verification Results

List executed commands or steps and actual results. If nothing was run, say **Not run** and why. Do not claim the fix is verified without passing relevant checks.

## 10. Remaining Risks

List unresolved questions, evidence gaps, and plausible regression risks. If none remain, state the scope of the verification that supports that conclusion.

For a complex flow without a diagram, you may close with: “I can also draw a Mermaid flowchart of this path if useful.” Omit this offer when the path is simple or a diagram is already included.

```

```sh
cat TASK.txt README.md transfer.py test_transfer.py
```

Exit status: 0

```text
Use panda-lead. Read its instructions at skills/panda-lead/SKILL.md through available instruction-loading tools. Load only relevant references or specialist instructions. Do not claim a programmatic skill invocation.

Investigate why the payment process fails. Do not change code. Work only with the supplied local transfer fixture; do not attempt any production operation.
# Runnable backend bug: transfer reports success without saving balances

This fixture is intentionally broken. Give an evaluating agent only this directory, without the answer key in `tests/evaluation.md`.

## Run

```sh
python3 -m unittest discover -s . -p 'test_*.py'
```

Run the command from this directory. It uses Python's standard library and a temporary SQLite database. The success-path test should fail because the reported transfer does not persist both balances.

## Request to the agent

Investigate the failed test. Trace the database transaction, identify the root cause with evidence and a confidence label, and propose a minimal fix and regression checks. Do not edit files. State which commands you ran and their results.
"""Intentionally broken transfer implementation for investigation practice."""

import sqlite3


def transfer(db_path, from_id, to_id, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")

    connection = sqlite3.connect(db_path)
    try:
        connection.execute("BEGIN")
        sent = connection.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_id),
        )
        if sent.rowcount != 1:
            raise ValueError("source account not found")

        received = connection.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_id),
        )
        if received.rowcount != 1:
            raise ValueError("destination account not found")
        return None
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
import sqlite3
import tempfile
import unittest
from pathlib import Path

from transfer import transfer


class TransferTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.db_path = Path(self.directory.name) / "accounts.sqlite"
        with sqlite3.connect(self.db_path) as connection:
            connection.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER)")
            connection.executemany(
                "INSERT INTO accounts (id, balance) VALUES (?, ?)",
                [(1, 100), (2, 20)],
            )

    def balances(self):
        with sqlite3.connect(self.db_path) as connection:
            return [
                row[0]
                for row in connection.execute("SELECT balance FROM accounts ORDER BY id")
            ]

    def test_success_persists_both_balances(self):
        self.assertIsNone(transfer(self.db_path, 1, 2, 25))
        self.assertEqual([75, 45], self.balances())

    def test_invalid_amount_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "amount must be positive"):
            transfer(self.db_path, 1, 2, 0)
        self.assertEqual([100, 20], self.balances())


if __name__ == "__main__":
    unittest.main()

```

```sh
python3 --version
```

Exit status: 0

```text
Python 3.15.0

```

```sh
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Exit status: 1

```text
test_invalid_amount_is_rejected (test_transfer.TransferTest.test_invalid_amount_is_rejected) ... ok
test_success_persists_both_balances (test_transfer.TransferTest.test_success_persists_both_balances) ... FAIL

======================================================================
FAIL: test_success_persists_both_balances (test_transfer.TransferTest.test_success_persists_both_balances)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/tmp/panda-suite-evals-lead/I/test_transfer.py", line 30, in test_success_persists_both_balances
    self.assertEqual([75, 45], self.balances())
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: [75, 45] != [100, 20]

First differing element 0:
75
100

- [75, 45]
+ [100, 20]

----------------------------------------------------------------------
Ran 2 tests in 0.008s

FAILED (failures=1)

```

```sh
python3 -c 'import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch
import transfer
real_connect = sqlite3.connect
class TraceConnection:
    def __init__(self, connection, commit_before_close):
        self.connection = connection
        self.commit_before_close = commit_before_close
    def execute(self, sql, parameters=()):
        result = self.connection.execute(sql, parameters)
        print("execute", sql, parameters, "rowcount", result.rowcount,
              "in_transaction", self.connection.in_transaction)
        return result
    def rollback(self):
        self.connection.rollback()
    def close(self):
        print("before close", self.connection.execute("SELECT id, balance FROM accounts ORDER BY id").fetchall(),
              "in_transaction", self.connection.in_transaction)
        if self.commit_before_close:
            self.connection.commit()
            print("control: explicitly committed before close")
        self.connection.close()
with tempfile.TemporaryDirectory() as directory:
    for control in (False, True):
        path = Path(directory) / (str(control) + ".sqlite")
        with real_connect(path) as connection:
            connection.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER)")
            connection.executemany("INSERT INTO accounts VALUES (?, ?)", [(1,100),(2,20)])
        print("commit control", control)
        with patch.object(transfer.sqlite3, "connect", lambda p: TraceConnection(real_connect(p), control)):
            print("return", transfer.transfer(path, 1, 2, 25))
        with real_connect(path) as connection:
            print("persisted", connection.execute("SELECT id, balance FROM accounts ORDER BY id").fetchall())
'
```

Exit status: 0

```text
commit control False
execute BEGIN () rowcount -1 in_transaction True
execute UPDATE accounts SET balance = balance - ? WHERE id = ? (25, 1) rowcount 1 in_transaction True
execute UPDATE accounts SET balance = balance + ? WHERE id = ? (25, 2) rowcount 1 in_transaction True
before close [(1, 75), (2, 45)] in_transaction True
return None
persisted [(1, 100), (2, 20)]
commit control True
execute BEGIN () rowcount -1 in_transaction True
execute UPDATE accounts SET balance = balance - ? WHERE id = ? (25, 1) rowcount 1 in_transaction True
execute UPDATE accounts SET balance = balance + ? WHERE id = ? (25, 2) rowcount 1 in_transaction True
before close [(1, 75), (2, 45)] in_transaction True
control: explicitly committed before close
return None
persisted [(1, 75), (2, 45)]

```

```sh
python3 -c 'from pathlib import Path; import hashlib; print('"'"'transfer.py'"'"',hashlib.sha256(Path('"'"'transfer.py'"'"').read_bytes()).hexdigest()); print('"'"'test_transfer.py'"'"',hashlib.sha256(Path('"'"'test_transfer.py'"'"').read_bytes()).hexdigest())'
```

Exit status: 0

```text
transfer.py 3ee53bc14182ef1062307d5115fb4740513f14fbc3b707d602e189efede73caf
test_transfer.py 536f31ce03e7372c5fa62a7f361c807f017f818d4b2dc536c575bef8cc6b6d69

```

Final hashes above match the initial artifact hashes for the listed read-only source/tests (or, for M, unchanged plan/tests). Python may create local __pycache__ files; no production state was accessed. ANSWER.md is the actual final response for this workspace.

Shared-context instruction provenance: earlier batched reads across assigned cases also loaded these absolute paths; these loads are not independent evaluations:
- skills/panda-lead/SKILL.md
- skills/panda-debugger/SKILL.md
- skills/buddhist-method/SKILL.md
- skills/panda-execute/SKILL.md
- skills/panda-review/SKILL.md
- skills/panda-write/SKILL.md
- skills/panda-manual/SKILL.md
- skills/panda-lead/references/handoff.md
- skills/panda-debugger/references/investigation-guide.md
- skills/panda-debugger/references/backend-evidence.md
- skills/panda-debugger/references/report-template.md

No grading cases, Suite documentation, baseline results, or other evaluator outputs were read. No Suite repository files changed. A requested RTK.md was absent from the current workspace and checked parent locations.
