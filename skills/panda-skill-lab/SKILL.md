---
name: panda-skill-lab
description: Create, review, evaluate, or improve Agent Skills when a workflow has an observed failure, unclear routing, compatibility questions, or context overhead that needs evidence-based investigation.
---

# Panda Skill Lab

Determine whether skill instructions solve a distinct problem and improve actual
work. An ordinary application feature, function explanation, or one-off debugging
request does not require skill development. Prefer an existing skill or reference
when a separate discovery trigger has no demonstrated value.

## Inputs and workflow

Use the target task, current skill if any, repository/host constraints, examples,
and observed failure evidence. Inspect relevant skills and evaluation artifacts
before designing changes. Missing access or model settings must remain visible.

1. **Define the problem.** Identify what normal agent behavior gets wrong, why
   it matters, and observable success criteria. Separate a hypothesized failure
   from one actually seen. Check overlap with existing capabilities.
2. **Define the contract.** Specify name, capability/trigger description,
   non-triggers, inputs, workflow, outputs, permission boundaries, and evaluation
   criteria. Verify current format against the
   [Agent Skills specification](https://agentskills.io/specification) and the
   target host's actual discovery mechanism. Format validity alone proves neither
   host compatibility nor correct behavior.
3. **Design minimally.** Keep instructions concise and independently usable.
   Use skill-local references only for conditional detail. Preserve upstream
   attribution and scope. Avoid repeating global rules, adding a runtime, or
   assuming programmatic skill invocation. Skill creation requests authorize the
   scoped artifact; review/evaluation requests do not automatically authorize edits.
4. **Create blind cases.** Include normal use, missing information, conflicting
   evidence, ambiguity, tool failure, wrong initial assumptions, authorization,
   and out-of-scope pressure where relevant. Include a case where this skill
   should not activate. Keep answer keys away from task-performing agents.
5. **Establish baseline and skill runs.** Use fresh contexts per case and arm;
   hold model/settings, tools, inputs, access, and budget comparable. Save actual
   answers, loaded paths, actions, results, and authorized artifacts. Use native
   evaluation/delegation only when available and authorized. If no model runner
   exists, deliver runnable scenarios and mark behavioral comparison **Not Run**;
   do not simulate another model's answer yourself as an independent result.
6. **Compare and diagnose.** Assess correctness, evidence, usefulness, completion,
   scope, verification honesty, and overhead. Measure context/time only when
   exposed reliably. Separate instruction defects from missing evidence, host
   limits, and model variance. Shared contexts or changed inputs limit comparison;
   metadata estimates and word counts do not establish token savings.
7. **Improve and regress.** Modify only demonstrated weaknesses within authorized
   scope, then repeat relevant checks including non-activation and safety cases.
   Retain original failures and label changed conditions. Reconsider, simplify,
   merge, or remove a skill that adds no observed value; do not assert improvement
   from a small or uncontrolled sample.

## Output and completion

Deliver purpose, target failure mode, contract, implementation changes if
authorized, scenarios, actual baseline/skill results, comparative analysis,
remaining weaknesses, and smallest justified next improvements. Clearly mark
unrun evaluations and unavailable measurements. Publishing, installation into
global configuration, external data sharing, or production actions require
authorization covering those actions. This skill needs no Panda Lead or custom
state service. Optionally consult `buddhist-method` at a specific uncertainty or
repeated-failure decision, without adding it to every evaluation stage.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Anatta: When evaluation challenges a favored revision, retain the evidence and reconsider it.
