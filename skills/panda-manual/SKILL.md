---
name: panda-manual
description: Create user or administrator manuals, onboarding guides, and feature walkthroughs from observed application journeys or supplied UI evidence, using browser capture when available.
---

# Panda Manual

Document what a user can actually do. Developer implementation detail belongs in
engineering docs. Never turn a hypothetical UI or screenshot into an observation.

## Establish access and scope

Identify audience/role, journey, environment or URL, prerequisites, and permitted
actions. Discover available browser capabilities rather than assuming a named
tool. Use supplied evidence when access is absent. Ask for missing role or journey
details only if they materially change the instructions.

A documentation request authorizes the manual artifact. Before production-data
interaction, deletion, payment, messaging, publication, or another external side
effect, ensure authorization covers that action. Prefer a test environment and
synthetic records; a walkthrough does not grant access to another role or account.

## Observe and draft

1. Inspect the starting application state. Record environment, role, route, and
   evidence source without secrets. Follow the host/browser tool's access rules.
2. Navigate the bounded journey, observing each state before choosing the next
   action. Record actual visible labels, inputs, prerequisites, and expected versus
   observed outcomes. Observe safe validation/recovery paths when feasible.
3. Capture screenshots only when supported and useful. Use descriptive filenames
   such as `02-draft-saved.png`; exclude or redact sensitive information before
   saving or sharing. Associate each capture with its real step. A source mockup
   or supplied screenshot has its own provenance and is not a new browser capture.
4. Write prerequisites, numbered interactions, expected outcomes, observed errors
   and recovery, and evidence status. Use the reader's language and exact UI
   labels. Read [manual structure](references/manual.md) for a substantial guide.
5. Recheck the sequence against observations or supplied evidence. Replay safely
   if useful; do not repeat consequential actions solely to verify documentation.

## Evidence limits and completion

When browser access is missing, produce a clearly labeled **draft from supplied
evidence**. Distinguish **observed**, **documented but not observed**, and
**unverified** steps. Do not invent routes, controls, validation messages, captures,
or recovery behavior to fill gaps. State the smallest check needed for completion.

Deliver the manual, captured assets if any, evidence coverage, and unverified
parts. A complete observed guide has matching steps and outcomes; a useful draft
must keep its verification limit visible. This skill works without Panda Lead;
handoffs preserve role, environment, sources, screenshots, missing observations,
and authorization.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Sati-Sampajañña: Confirm the visible state and evidence source before describing each step.
