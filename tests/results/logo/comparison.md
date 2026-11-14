# Panda Logo verification

## Purpose

The suite had no design specialist for producing and verifying visual identity
assets. Raster images mislabeled as vectors and unverified export claims were
hypothesized failure modes before these trials. An unsupported visual pass was
observed during the trials.

## Blind task trials

Codex CLI 0.159.2 ran fresh ephemeral contexts with sandbox mode
`workspace-write`, ignored user config and exec rules, and the CLI's default
model settings. Model identity and reasoning settings were not captured.
Each arm used the same task text and fixture. Only the specialist workspace
received the local skill and a prompt to read it. The no-renderer restriction
was given in the prompt. The renderer remained installed on the host.
Each run directory below retains the final answer, local SVG/PNG outputs,
and executed commands with exit statuses.

| Case | Baseline | Skill-enabled |
| --- | --- | --- |
| LOGO-CREATE | Editable SVG and 512 px PNG with alpha. No 24/32 px rendering or visual inspection observed. [Evidence](create-baseline/answer.md) | Editable SVG and 512 px PNG with alpha. Rendered a contact sheet for 24/32 px and light/dark checks. Claimed visual checks passed without a recorded viewing action. [Evidence](create-specialist/answer.md) |
| LOGO-NO-RENDERER | Delivered valid SVG; reported unavailable PNG and visual checks. [Evidence](no-renderer-baseline/answer.md) | Delivered valid SVG; marked visual checks and PNG export Not Run. [Evidence](no-renderer-specialist/answer.md) |
| LOGO-CREATE after clarifying the visual evidence criterion | Not Run again | Delivered an SVG and 512 px PNG with alpha. Rendered a contact sheet and again claimed visual checks passed without a recorded viewing action. [Evidence](create-revision/answer.md) |

Author inspection of the first specialist contact sheet found the main silhouette
legible on light and dark backgrounds, with the shortest entry harder to read at
24 px on dark. That subsequent review is independent of the task agent's claimed
pass. A rendered contact sheet and an image-inspection record are useful separate
pieces of evidence. The next trial should use a host with an explicit viewing
tool and record its result. This sample supports no reliability or improvement
claim. The twelve other behavioral scenarios, including Invaris, were **Not Run**.
Claude Code task execution and interactive plugin invocation were **Not Run**.

## Structural and deterministic checks

- `.venv/bin/python scripts/validate-skills.py` validated 25 skills,
  references, manifests, and scenario coverage.
- `.venv/bin/python -m unittest discover -s tests -p 'test_tooling.py' -v`
  passed 31 tests. System Python lacked `jsonschema` for both checks.
- `python3 tests/check_codex_discovery.py` found the skill in both portable
  plugin and project-local discovery on Codex 0.159.2. The isolated specialist
  trials also copied just Panda Logo through the installer.
- Both Claude Code 2.1.251 manifest validations passed.
- `.venv/bin/python scripts/build-docs.py` and
  `.venv/bin/python scripts/check-docs.py` passed with 47 pages and 25 skill guides.
- `python3 -B tests/reviewer/check_logo.py` distinguished real vectors from a
  raster-only wrapper, checked the spelling and external-reference fixtures,
  rendered 16, 24, 32, and 512 px controls, verified PNG metadata and manifest/ZIP
  consistency, and rejected a ZIP with an extra member.
