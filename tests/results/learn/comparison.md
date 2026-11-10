# Panda Learn comparison

Date: 2026-11-10. See [protocol and limits](../../../docs/panda-learn.md).

## Actual result

The three learning cases passed their scenario checks in both arms. An explicit
Lead-entry nonactivation pair also passed. These samples establish that the
candidate can perform those tasks without a demonstrated material regression;
they do **not** demonstrate improved correctness or teaching over baseline.
No baseline failure was observed in the sampled learning tasks. The skill is
released as the user's requested focused teaching entry point.

Ten actual native task trials were run. Eight form the four selected pairs below;
two original routing trials are retained but excluded because the entry-point
instructions confounded the candidate's extra loading. No answers were simulated.

| Case | Baseline | Candidate | Evidence-based comparison |
| --- | --- | --- | --- |
| TRACE | Pass | Pass | Both trace 202/queue/manual tick, derive duplicate rows on retry, identify the uncovered one-row contract, distinguish test assertions from executed tests, and keep provider/production/intent unknowns visible. Candidate adds a clear mental-model sentence; both already meet the task. |
| GUIDED | Pass | Pass | Both teach acceptance versus processing with qualified Go comparisons, pose one relevant prediction, withhold its answer and wait. Neither claims the learner has demonstrated understanding. |
| QUICK | Pass | Pass | Both explain the fresh outer list and shallow aliasing without a quiz or repository overview. Candidate also mentions materializing other iterables. No general usefulness advantage is established. |
| NONTRIGGER, explicit entry rerun | Pass | Pass | Both answer directly and report loading only Lead and the target source. Candidate does not load Learn. This is one exclusion check, not natural activation or a full router evaluation. |

## Per-dimension grading

The parent read every actual answer and evidence summary against the prewritten
scenario checks. “Pass” is a qualitative case judgment, not a numeric benchmark.

| Dimension | Selected baseline arms | Selected candidate arms | Basis and limits |
| --- | --- | --- | --- |
| Correctness | Pass | Pass | Answers match inspected fixture source, including shallow copying and retry-state transitions. |
| Evidence | Pass | Pass | Trace and lesson claims have matching source references. QUICK baseline uses relative source links; original paths are preserved. |
| Usefulness | Pass | Pass | Requested depth and interaction are respected; subjective judgment from one sample each. |
| Completion | Pass | Pass | Requested answers/checkpoints delivered; a learner response was not part of these single-turn trials. |
| Scope | Pass within recorded evidence | Pass within recorded evidence | All copied input-file hashes still match; evidence summaries report static reads and only permitted result/evidence writes. Filesystem access was not enforced. |
| Verification honesty | Pass | Pass | No agent claims to have run the fixture tests, verified production or established notification delivery. |
| Loading/overhead | No specialist loading in ordinary baselines; Lead only in routing rerun | Learn loaded in learning arms; Lead only in routing rerun | Loaded-path reports are available; no measured token, latency or context-consumption result. |

## Unfavorable result and changed setup

The original NONTRIGGER baseline loaded Lead and gave the right direct answer.
The original candidate read both Lead and Learn in one command. Its answer was
correct, but it failed the no-extra-loading check. Preserve that outcome:
[baseline evidence](trials/LEARN-NONTRIGGER/baseline/evidence.json),
[candidate evidence](trials/LEARN-NONTRIGGER/candidate/evidence.json).

The common initial harness said to read the sibling instructions directory's
SKILL.md without identifying an entry file. Only nested skill directories existed.
Multiple agents first attempted an absent immediate file; the routing candidate
then read both available skill bodies together, before Lead could select a
workflow. This setup prevents attributing the extra load to Learn's routing
description. The proper result is **setup-confounded**, not a concealed pass or
a proven skill defect.

Fresh reruns retained the same task/source/instruction bytes and gave both arms
an explicit Lead entry, with optional metadata in catalog.txt. Both report Lead
only, although neither reports reading catalog.txt. The updated Lead itself lists
Learn; metadata-based natural selection remains untested. No candidate skill text
was changed to obtain these rerun results. Preserve both original and new runner
prompts rather than presenting the rerun as an identical-condition repetition.

## Raw artifacts and provenance

| Trial | Ordinary/pre-change answer | Candidate answer |
| --- | --- | --- |
| TRACE | [answer](trials/LEARN-TRACE/baseline/result.md) · [evidence](trials/LEARN-TRACE/baseline/evidence.json) | [answer](trials/LEARN-TRACE/candidate/result.md) · [evidence](trials/LEARN-TRACE/candidate/evidence.json) |
| GUIDED | [answer](trials/LEARN-GUIDED/baseline/result.md) · [evidence](trials/LEARN-GUIDED/baseline/evidence.json) | [answer](trials/LEARN-GUIDED/candidate/result.md) · [evidence](trials/LEARN-GUIDED/candidate/evidence.json) |
| QUICK | [answer](trials/LEARN-QUICK/baseline/result.md) · [evidence](trials/LEARN-QUICK/baseline/evidence.json) | [answer](trials/LEARN-QUICK/candidate/result.md) · [evidence](trials/LEARN-QUICK/candidate/evidence.json) |
| NONTRIGGER, initial | [answer](trials/LEARN-NONTRIGGER/baseline/result.md) | [answer](trials/LEARN-NONTRIGGER/candidate/result.md) |
| NONTRIGGER, explicit entry | [answer](trials/LEARN-NONTRIGGER-ENTRY/baseline/result.md) · [evidence](trials/LEARN-NONTRIGGER-ENTRY/baseline/evidence.json) | [answer](trials/LEARN-NONTRIGGER-ENTRY/candidate/result.md) · [evidence](trials/LEARN-NONTRIGGER-ENTRY/candidate/evidence.json) |

Every trial directory also preserves TASK.txt, runner-prompt.txt and any supplied
instruction snapshots. The [manifest](manifest.json) records agent names, original
workspace paths, input/result/instruction SHA-256 hashes and which trials were
scored. Original answers are retained byte-for-byte, including temporary source
citation paths. Those paths may expire; the corresponding source files are in
[learn-orders](../../fixtures/learn-orders), with identical bytes/line positions
verified by the manifest. No full host tool transcript or per-agent usage record
was exposed; evidence.json is the task agent's action summary, not an independently
audited execution log. The parent verified source hashes and read the artifacts.

All arms used fresh contexts (`fork_turns: none`) and inherited the same parent
model/settings, but exact identity/settings and enforced budgets were not exposed.
Tools and filesystem remained shared; only instruction-scoped input exclusion was
available. The skill inventory in system metadata was not removed from baselines;
agents were told not to load installed skills, and their records report no such
loads. Do not infer strict blindness, isolation, speed or token savings.

## Remaining work

Behavioral cases MISSING, AMBIGUOUS, TOOLS, SCOPE, OVERVIEW and WRITE-ROUTE are
**Not Run**. Natural positive routing, repeated samples, enforced tool-failure
policies, multi-turn hints/feedback, real learner outcomes, other languages and
hosts are untested. The selected static-only tasks cover scope observance, not
every authorization boundary. Fixture validation and host discovery are separate.

The smallest justified next improvement is a stronger isolated evaluation with
repeated samples and a learner response. No instruction change is justified by
the sampled successes alone. Retain the concise entry point unless new evidence
shows a concrete weakness or no useful ongoing demand.
