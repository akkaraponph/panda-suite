# Panda Spec save behavior, 2026-11-10

Each arm used a fresh fixture workspace and an ephemeral Codex CLI session with
workspace-write access and the same host defaults. Baseline prompts supplied only
the task. Specialist prompts identified the repository skill. The non-trigger case
used Lead for routing. Reviewer checks stayed outside the prompts. The host skill
catalog was available to both arms. These are single observations per condition.

| Case | Baseline | With Panda instructions |
| --- | --- | --- |
| F, Thai approval spec | Saved at workspace root | Saved and linked a dated Markdown spec under the default directory |
| Named project | Saved in billing/timeout-spec.md | Saved under billing/.panda-suite/specs/ |
| Explicit path | Wrote design/rejection.md | Same |
| Chat only | Returned spec in chat | Same, with zero file changes |
| Edit existing | Updated only requirements.md | Same, including a repeat after clarifying how inputs are handled |
| Invalid path through service.py | Reported failure and asked for another path | Reported failure and delivered the spec in chat, with zero file changes |
| Two plausible projects | Asked which project owns the spec | Same, with zero file changes |
| Explain existing function | Answered in chat | Lead answered in chat without loading Panda Spec or writing a file |

The first Git prompt asked for a specification “for the retry policy in
requirements.md.” Both arms edited the staged requirements document. After
clarifying the skill's input-versus-target rule, a fresh specialist run still
interpreted the same prompt as an in-place edit. That wording is ambiguous.
The retained Git case explicitly identifies requirements.md as input for a new
document. Its result tests the clearer contract and cannot establish a fix for
the original wording.

To reproduce the cases, use scripts/prepare-evaluation.py with F or the SPEC-
case IDs from the scenario catalog. For SPEC-GIT, initialize a Git repository in
each prepared workspace and stage .gitignore and requirements.md before running
the task. Compare the saved path, file contents, ignore rules, staged entries,
and final response. The explicit destination, chat and edit controls exercise
behavior that should still work without the default save convention.

With requirements.md explicitly named as source material, the baseline created
SPEC.md and the specialist created .panda-suite/specs/2026-11-10-retry-policy.md.
Both files were untracked and eligible for staging. The ignore file, source file
and staged entries matched their initial contents. The local run evidence is
under tests/runs/spec-save/, including the unsuccessful first attempts.

A 23rd run used the final explicit ambiguity rule and the original ambiguous
prompt. The specialist asked whether requirements.md should be edited or used
as input. A byte comparison confirmed it was preserved. This single repeat
establishes the observed correction, with reliability across repeated runs unknown.
