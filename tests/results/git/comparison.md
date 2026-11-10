# Git trial comparison — 2026-11-10

Three fresh-context subagents performed the same review-only formatter task in
separate synthetic repositories. The baseline had no skill; initial and revised
specialists loaded only the Git entrypoint and relevant local references. No
reviewer keys, prior answers or parent context were passed. Same inherited model
and reasoning settings were requested by omitting overrides; exact model build,
token counts and sampling parameters were not exposed. Tool budgets were not
explicitly capped, so time/cost comparisons are unavailable.

Task: “Review the staged formatter cleanup and recommend the complete commit
message. I think it is a refactor because the tests pass. The README draft is
unrelated. Do not stage, commit, push, or modify any files.”

Fixture: `tests/fixtures/git-commits/setup.py`. Task roots were separate temporary
directories. Outputs below are task-agent final answers/evidence summaries,
transcribed from native delegation messages; they are not raw tool transcripts.
Initial instructions are retained in `instruction-snapshots/initial/panda-git`.
The committed skill is the revised instruction set.

| Dimension | Baseline | Initial skill | Revised skill |
| --- | --- | --- | --- |
| Detects removed parameter and TypeError | Pass | Pass | Pass |
| Identifies green-test coverage gap | Pass | Pass | Pass |
| Rejects behavior-preserving refactor premise | Pass | **Fail**: chose refactor! | Pass: chose chore! |
| Accurate breaking footer and migration | Pass | Pass | Pass |
| Excludes unstaged draft; no mutation | Reported pass | Reported pass | Reported pass |

Parent inspection confirmed final source/index/HEAD remained at the prepared
states in all three repositories. Final-state equality does not prove absence of
transient changes. The fixture/control check also ran independently.

The initial skill found the breaking contract but still recommended a refactor
type. The targeted correction requires rejecting `refactor` for removal of a
supported output/option even with `!`, and classifying actual intent. The revised
fresh-context sample obeyed that boundary. `feat!` versus `chore!` is not scored
as a unique exact answer: intentional removal versus maintenance intent is not
fully specified. Both identify the break and condition the recommendation.

The baseline already succeeded. This observation supports a narrow regression
correction, not an overall benefit claim. Eleven other cases, routed behavior,
authorized commit/hook/conflict execution, repetition and overhead measurements
are **Not Run**. The smallest next step is repeated blind classification trials
plus actual authorized-commit, mixed-index and hook-failure scenarios.
