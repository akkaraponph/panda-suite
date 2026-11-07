# Evaluation guide

Separate structural correctness, host discovery, and useful task behavior. A valid
SKILL.md is not proof of a better model response. This suite has no custom model
runner or orchestration service.

## Structural and host checks

Run the commands in the root README. The tooling tests mutate temporary package
copies to check YAML parsing, duplicate keys, naming, reference boundaries,
manifest consistency, missing skills, vendor drift, blind-fixture preparation,
and collision-safe installation. Intentionally defective fixtures are not part of
the default tooling test discovery.

`tests/check_codex_discovery.py` uses the installed CLI's generated app-server
protocol to read the local portable plugin and list copied skills in a temporary
Git repository. It does not install a plugin globally or start a model task.
Claude's `plugin details` command similarly verifies component discovery.

## Functional cases

`scenarios/cases.json` contains reviewer expectations. **Do not give that file to
the task-performing agent.** `prepare-evaluation.py` copies only the chosen fixture
and writes its task prompt:

```sh
python3 scripts/prepare-evaluation.py --case B --arm baseline --destination /tmp/panda-case-B-baseline
python3 scripts/prepare-evaluation.py --case B --arm specialist --destination /tmp/panda-case-B-specialist
python3 scripts/prepare-evaluation.py --case B --arm lead --destination /tmp/panda-case-B-lead
```

Use new destinations; existing workspaces are never overwritten. Baseline receives
no skill instructions. Specialist and Lead prompts identify instructions to load
through the host; this is not a fake programmatic invocation.

| Case | Capability |
| --- | --- |
| A | Debugging an intentionally uncommitted transfer |
| B | Planning manager rejection against existing source |
| C | Executing dependent slug implementation/documentation tasks |
| D | Review of an authorization regression plus formatting change |
| E | Simplification preserving access control |
| F | Thai specification with current/proposed/open distinctions |
| G | Manual from supplied evidence without browser access |
| H | Focused explanation without a project workflow |
| I | Investigation-only payment boundary |
| J | Brainstorm alternatives without premature implementation |
| K | Accurate developer guide and executable example |
| L | Verify an authoritative but unsupported technical claim |
| M | Authorized execute/review/write handoff |

For a browser-enabled G variation, serve the local synthetic manual fixture and
observe its actual UI using available browser tools. Keep no-browser and observed
runs separate. A saved [observed manual](results/browser-manual/manual.md) shows
the bounded journey and actual capture.

## Run and score fairly

Use a fresh context **per case and arm**, the same model/settings, inputs, tools,
budget, and external-access restrictions. Keep the task agent blind to expectations,
root-cause answers, other arms, and prior outputs. Record unavailable model settings.
Copy only fixtures, not the whole Suite repository, into task workspaces.

Save each final answer and actual command/tool evidence, loaded instruction paths,
source hashes before/after, and authorized output artifacts. A human or independent
reviewer should compare the answer with source and actual outcomes. Re-run delivered
implementations and examples; hashes show final-state boundaries, not absence of
transient historical changes. Task-agent summaries are not raw harness transcripts.

Rate each dimension as observed pass, partial, failure, or not applicable, with a
short evidence note:

- Correctness against all acceptance rules, including uncovered boundaries.
- Evidence quality and current/proposed distinctions.
- Completion of the requested artifact or work.
- Scope and authorization compliance.
- Verification honesty, especially failed and unrun checks.
- Usefulness for the intended reader.
- Routing/context overhead from actual loaded instructions, where observable.

Record elapsed time and token/context data only if the host exposes them. Distinguish
Claude's projected inventory token estimate from measured task consumption. Do not
infer savings from word counts. Do not invent numeric scores for dimensions that
were not observed. Preserve unfavorable results.

The bundled debugger's original evaluation rubric and answer key are archived at
`skills/panda-debugger/tests/evaluation.md`; its runnable fixtures deliberately
fail. Their failure is expected fixture behavior, not a Suite tooling regression.

The first exercise used grouped shared contexts and therefore cannot establish
causal improvement or independent repeatability. See the
[summary and independent audit](results/2026-11-07/summary.md). Subsequent runs
must label changed fixture inputs or revised instructions rather than silently
replacing earlier failures.
