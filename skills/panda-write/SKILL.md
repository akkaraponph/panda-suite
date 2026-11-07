---
name: panda-write
description: Create or maintain evidence-based project documentation such as READMEs, developer guides, setup instructions, API guides, runbooks, changelogs, and engineering reports in English or Thai.
---

# Panda Write

Produce documentation the intended reader can use and maintain. Use a technical
specification workflow for proposed contracts and design, or a manual workflow
for observed user journeys; ordinary documentation needs neither automatically.

## Inputs and workflow

Establish the audience, document purpose, requested language and destination,
source material, and project conventions. Existing templates take precedence over
a generic structure. Inspect available evidence before asking for missing facts.

1. **Gather evidence.** Read the relevant implementation, configuration, tests,
   existing docs, and supplied artifacts. Keep a short claim-to-source map for
   material behavior, commands, endpoints, permissions, and prerequisites.
2. **Define structure.** Organize around the reader's task. Include only useful
   sections: purpose, prerequisites, steps/examples, behavior, troubleshooting,
   operations, or references as the document needs.
3. **Draft.** Use direct B2-level English by default. For Thai, use professional
   Thai while preserving established identifiers and technical terms. Distinguish
   current behavior, a proposal, an assumption, and missing evidence. A planned
   feature must not become an implemented capability in the prose.
4. **Verify claims.** Check paths, configuration names, commands, example payloads,
   errors, and permissions against source. Run safe examples where feasible;
   record what ran and mark unverified examples honestly. Missing runtime access
   does not justify invented test results or setup steps.
5. **Refine.** Remove filler, duplication, unsupported claims, and conversational
   text from the finished artifact. Use diagrams only when they clarify supported
   behavior. Link useful source locations and check document references.

## Output and scope

Deliver the requested artifact plus a short account of its evidence, meaningful
verification, and remaining gaps. When evidence cannot establish a material claim,
omit it, label the uncertainty, or ask the precise question needed to resolve it.
The document is ready when a reader can follow it and assess its limits.

Writing authorizes the requested documentation changes, not unrelated application
implementation. Preserve source code unless changes were also requested. Safe
local examples may run; deployment, publication, production data changes, or
external side effects require authorization for those actions. Do not install
tools merely to make a guide look tested. This skill stands alone; any handoff
carries the audience, artifact paths, source evidence, unresolved claims, and
authorization.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Kalāma: Check material commands and behavioral claims against available evidence.
