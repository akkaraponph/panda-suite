# v1.1.0 task trials

Fifteen real native task-agent trials were run on 2026-11-08. Each case/arm used
a fresh context (`fork_turns=none`), equivalent fixture inputs, inherited settings,
and directory-only/no-network instructions. Baseline loaded no skill instructions;
specialist/Lead loaded isolated copies retained beside each answer. Models were
not given reviewer criteria, other answers, or parent conversation history.

Model identifier/settings details and raw token telemetry are not exposed by this
harness. Agents share host filesystem access; isolation was instructed, not
independently enforced. ACTIONS.md files are agent-authored evidence, not raw
orchestration transcripts. Cases ran with other host activity, so cross-arm timing
comparisons are uncontrolled. No statistical improvement or token-saving claim
is supported. Baselines already succeeded on their tested tasks.

## Results

| Case/arm | Actual outcome and limits |
| --- | --- |
| [SEC-MIXED baseline](SEC-MIXED/baseline/ANSWER.md) | Identified injection and unsafe pickle loading, rejected protected/sample paths; dependency evidence reconciled. Static code reasoning, no unsafe payload execution |
| [SEC-MIXED specialist](SEC-MIXED/specialist/ANSWER.md) | Same supported flaws, separate severity/confidence, safe in-memory injection and owner-bound-query checks, actionable mitigation/regression guidance |
| [SEC-REPORT baseline](SEC-REPORT/baseline/ANSWER.md) | Correctly rejected stale/withdrawn advisory claims and retained failed scan; added code findings beyond requested dependency triage, reducing scope precision |
| [SEC-REPORT specialist](SEC-REPORT/specialist/ANSWER.md) | Correctly limited report to dependency triage: resolved version outside range, withdrawn dev advisory, failed scan not clean |
| [SEC-NONTRIGGER Lead](SEC-NONTRIGGER/lead/ANSWER.md) | Answered focused bound-query explanation without a Sec load or audit report |
| [PERF-ALGORITHM baseline](PERF-ALGORITHM/baseline/ANSWER.md) | Proposed ordered dictionary optimization for exact integers, preserved generic helper, ran tests/equivalence and repeated local timings |
| [PERF-ALGORITHM specialist](PERF-ALGORITHM/specialist/ANSWER.md) | Same valid optimization; included measured peak-allocation cost and retained empty-input timing regression, plus explicit workload limits. Delivered diff independently applied and tests passed |
| [PERF-QUERIES original specialist](PERF-QUERIES/specialist/ANSWER.md) | Candidate batching preserved tenant/order/duplicates/missing IDs/500-ID chunks in fake-repository checks and retained snapshot gate. Delivered hunk failed ordinary `git apply --check`; it needs `--unidiff-zero`. Original failure retained |
| [PERF-QUERIES revised specialist](PERF-QUERIES/revised-specialist/ANSWER.md) | After an instruction change requiring verification of the delivered diff, fresh trial supplied a normally applicable patch and verified behavior on a disposable copy. Snapshot gate remains; no real DB speed claim |
| [PERF-APPLY specialist](PERF-APPLY/specialist/ANSWER.md) | Applied exact-int optimization only, added meaningful boundary tests, five tests passed; repeated synthetic timings and peak memory reported with trade-offs |
| [PERF-MEMORY specialist](PERF-MEMORY/specialist/ANSWER.md) | Measured bounded recent deque versus growing history with safe synthetic allocations; preserved shared ownership and retention-policy uncertainty. No invented production leak or destructive patch |
| [PERF-NONTRIGGER Lead](PERF-NONTRIGGER/lead/ANSWER.md) | Explained bounded deque in two sentences without profiling or Perf load |
| [D Review regression](D/specialist/ANSWER.md) | Located removed owner guard and supported high-impact unauthorized cancellation finding; source unchanged |
| [K Write regression](K/specialist/ANSWER.md) | Produced developer guide, ran two existing tests and a usage example; rejection remains proposed; source/tests unchanged |
| [Research conflict regression](RESEARCH-CONFLICT/specialist/ANSWER.md) | Reconciled v2/v3 device-code capability and configured/default retries with citations; kept deployment unknown |

Each trial includes its actual TASK.txt, fixture and instruction snapshot, ANSWER.md,
ACTIONS.md, and metadata.json containing artifact hashes and final input-state
comparison. Hashes verify retained files and final state, not absence of transient
changes. Only PERF-APPLY changed application/test fixture files, as authorized.
K created a requested guide; some trials retained disposable local check harnesses.

## Demonstrated improvement and regression evidence

The one observed instruction weakness was testing an in-memory candidate without
verifying the delivered patch's applicability. Perf now explicitly checks the
serialized diff on a disposable copy. The original and revised instruction copies
and outputs remain available; this is one local regression, not general efficacy
proof. The revised trial changed instructions and is labeled separately rather
than silently replacing the failed result.

Run the independent retained-artifact check:

```sh
python3 tests/results/v1.1.0/verify_patches.py
```

It applies the algorithm and revised batching diffs to disposable original
fixtures and reruns supplied behavior tests; it reproduces the original query
patch's ordinary-apply failure as an explicit retained negative control. It also
reruns the five tests in the delivered applied-optimization trial. Additional
independent tenant/order/duplicate/missing/500-ID boundary checks were performed
during the release review; no real database or production benchmark was run.

## Unrun and next checks

The complete catalog contains 47 scenarios; only the trials above ran models.
Preparing 141 case/arm workspaces validates preparation, not task success.
Remaining security scope/placeholder/ambiguity and unavailable-profiler cases are
Not Run as separate model trials. Existing skills outside the selected regressions
have packaging/standalone checks, not new behavioral coverage. Useful next work is
repeat sampling of patch applicability and workloads/DB plans from a real project,
not claiming all vulnerabilities or bottlenecks can be detected from these fixtures.
