# Independent audit of the 34 evaluation artifacts

Audit scope: the original 11 baseline, 10 specialist, and 13 Lead artifacts under `tests/results/2026-11-07`, assessed against `tests/scenarios/cases.json`, raw fixtures, saved implementation artifacts, and relevant `ACTIONS.md` command/evidence records. No Suite or evaluation artifact was edited. This report is an independent inspection of outputs, not an independently repeated evaluation run.

## Material findings

1. **All three original C implementations violate the Unicode separator requirement.** `baseline/C`, `specialist/C`, and `lead/C` use `NFKD(...).encode("ascii", "ignore")` before the separator regex. Independently executing each frozen `artifacts/slug.py` returns `ab` for both `a💰b` and `a—b`; the approved plan requires non-alphanumeric runs to become a hyphen, so the expected result is `a-b`. All four supplied tests really pass, and the documented Café example really returns `cafe-deja-vu`. The defect is incomplete contract coverage, not a fabricated passing test result. This is a real execution/review weakness present in every original C arm; it prevents an unqualified claim that C meets its semantic requirements.
2. **Lead M fixes the same defect, but only after its initial review incorrectly found no significant defect.** `lead/M/ACTIONS.md:440` records the initial review; line 514 records the failing emoji check; line 526 explicitly supersedes that review. The final saved implementation removes combining marks while preserving other characters until the regex replacement. Independently executing it passes the four original tests and returns `a-b` for emoji and em dash separators. The final guide describes the corrected behavior. The intermediate documentation-edit SyntaxError at line 592 is disclosed and corrected. M's delivered state passes the observed requirements; this is evidence of a successful correction in M, not evidence that Lead caused an improvement over C.
3. **Specialist B and Lead B have a small contradictory proposed error contract.** Each proposes the required three-argument `reject(request, actor, reason)` signature while requiring a *missing* reason to raise `ValueError`. Omitting a required positional argument raises Python `TypeError` before function validation can run. Specify whether “missing” means `None`, or use an explicit default/sentinel if omission must become `ValueError`. This is a plan inconsistency, not an implemented runtime defect. Their permission/status/payload requirements and dependency ordering are otherwise useful and correct.
4. **The original routing/context evidence does not establish minimal isolated loading.** Lead H's answer is focused and correct, but its `ACTIONS.md:149` discloses that the shared context had already loaded debugger, execute, review, write, manual, Buddhist, and handoff/reference instructions. Similar shared-provenance disclosures occur in A, I, L and M. F/G/J/K were loaded in a batch containing all four specialists and Lead. These can establish intended route selection, but cannot satisfy an unqualified claim that an individual original task loaded only its needed instructions. M explicitly identifies the unnecessary initial `panda-manual` load at `ACTIONS.md:649`. No per-task token or time measurements exist, so overhead is qualitative only.
5. **Some specialist action narratives contain copied Lead language.** Specialist B says “Lead selected panda-plan”; specialist C says “Lead routed to panda-execute”; specialist D/E describe Lead reuse/routing despite being the specialist arm. Those lines should not be treated as clean per-arm routing provenance. The file lists and runtime outputs still agree with the inspected fixtures. All ten specialist answers equal their corresponding Lead answers after replacing the workspace path prefix; B–E are byte-identical. This is compatible with their disclosed shared evaluation context. I found no copied *incorrect runtime result*, invented route/database implementation, fabricated screenshot, falsely passed unavailable integration, or unsupported production operation.
6. **Baseline G is useful but slightly incomplete against the checklist.** Its manual gives exact labels, steps, confirmation, and accurate browser-unverified status. It does not explicitly present prerequisites; it instead states that how to reach the form is not established. Specialist/Lead G explicitly state that the form must be available and identify role/sign-in as unverified. This is a small manual-completeness gap, not a verification-honesty failure.

## Independent checks performed

- Recomputed all 34 `ANSWER.md` SHA-256 values against `artifact-audit.json`: all match.
- Compared every available raw fixture file with its corresponding `/tmp/panda-suite-evals-{arm}/{case}` source: the manifest's boundaries match exactly. Only `slug.py` differs for the three C tasks and Lead M. Source, tests, requirements, and plans remain unchanged in all other cases. Compared saved `artifacts/slug.py` and `usage.md` with the live evaluation workspaces: all match. This confirms final state, not absence of a transient historical edit.
- Ran `python3 -B -m unittest -v` in `tests/fixtures/approvals`: 2/2 pass.
- Ran the same command in `third_party/panda-debugger/tests/fixtures/backend-uncommitted-transfer`: exit 1; invalid amount passes, success persistence fails, expected `[75, 45]`, actual `[100, 20]`. The intentionally broken upstream fixture was not repaired. Source inspection confirms BEGIN, both updates, return, and close without commit; supplied trace/control evidence agrees with that mechanism.
- Loaded each frozen C/M implementation while running its original unchanged four supplied tests: 4/4 pass for all four implementations. Executed their Café example, emoji, em dash, and a non-ASCII word-boundary probe. C returns `ab` for all three boundary probes; M returns `a-b`.
- Checked the complete review fixtures: `after.py:3–5` lacks the owner check, so an actor whose ID differs from `owner_id` can cancel an unshipped order. All D answers identify this material security regression at a precise location with appropriate high/P1 severity.
- Inspected the complete approval, greeting, and supplied UI-evidence fixtures against the answers: source assertions, role/status/error ordering, shallow-copy behavior, current/proposed rejection distinction, and exact draft UI labels are supported. ACTIONS provide local example/test records where claimed. Historical command execution is reported by those logs; independent reruns corroborate results, not historical timings.

## Per-artifact assessment

Legend: **P** = observed pass; **~** = partial; **F** = observed failure; **—** = not applicable. Correctness is judged against the full source/requirement contract, not only the supplied tests. Evidence means traceability and consistency of material claims; honesty means accurately reporting what was or was not verified. “Shared” in routing/context means the intended route is visible but isolated minimal loading is unmeasured or contradicted by disclosed batching. No aggregate or causal ranking should be derived from this table.

| Arm/case | Correctness | Evidence | Completion | Scope | Verification honesty | Output usefulness | Routing/context overhead | Case observation |
|---|---|---|---|---|---|---|---|---|
| baseline A | P | P | P | P | P | P | — | Correct missing-commit/close mechanism; actual 1 pass/1 fail; read-only. |
| baseline B | P | P | P | P | P | P | — | Ordered local rejection plan with per-task acceptance/verification; proposed additions explicit. |
| baseline C | F | P | ~ | P | P | ~ | — | Four real tests/example pass; Unicode separators are deleted, violating plan. |
| baseline D | P | P | P | P | P | P | — | P1 owner-authorization regression with attacker input and precise line. |
| baseline E | P | P | P | P | P | P | — | Removes forwarding collaborators while retaining public method/admin guard; compatibility risks named. |
| baseline F | P | P | P | P | P | P | — | Useful professional Thai spec; current/proposed/open decisions separated; no invented infrastructure. |
| baseline G | P | P | ~ | P | P | ~ | — | Accurate unverified manual, exact supplied labels; prerequisites not explicit. |
| baseline H | P | P | P | P | P | P | ~ | Focused correct answer; unnecessarily reads requirements and approval tests for label explanation. |
| baseline J | P | P | P | P | P | P | — | Realistic local/module/service alternatives; source-grounded recommendation and assumptions; no execution plan. |
| baseline K | P | P | P | P | P | P | — | Clear English current-service guide with actually executable example; rejection remains proposed. |
| baseline L | P | P | P | P | P | P | — | Rejects unsupported PostgreSQL/HTTP assertion and supplies bounded release wording. |
| specialist A | P | P | P | P | P | P | ~ | Debugger method and trace/control are useful; shared-context disclosure prevents route-purity claim. |
| specialist B | ~ | P | P | P | P | ~ | ~ | Good ordered plan; omitted reason vs required signature error mismatch; copied Lead narrative. |
| specialist C | F | P | ~ | P | P | ~ | ~ | Same semantic separator defect; wrong-file read corrected; copied Lead narrative/shared context. |
| specialist D | P | P | P | P | P | P | ~ | Correct high-severity security finding/reproduction; copied Lead routing language. |
| specialist E | P | P | P | P | P | P | ~ | Good minimal recommendation and 12-case bounded comparison; additional Buddhist references loaded. |
| specialist F | P | P | P | P | P | P | ~ | Accurate Thai current/proposed spec; shared four-specialist instruction batch. |
| specialist G | P | P | P | P | P | P | ~ | Exact labels, prerequisites/unknowns, draft/browser-unverified status; shared batch. |
| specialist J | P | P | P | P | P | P | ~ | Four alternatives and explicit assumptions/open decisions; shared batch. |
| specialist K | P | P | P | P | P | P | ~ | Executed correct guide example; current behavior and proposal clearly separate; shared batch. |
| specialist L | P | P | P | P | P | P | ~ | Source beats authority claim; tests/example bounded; shared instruction provenance. |
| lead A | P | P | P | P | P | P | ~ | Correct debugger route and causal trace/control; unrelated instructions already in shared context. |
| lead B | ~ | P | P | P | P | ~ | ~ | Routes to plan; same omitted-argument inconsistency as specialist B; sequential shared context. |
| lead C | F | P | ~ | P | P | ~ | ~ | Routes to execute and honestly reports four passing tests; same Unicode separator defect. |
| lead D | P | P | P | P | P | P | ~ | Routes to review; high-severity owner defect and safe reproduction; shared context. |
| lead E | P | P | P | P | P | P | ~ | Routes to simplify; access control preserved and compatibility bounded; additional Buddhist reads. |
| lead F | P | P | P | P | P | P | ~ | Routes to spec; accurate Thai artifact, decisions/proposals explicit; shared batch. |
| lead G | P | P | P | P | P | P | ~ | Routes to manual; refuses unsupported fully-verified label; useful bounded journey; shared batch. |
| lead H | P | P | P | P | P | P | ~ | Direct concise label explanation with executed example; original context already contains unrelated skills. |
| lead I | P | P | P | P | P | P | ~ | Debugger selected; actual local failing/passing tests and no production operation; shared context. |
| lead J | P | P | P | P | P | P | ~ | Brainstorm selected; realistic alternatives and bounded recommendation; shared batch. |
| lead K | P | P | P | P | P | P | ~ | Write selected; clear current-service guide with executed example; shared batch. |
| lead L | P | P | P | P | P | P | ~ | Appropriate source/uncertainty discipline; no unsupported persistence/HTTP assertion; shared context. |
| lead M | P | P | P | P | P | P | ~ | Execute/review/write handoffs preserve authorization; final correction and guide verified; unnecessary manual load disclosed. |

## Interpretation limits and follow-up

The 34 artifacts came from shared case-group contexts, including cross-arm contexts. All ten specialist/Lead answer pairs are identical after workspace-link normalization. These are not 34 independent samples, do not establish independent repeatability, and cannot demonstrate causal superiority or improvement due to a skill. Timing/token data per task is unavailable. No quantitative overhead, efficiency, or performance conclusion is supported.

The main skill weakness directly observable here is incomplete semantic verification in C: a four-test green result was treated as local completion even though a requirement-derived Unicode separator case failed. Planning also needs a consistency check between proposed signatures and error behavior. Routing restraint is written into Lead instructions, but the original batched evaluation does not measure isolated restraint; its recorded unnecessary manual load is a real overhead observation. Other major safety/evidence boundaries survived the observed tasks.

A separate fresh focused H artifact was also inspected at `/tmp/panda-suite-evals-focused/H`. Its ACTIONS list only TASK.txt, Lead instructions, and service.py as content loads, with a filename-only inventory; its short answer is correct and accurately says no tests were run. This supports one isolated successful focused route. It is supplemental evidence, not one of the original 34 artifacts, and does not retroactively make the original H context isolated.

Preserve the original C failures. Add a requirement-derived Unicode separator regression and rerun explicitly as a new evaluation rather than silently repairing these frozen artifacts. Clarify the B omission contract. Keep future per-task instruction-load provenance separate so routing overhead can be evaluated directly.
