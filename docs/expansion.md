# Essential engineering expansion

## Investigation and decisions

Inspected the existing eleven skills, skill-local references, both host manifests,
installation utilities, validators, fixtures, and recorded evaluation failures.
The existing pinned Panda Debugger and Buddhist Method technique Markdown was
reviewed in this session and its thirty source-file hashes rechecked unchanged.
Current metadata requirements were checked against the
[Agent Skills specification](https://agentskills.io/specification).

The gaps were distinct: requirements define what the business needs; impact traces
dependencies before a change; testing owns test effectiveness; release assesses
delivery evidence; Skill Lab evaluates instruction behavior. Plan still orders
implementation and Spec still defines technical design. No new runtime is needed.

## Implemented milestone

| Skill | Responsibility |
| --- | --- |
| panda-requirements | Actors, permissions, business rules, identified functional requirements, relevant quality requirements, testable acceptance, conflicts and open decisions |
| panda-test | Risk-based scenarios, authorized test implementation, real execution, assertion effectiveness and remaining coverage gaps |
| panda-impact | Confirmed dependencies, compatibility/data/API/operational effects, risk confidence, mitigations and required verification |
| panda-release | Bounded scope, evidence freshness, proportional gates, release/recovery artifacts and READY/CONDITIONALLY READY/BLOCKED/UNKNOWN assessment |
| panda-skill-lab | Distinct failure modes, skill contracts, blind baseline/skill comparisons, nonactivation, justified edits and regression evaluation |

Lead now routes these intents without imposing a delivery pipeline. Direct
specialist installation remains supported. Handoffs carry progress and verification
as well as facts, assumptions, files, decisions, unknowns and authorization. A
receiver checks current state; a summary never overrides source or user limits.

Read-only analysis, task-authorized workspace changes, and consequential operations
are separate scope categories. Preparation never authorizes deployment, publication,
migrations, or announcements. Prior implementation authorization remains valid.

## Primary skill integration

Panda Debugger and Buddhist Method are primary Suite skills. Their `SKILL.md` and
technique documents under `references/` keep their exact original bytes. Supporting
README and evaluation material now live inside their skill directories; historical
manifest metadata lives under `source-metadata/`. There is no separate source-vendor
directory. The source mapping and hashes were updated for the new locations.
Attribution and license facts remain in [source notices](../SOURCE_NOTICES.md).
Historical evaluation logs retain paths that were true when those runs happened;
they were not rewritten into fictional current-path transcripts.

## Advanced capabilities

No advanced placeholder skills were created. Security review overlaps Review;
source/telemetry causal investigation belongs to Debugger; migration design can use
Plan and Spec; usability exploration can use Brainstorm; ADRs already have a Spec
template. A separate Decision skill has no demonstrated frequent distinct workflow.
Dedicated Observe, Migrate, Security, or UX skills need realistic domain fixtures
and a demonstrated benefit before expanding discovery metadata further. This
milestone implements and validates the five essential skills first.

## Verification and limits

Twenty-four tooling regression tests pass. The package validator checks the sixteen-skill catalog and scenario coverage.
Codex 0.159.2 actually reads all sixteen plugin skills and discovers sixteen
standalone copies. Claude Code 2.1.251 lists all sixteen components. All thirty
source-file hashes still match. These implementation checks did not perform global installation or package publication. Commit/push delivery is recorded in Git history.

Seven expansion cases cover ambiguity, incompatible status changes, an unsafe
release, a failing authorization regression test, missing database tools, missing
model-runner evidence, and nonactivation. Actual task outputs and command evidence
are saved under `tests/results/expansion/`; see the [task-use results](../tests/results/expansion/summary.md). These are small grouped
task-use checks, not comparable independent model samples or evidence of performance
improvement. The Lab task explicitly lacks a runner; its comparison must remain
Not Run. Persistent plugin invocation and production operations remain untested.

Next useful work is fresh-context baseline/specialist comparisons for a specific
observed weakness, rather than adding advanced skill names without evidence.
