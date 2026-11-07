# Buddhist Skill Success Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give all 15 Panda skills observable success conditions and concise Buddhist practices that guide difficult decisions and completion.

**Architecture:** Integrate essential actions directly into each standalone SKILL.md, using Iddhipāda 4 as the shared foundation and one primary situational principle per skill. Keep the full Buddhist method optional. Evaluate current and revised instructions against identical evidence before claiming behavioral improvement.

**Tech Stack:** Markdown skills, Python 3 tooling, unittest, PyYAML, jsonschema, existing fixture preparation and SHA-256 upstream verification.

**Spec:** The agreed design in this conversation is captured in the design contract and skill matrix below. Read this whole document before execution. Existing compatibility requirements are in `docs/skill-contract.md`.

## Global Constraints

- Scope is 15 `panda-*` skills. `buddhist-method` remains the source of fuller teachings.
- “Essential rules are local to each skill so copying a specialist directory alone does not break it.” — `docs/skill-contract.md`.
- “A specialist may name an optional peer capability, but does not require another skill, a parent folder, or Panda Lead.” — `docs/skill-contract.md`.
- “Verification includes actual commands/results or an explicit not-run/blocked reason.” — `docs/skill-contract.md`.
- Preserve existing user authorization and each specialist's scope, confidence labels, and evidence requirements.
- Existing README.md modifications and untracked images/ were present during planning. Inspect current Git state and preserve those edits.
- RTK.md was referenced by supplied instructions but absent from the workspace root during planning. Recheck at execution and apply it if available.
- No new runtime service, mandatory peer loading, global installation, publication, or package version change is required.
- Instruction length is a review signal. Word counts cannot establish token savings or behavioral quality.

## Review Focus

1. A specialist copied alone must retain its success checks when Buddhist Method is unavailable. Task 5 owns standalone-copy checks.
2. A tiny request must receive proportionate work without a ceremonial checklist. Tasks 2 and 4 own the trivial-case evaluation.
3. Missing tools must lead to an honest partial result and useful remaining work. Tasks 2 and 4 own the unavailable-tool case.
4. User pressure and repeated failures must trigger evidence review while preserving authorized progress. Tasks 2 and 4 own the pressure and retry cases.
5. Pinned upstream restoration must preserve authentic upstream bytes and detect accidental local drift. Task 1 owns archive, restore, and mutation tests.

## Design contract

Treat “harness” here as written decision and completion guidance carried by each skill. This plan adds no executable orchestration layer.

Use Iddhipāda 4 as a design foundation with these observable actions:

| Basis | Required practical behavior |
| --- | --- |
| Chanda | Identify the user's requested outcome and what counts as done. |
| Viriya | Continue authorized useful work through recoverable obstacles, choosing a changed approach when evidence warrants it. |
| Citta | Keep attention on current evidence, scope, dependencies, and the task being completed. |
| Vīmaṃsā | Compare the actual artifact and observations with success conditions, then correct supported gaps. |

Consolidate existing workflow and completion wording before adding text. Prefer one compact paragraph near task entry and one skill-specific decision instruction at the relevant workflow step. Name the Buddhist principle once with a plain-language action. Existing good instructions may satisfy the action and need only a precise attribution or clarification. Do not copy the entire four-basis table into every skill.

The agent need not narrate the principles or add religious terminology to user deliverables. The instructions guide actions. Completion can include unresolved decisions or missing observations when the requested analysis is complete and those limits are explicit. Continued effort remains bounded by scope, authorization, and actual dependencies.

## Skill matrix

All paths below are `skills/<skill>/SKILL.md`. This matrix specifies behavior, not claims of measured improvement.

| Skill | Success evidence | Principle, trigger, and required action | Evaluation condition |
| --- | --- | --- | --- |
| panda-brainstorm | Assessable direction, trade-offs, deciding unknowns | Kalāma: a premise drives the recommendation; inspect evidence and name what would change the choice | Microservices proposed for slow releases while approval waits dominate |
| panda-debugger | Causal mechanism with justified confidence, or exact missing causal observation | Yoniso Manasikāra: several causes fit; select an observation that distinguishes them | Unchanged transfer balances with competing persistence and cache explanations |
| panda-requirements | Confirmed rules have observable acceptance, conflicts remain explicit | Kalāma: stakeholder claims conflict; preserve sources and identify the deciding business question | Cancellation permission differs between two supplied policies |
| panda-plan | Ordered tasks cover requirements, dependencies, and verification | Vīmaṃsā: ready to finish a plan; map every acceptance condition to a concrete task/check | Rejection API omits a required reason while promising a validation error |
| panda-execute | Authorized deliverables complete with actual verification status | Appamāda: late-task pressure; recheck remaining acceptance and artifact completeness | Slug implementation passes supplied tests but misses Unicode separators |
| panda-review | Material defects have triggering conditions and causal evidence | Upekkhā: pressure to approve; inspect guards and report only supported findings | Owner check removed alongside harmless formatting |
| panda-simplify | Demonstrable complexity reduction preserves needed behavior | Majjhimā Paṭipadā: abstraction or shortcut proposed; justify the smallest shape against actual cases | Remove pass-through layer while preserving authorization |
| panda-impact | Traced dependencies, confidence, coverage limits, mitigations | Anāgataṃsa-ñāṇa: contract changes; inspect immediate consumers and persisted-data compatibility | Renamed event field with an uninspected external consumer |
| panda-release | Readiness derives from release-specific evidence and explicit gates | Sati-Sampajañña: prior evidence reused; match revision and environment before accepting it | Passing tests belong to a different commit |
| panda-spec | Current, proposed, and open contracts are internally consistent | Kalāma: a contract is asserted; connect current claims to source and label proposals | Unsupported endpoint supplied as if already implemented |
| panda-write | Reader can follow source-supported documentation and assess limits | Kalāma: command or behavior stated; verify against repository evidence | README example names an unsupported CLI option |
| panda-manual | Steps and outcomes match observed or supplied journey evidence | Sati-Sampajañña: next UI step chosen; confirm visible state and provenance | Browser absent and screenshots omit recovery behavior |
| panda-test | Assertions discriminate required behavior and report execution honestly | Vīmaṃsā: suite passes; check whether a known faulty behavior would still pass | Test asserts status only while unauthorized state mutation remains possible |
| panda-skill-lab | Comparison artifacts support bounded conclusions and next improvements | Anatta: evaluation contradicts a favored revision; retain unfavorable evidence and revise/remove ineffective wording | Revised skill performs worse on a simple request |
| panda-lead | Requested outcome delivered through proportionate routing and complete handoffs | Chanda: request spans phases or changes; re-anchor to current deliverable and carry authorization/evidence forward | User narrows a feature request to explanation only |

## File structure and responsibilities

- Modify all 15 `skills/panda-*/SKILL.md` files for local guidance and completion criteria.
- Preserve Buddhist Method files and upstream lock hashes for their existing destinations.
- Create `vendor/panda-debugger/SKILL.md` as the pristine pinned Debugger file. Move only its lock destination there before changing the active skill.
- Modify `upstream-lock.json`, `tests/test_tooling.py`, and provenance documentation to distinguish the pristine upstream artifact from the Suite-maintained active Debugger instructions.
- Create `tests/scenarios/buddhist-success.json` with reviewer-only expectations for all matrix cases and cross-cutting cases.
- Create `tests/fixtures/buddhist-success/<case-id>/` with only task evidence. Reuse existing fixtures where their inputs support a case exactly.
- Modify `scripts/prepare-evaluation.py` to support the new case catalog and immutable instruction snapshots without exposing expectations.
- Modify `tests/evaluation.md` for comparison protocol.
- Create `tests/results/buddhist-success/summary.md` when evaluations are performed or explicitly recorded as Not Run.
- Modify `docs/skill-contract.md`, `docs/integration.md`, `docs/skill-catalog.md`, and `docs/verification.md` to describe the final contract and actual checks.

## Task 1 — Preserve Debugger provenance before local enhancement

**Files:** Create `vendor/panda-debugger/SKILL.md`. Modify `upstream-lock.json`, `tests/test_tooling.py`, and `docs/integration.md`.

**Interfaces:** Existing `verify(root)` and `restore(root)` from `scripts/vendor-upstreams.py` retain their signatures. The single Debugger SKILL.md lock entry retains source, revision, and sha256, with destination `vendor/panda-debugger/SKILL.md`.

- [ ] Inspect current working-tree changes and run the existing vendor verifier. Resolve any pre-existing hash mismatch explicitly before archiving.
- [ ] Add a regression test that expects the Debugger lock destination above, checks its bytes against its original sha256, and checks that the active Debugger skill remains present for installation. Run the test and confirm the current destination makes it fail.
- [ ] Copy the verified active Debugger bytes into the vendor path and change only that record's destination. Document that local enhancements apply to active Suite instructions and that the archive retains upstream provenance.
- [ ] Add a mutation assertion that modifying archived bytes causes `verify(root)` to report a sha256 mismatch. Retain the existing path-escape, clean-restore, and modified-upstream refusal tests using an appropriate pinned record.
- [ ] Run `python3 scripts/vendor-upstreams.py` and `.venv/bin/python -m unittest discover -s tests -p 'test_tooling.py' -v`. Expected vendor success and all tooling tests passing. Use a temporary root for destructive mutation tests.
- [ ] Commit only this task's paths with `chore: preserve debugger upstream before suite enhancements`.

## Task 2 — Prepare blind, comparable evaluation inputs

**Files:** Modify `scripts/prepare-evaluation.py`, `tests/test_tooling.py`, `tests/evaluation.md`. Create `tests/scenarios/buddhist-success.json` and task-evidence fixture directories.

**Interfaces:** Extend `prepare(root, destination, case_id, arm, *, catalog=None, skill_root=None)` with optional Path arguments. Defaults preserve current calls. Add CLI options `--catalog` and `--skill-root`. Skill root directly contains skill directories. Arms remain baseline, specialist, and lead. Current and revised specialist comparisons use different immutable skill roots, recorded in run metadata.

- [ ] Add failing tests for custom catalog selection, explicit skill-root instruction paths, default compatibility, rejection of unknown cases/arms, existing destination refusal, and exclusion of reviewer checks and other answers from TASK.txt and fixture copies.
- [ ] Implement optional arguments and CLI wiring using the existing preparation flow. Resolve catalog and skill-root paths once. Baseline prompts contain no skill-loading instruction.
- [ ] Add one case for each matrix row, with id, skill, fixture, prompt, and checks matching the existing JSON format. Use distinct ids prefixed `BS-`.
- [ ] Add cross-cutting cases `BS-tiny`, `BS-missing-tool`, `BS-retry`, and `BS-pressure`. Pin concrete expected behaviors: brief direct response, explicit unrun check plus independent progress, changed diagnostic observation after unproductive retries, and evidence-supported completion status under pressure.
- [ ] Keep ground truth only in the reviewer catalog. Fixtures contain source facts, logs, requirements, and user prompts sufficient to solve the task. Do not place check lists, principle names, or desired conclusions into task evidence unless the user prompt genuinely supplies them.
- [ ] Run tooling tests. Prepare one baseline and one specialist workspace in new temporary destinations using the new CLI options. Inspect TASK.txt and copied file inventory. Expected correct instruction path and absence of answer keys.
- [ ] Document that task agents receive isolated fixtures and instruction snapshots without access to reviewer catalogs or other run results.
- [ ] Commit with `test: add blind buddhist success evaluation cases`.

## Task 3 — Implement the two-skill pilot

**Files:** Modify `skills/panda-brainstorm/SKILL.md` and `skills/panda-debugger/SKILL.md`.

**Interfaces:** Preserve names, descriptions, direct-use triggers, Debugger confidence labels, and existing authorization contracts. Task 2 supplies case inputs. Task 1 supplies provenance protection.

- [ ] Snapshot current instructions into a temporary directory outside task workspaces and record content hashes before editing.
- [ ] Write a reviewer checklist for the pilot from the corresponding matrix rows. Inspect current wording and record which actions already exist, which need precision, and which proposed additions duplicate existing instructions.
- [ ] Integrate the four-basis actions through existing workflow and completion wording. In Brainstorm, explicitly connect the deciding assumption to a falsifying observation. In Debugger, explicitly connect the next investigation to competing causes and the outcomes that discriminate them.
- [ ] Add the Buddhist mnemonic with a local plain-language action so optional Method loading carries no essential requirement. Keep user-facing reports focused on task evidence.
- [ ] Run `.venv/bin/python scripts/validate-skills.py` and the vendor verifier. Expected 16 skills valid and pristine upstream hashes valid.
- [ ] Commit with `feat: add success discipline to brainstorm and debugger`.

## Task 4 — Evaluate the pilot and refine the instruction pattern

**Files:** Create `tests/results/buddhist-success/summary.md` and run artifacts beneath that directory. Modify pilot instructions only when actual results justify a change.

**Interfaces:** Use Task 2 catalogs and immutable current/revised skill roots. Store each run in `<case-id>/<arm>/<repeat>/` with TASK.txt, ANSWER.md, ACTIONS.md, and metadata.json. Metadata records instruction/fixture hashes, host, model/settings when available, tool/access constraints, arm, repeat, and revision.

- [ ] Prepare current-specialist and revised-specialist runs for both pilot cases and all four cross-cutting cases. Use fresh contexts and identical task evidence, tools, access, and budgets for each pair.
- [ ] Run two independent repetitions per case and arm, alternating arm order. This is a bounded qualitative comparison, not a statistical significance claim. Use a host-supported runner or authorized delegation. If neither is available, retain runnable inputs and mark behavioral evaluation Not Run.
- [ ] Have a reviewer assess raw outputs against hidden checks after each run finishes. Grade correctness, evidence, completion, scope, verification honesty, usefulness, and observed overhead as pass/partial/failure/not applicable with citations to artifacts.
- [ ] Record whether the revised version makes the intended decision and whether current instructions already achieve it. Retain ties, failures, and execution limits.
- [ ] Revise redundant or harmful wording. Rerun only affected comparisons after revision, saving new hashes and retaining original results.
- [ ] Decide rollout wording. Every skill receives an explicit assessable success condition. Situational guidance is retained where it clarifies an observed or concretely specified decision failure. Unrun comparisons permit a candidate rollout with unverified status, and cannot support an improvement claim.
- [ ] Commit with `test: record success discipline pilot outcomes`.

## Task 5 — Extend skill-specific success guidance across the suite

**Files:** Modify the other 13 Panda SKILL.md files listed in the matrix. Modify pilot files only for the accepted refinement from Task 4.

**Interfaces:** Each skill consumes the same local design contract and its matrix row. No skill consumes another skill's required file or a global checklist.

- [ ] For each skill, map existing entry, workflow, and completion text to the four bases. Replace duplicated wording and add only the missing action needed by its matrix row.
- [ ] Apply requirements/plan/spec changes together, checking unresolved business rules, task acceptance, and current/proposed contracts remain consistent.
- [ ] Apply execute/test/review/release changes together, preserving actual result reporting, evidence freshness, authorization, and the distinction between artifact completion and verification coverage.
- [ ] Apply impact/simplify changes together, bounding foresight to demonstrated dependencies and preserving required behavior.
- [ ] Apply write/manual changes together, preserving source and observation provenance and exact audience-facing labels.
- [ ] Apply skill-lab/lead changes together, preserving unfavorable evaluation evidence and routing proportional to the latest requested outcome.
- [ ] Prepare and assess each skill's matrix case against current and revised snapshots using Task 4's protocol. Report unrun cases explicitly. Investigate regressions before claiming rollout quality.
- [ ] For each of the 15 skills, copy its directory into an otherwise empty temporary skills root and validate skill-local links using the existing validator's `local_links` function. Inspect instructions for essential peer dependencies. Exercise at least one pilot case with Buddhist Method absent.
- [ ] Run structural validation, vendor verification, and all tooling tests. Expected all checks pass. Review the diff for incidental permission changes and added mandatory stages.
- [ ] Commit coherent skill groups separately with messages identifying the group and success behavior.

## Task 6 — Reconcile guidance and publish local verification evidence

**Files:** Modify `docs/skill-contract.md`, `docs/integration.md`, `docs/skill-catalog.md`, `docs/verification.md`, `tests/evaluation.md`, and the comparison summary.

**Interfaces:** Documentation describes the actual final instructions and Task 4/5 artifacts. Existing historical results remain dated and attributable to their original instruction versions.

- [ ] Document Iddhipāda as the design foundation, local operational instructions, optional deeper Method use, and skill-specific observable completion.
- [ ] Add the final principle mapping to the catalog. State that mapping is a design choice and record measured outcomes separately in the evaluation summary.
- [ ] Explain the Debugger archive destination and Suite-local active instructions in provenance guidance. Confirm restore behavior still restores pinned originals to their declared destinations.
- [ ] Record every actual check and result, remaining behavior comparisons, unavailable host observations, and any unresolved regressions. Do not replace historical failures with revised successes.
- [ ] Run `.venv/bin/python scripts/validate-skills.py`, `python3 scripts/vendor-upstreams.py`, and `.venv/bin/python -m unittest discover -s tests -p 'test_tooling.py' -v`. If `.venv` is absent, use an existing interpreter with requirements-dev.txt dependencies or create a temporary development environment and record it.
- [ ] Inspect `git diff --check` and the final scoped diff. Expected valid links, metadata, fixtures, provenance, and backward-compatible preparation calls. A behavior claim requires saved behavioral evidence.
- [ ] Commit with `docs: document buddhist success guidance and evaluation limits`.

## Dependencies and recovery

Task 1 precedes Debugger edits. Task 2 precedes behavioral evaluation. Task 3 precedes Task 4. Task 4 determines the final instruction wording used in Task 5. Task 6 follows the rollout and its actual checks.

Rollback an unsuccessful instruction revision by reverting its scoped commit and retaining evaluation evidence. Restore a damaged pinned archive through the existing verified restore path. Do not use restore as a way to overwrite active local skill changes. No data migration or deployment rollback is involved.

## Completion and self-review

The delivery contains all 15 skill success conditions, actionable relevant principles, standalone compatibility, blind runnable cases, preserved provenance, passing structural/tooling checks, and an honest evaluation summary. Behavioral benefit is reported only to the extent demonstrated by saved comparisons.

Self-review completed against the conversation and repository contracts. All 15 skills are covered by the matrix and Task 5. All five Review Focus conditions have owning checks. Existing prepare calls remain valid through keyword-only optional additions. The provenance design preserves immutable upstream hashes without teaching the verifier to accept arbitrary local drift. Remaining unknowns are model-runner availability and the measured benefit of revised instructions.
