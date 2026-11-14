# Panda Plan execution-readiness evaluation

Date: 2026-11-14 (Asia/Bangkok).

## A. Baseline assessment

[Capability audit and contract](../../../docs/panda-plan-refinement.md#execution-readiness-and-release-gate-refinement-2026-11-14).
Original Plan already handles source inspection, dependencies, exact cross-task
interfaces, signature/error consistency, task acceptance, artifact/ignore rules,
scope propagation and execution modes. Historical B's signature defect already
had a correction; it was not treated as a new gap. Prior proportion trials were
partial and scope-revision behavioral trials were not run. The narrow additions
are evidence traceability, explicit risk-based gate planning and plan readiness.

## B. Architecture and behavior changes

Stable task IDs and Requirement → Task → Check → Evidence links extend existing
planning. Tasks state discriminating checks and relevant dependencies/fixtures.
Small changes may stay one inline task; complex architecture records ownership,
invariants and compatibility checks. A skill-local conditional reference defines
release gates as pending evidence. Release still owns actual release assessment;
Execute/Test keep their work. Native/subagent execution contracts and permissions
are retained without requiring any peer skill or new runtime.

The first candidate generated a separate live-release task but called the whole
plan execution-ready despite that task being unavailable. Candidate v2 keeps
future release-only checks in gates unless included in requested execution scope,
and assesses readiness across every task in the saved execution scope. The first
candidate and its unfavorable observation remain preserved, not replaced.

## C. Files modified

- `skills/panda-plan/SKILL.md`: consolidated planning/validation contract and readiness.
- `skills/panda-plan/references/release-gates.md`: conditional gate design and evidence boundary.
- `tests/scenarios/cases.json`: three new scenarios; existing cases unchanged.
- `tests/fixtures/plan-campaign/`: synthetic versioned CLI with a deliberately uncovered strict-policy defect.
- `tests/fixtures/plan-gate-scope/`: scope fixture extended with stale gate/traceability references; original retained.
- `tests/test_tooling.py`: regression for blind inputs excluding reviewer controls.
- `tests/reviewer/check_plan.py`, `tests/reviewer/plan-control/campaign.py`: green-suite distinguishing check and correct control, excluded from task inputs.
- `docs/panda-plan-refinement.md`, `docs/routing.md`, `tests/evaluation.md`: audit, ownership and evaluation protocol.
- This result directory: frozen instruction versions, actual trial artifacts, checks and limitations.

## D. Evaluation results

Fresh task-performing contexts received only TASK.txt, the copied fixture and
explicit instruction path (plus conditional references). Reviewer expectations
were not supplied. Same inherited model/settings, no overrides; exact model
revision, temperature, budget and per-run token use were not exposed/controlled.
Tools and fixture inputs matched in paired cases. Agents could inspect files and
run local checks; evidence-boundary explicitly prohibited tests. Task agents did
not delegate. The author reviewed actual plans and verified source boundaries;
this is not independent blind scoring or a reliability benchmark. RUN records
are agent-reported command summaries, not raw host transcripts.

Original, candidate, candidate-v2 and candidate-v3 snapshots are separate. Candidate-v2 changes
conditions after the first observed failure, so it is a regression check rather
than an unchanged-arm comparison. Candidate v3 changes only the handoff opener:
the review/mode request must end the user-facing response, not appear only in the
saved artifact. This responds to omitted prompts in v1 handoff and v2 B trials. No no-skill baseline was run in this session.

### Actual trials

| Case / arm | Observation | Result / limitation |
| --- | --- | --- |
| PLAN-RELEASE-GATES / original | Correct policy, meaningful failure checks and three blocking gate bullets; existing test weakness found | Pass on core correctness; no explicit gate IDs or check/evidence matrix |
| PLAN-RELEASE-GATES / candidate v1 | Explicit task/check/evidence/gate links; also unavailable live T4 while whole plan labeled ready | Partial; readiness/scope defect, extra proposed defensive policy |
| PLAN-RELEASE-GATES / candidate v2 | Two cohesive tasks; exact interface; discriminating matrices; live check only in gates; unspecified validation stays outside scope | Pass on scenario rubric; handoff prompt incomplete |
| PLAN-PROPORTION / original | Two tasks; second is mainly regression verification | Partial on task cohesion; correct/scoped |
| PLAN-PROPORTION / candidate v1 | One task including useful checks; no matrix/gates | Pass on cohesion; still verbose relative to likely implementation |
| B / candidate v1 | Valid one-task plan but report-filename instruction changed the output destination | Partial: harness contamination; default-path behavior not scored |
| B / candidate v2 | Default dated plan, one coherent task, preserved approval/pending semantics; no source edits | Core pass; omitted final review/mode prompt; substantial single-function plan |
| B / candidate v3 | Valid default-path one-task plan; read-back and baseline tests; asks for review but no mode choice | Core pass; mode-offer observation remains partial/confounded |
| PLAN-ERROR-BOUNDARY / candidate v1 | Sentinel permits omitted/None/blank ValueErrors, tests separate cases | Contract pass; proposed python command's executable availability unverified |
| PLAN-SCOPE-REVISION / candidate v1 | Removed required legacy work; preserved runtime fallback/history; paths explicitly provisional | Pass; no source/tests supplied, so behavior Not Run |
| PLAN-GATE-SCOPE-REVISION / candidate v2 | Removed legacy task/gate/evidence links; runtime/history gates remain pending | Pass; plan partially ready pending source contracts |
| PLAN-EVIDENCE-BOUNDARY / candidate v1 | No tests/writes; rejects green-suite claim; pending revision/environment gates | Pass on evidence boundary; repeats future release-task issue fixed in v2 |
| PLAN-HANDOFF / candidate v1 | Saved dated plan; surfaces malformed-CSV/multiline policy ambiguity instead of fabricating resolution | Partial: no mode menu; actual execution blocked by domain decision |
| PLAN-INTERFACES / candidate v2 | Exact parser/validator/import/report contracts and dependencies; 1,904-word plan; physical-line CSV policy explicitly proposed | Core interface pass; oversized and multiline support excluded without external policy confirmation |
| PLAN-HANDOFF-PRESET / candidate v2 | Keeps sequential subagent choice; asks for plan review without reopening menu | Pass; no implementation |
| PLAN-HANDOFF / candidate v3, initial harness | Review ask and native recommendation/request present; no two-option menu | Partial on literal rubric; future delegation capability ambiguous in harness |
| PLAN-HANDOFF / original, explicit future capability | Review request, both modes and native recommendation with ready request | Pass under changed, matched host-capability prompt |
| PLAN-HANDOFF / candidate v3, explicit future capability | Review request, both modes and native recommendation with ready request | Pass; no superiority over original established |
| PLAN-NONTRIGGER / Lead | Direct KeyError answer; only Lead/source loaded; no plan/writes | Pass; routing control, not final Plan activation |
| EXEC-PLAN-RESUME / unchanged Execute | Exact saved-plan implementation; 15 tests and existing reviewer 30/30 | Pass; original inventory/tests/requirements unchanged |
| EXEC-SCOPE-REVISION / unchanged Execute | Removes deferred migration, implements invalidation-before-refresh; six tests | Pass; parent reran suite and checked runtime plan/source |
| Generated candidate-v2 plan → unchanged Execute / synthetic fixture | Shared policy/recovery and CLI tests implemented; parent rerun six tests passes | Handoff compatible; task acceptance partial because Python 3.9 unavailable; boxes honestly unchecked |

The two original/candidate pairs use identical task prompts and fixtures. Correctness
was strong in both original arms; evidence tables and task grouping changed, not
proven general correctness. Candidate v2's gate case also omits an explicit
review/mode question in its final response. Candidate v3 targets that observed
omission without repeating the mode rules. V3's first handoff rerun explicitly asked for review and recommended native, but
still omitted a two-option menu. The harness had forbidden delegation without
clarifying whether that restricted future mode availability; this is a potential
confound with the skill's capability-gated offer. A separate matched original/v3
pair adds the same explicit future-host-capability statement to both prompts.
Those inputs differ from the earlier run and are not substituted for it. Both matched runs offered native/subagent-driven modes, asked for review and
recommended native with a ready request. This supports compatibility and the
importance of explicit host constraints; it does not show v3 outperforms original.
Across this session there were 22 fresh task contexts, including changed candidate
versions and capability conditions; these are not 22 independent comparisons of
the final skill. Final v3 was directly exercised for B and handoff; other behavioral
trials used the retained v1/v2 snapshots, whose core contracts v3 leaves unchanged.

[Full saved artifacts](trials/), [chat answer excerpts](trials/chat-answers.md),
[instruction hashes](sha256.json) and [boundary comparisons](boundaries.json).
Chat-only answers are excerpts, not full transcript archives. One B v1 harness
instruction to save the final answer was interpreted as the plan destination;
B v2 removed that instruction and used the correct default dated path.

Not Run in this session: no-skill model baseline; original paired arms for the
remaining cases; fresh EXEC-PLAN-SUBAGENT execution (historical evidence exists);
Python 3.9 runtime and live-provider checks. Prepared cases are not counted as
model trials. No statistical or token-use comparison is claimed.

### Structural and fixture checks

- Skill metadata, local references, manifests and scenario coverage: 25 skills validated.
- Panda tooling: 32 tests passed (including new blind-preparation regression).
- Codex CLI discovery: 25 plugin and standalone skill names match; no global installation performed by this task. The tool reported existing plugin installation state as true.
- Reviewer fixture: supplied suite passes both faulty/control; strict-unproven assertion fails only for faulty; correct control satisfies timeout/cancellation, empty strict, permissive, proven and unrelated-exception checks.
- Blind preparation: 14 cases × 3 arms = 42 workspaces; fixture bytes preserved and reviewer keys absent. This is packaging validation, not 42 model trials.

Exact command log and final verification results are retained in `checks.txt`.
`python3 -B tests/results/plan-handoff/verify_exec.py /tmp/panda-plan-execute-resume tests/fixtures/plan-execute`
returned 30/30. Parent reran `python3 -B -m unittest -v` inside the generated-plan
execution and scope-execution workspaces: six tests passed in each. The
trial-specific `verify_generated.py` rejects original campaign orchestration:
one strict-unproven assertion failure and six missing-recovery exception errors,
with the delivered helper supplied only to allow imports. Correct implementation
passes separately. These expected defect results are retained as failures, not
misreported as ordinary test passes. Parent Python resolved to 3.15; task agents
reported 3.14.7 where recorded. Supported-runtime evidence is still absent.
Not-run checks remain Not Run; intentionally defective fixture behavior is not a
Suite tooling failure. No actual release gate has been passed by this evaluation.

## E. Compatibility and regression findings

Default/explicit/chat-only Markdown artifacts, task checkboxes and exact interface
contracts remain text-consumable by unchanged Execute. Historical comparison
results are retained under plan-refinement and plan-handoff; they are not new
results for this candidate. Scenario preparation covers all existing Plan and
relevant Execute cases. Actual behavioral coverage is limited to the trials below;
unrun scenarios are explicitly distinguished from preparation.

## F. Remaining risks

Small-scope outputs may still be too long; one B trial produced a matrix and inline
compatibility gate despite being a one-function change. The short-chat candidate
used one task while the original used two, but a single sample cannot establish
improvement. Both original and candidate already identified the new green-suite
gap and compatible policy; explicit table fields alone are not proof of better
engineering. Candidate v1 also proposed extra defensive null/string/malformed-input
policy beyond the required contract, visibly labeled proposed but adding scope.
Candidate v2 kept those unspecified policies outside scope. No token savings,
reliability, deployment safety or broad performance improvements are measured. Python 3.9 runtime and live-provider checks are unavailable/not run.

## G. Practical demonstration

Synthetic example grounded in `tests/fixtures/plan-campaign/`, not a real provider.
All implementation checks below are **planned**; these are expected outcomes.

| Task | Dependency / exact interface | Acceptance and discriminating verification |
| --- | --- | --- |
| T1: implement shared policy and campaign enforcement (REQ-1/2) | None; produce `evaluate_policy(report: dict, *, require_all_proven: bool) -> bool`; retain `run_campaign(config: dict, transport) -> dict` | Strict succeeds only for nonempty all-proven reports; permissive succeeds. Unit assertions for empty and mixed lists reject `all([])` and first-item-only bugs; assert strict-unproven exit 2 and unchanged input. |
| T2: recover transport failures (REQ-3) | T1 policy; consume one `transport.evaluate()` call | TimeoutError/InterruptedError yield one unproven safety report, strict 2/permissive 0; counting doubles reject retries; RuntimeError must propagate. |
| T3: preserve CLI compatibility (REQ-2/4) | T1/T2; retain `main(config_path: str, transport) -> int`, consume shared policy | Capture JSON from temp configs; returned code equals JSON exit_code; old/default config stays 0 and schema_version 1 shape remains. Assert call count and unchanged config. |

Traceability: REQ-1 → T1 → policy matrix → expected passing assertions;
REQ-2 → T1/T3 → API/CLI contract checks → matching signatures/JSON/return values;
REQ-3 → T2 → controlled failure checks → one-call/no-mutation/propagation results;
REQ-4 → T3 and gates → compatibility/live checks → revision/environment-linked artifacts.

| Defined gate | Condition / future evidence | Blocking |
| --- | --- | --- |
| G1 functional / REQ-1–3 | `python3 -m unittest -v` after implementation, including discriminating assertions and source review, tied to candidate revision | Yes |
| G2 compatibility / REQ-2/4 | Old config and schema/CLI assertions on supported Python 3.9; record interpreter/revision/output | Yes |
| G3 provider / REQ-4 | Future real-provider check using verified environment tooling; sanitized candidate-revision/environment/results artifact | Yes; environment and credentials unavailable |

T1 is unblocked for a separately authorized implementation; T1 → T2 → T3 is
execution-ready under the stated contract. G1–G3 remain defined, not passed. A
native Execute handoff can implement these tasks and report G2/G3 evidence gaps;
no provider action is authorized by this example. No task requires new infrastructure.

## H. Final verdict

**Complete for the scoped skill implementation and local verification.** The
new task/evidence/gate contracts are supported by actual plans, a discriminating
fault/control fixture, and a plan-to-Execute implementation probe. Existing artifact,
resume and runtime-scope contracts remain usable; no peer skill edits were needed.

Behavioral results are mixed: readiness separation was corrected after an observed
failure; concise plans and CSV-policy treatment remain inconsistent; matched
handoff behavior was already good in the original. General behavioral superiority,
repeatability, token savings and real release readiness are **not established**.
Fresh subagent execution and supported-runtime/live checks remain Not Run here;
the corresponding existing contract/historical results are preserved. The smallest
next evaluation is repeated short/ambiguous-policy trials against frozen final
instructions, followed by an independently scored execution comparison, rather
than more templates or generic rules.
