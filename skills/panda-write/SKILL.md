---
name: panda-write
description: Create, review, or update evidence-based engineering documentation such as READMEs, developer guides, API guides, runbooks, architecture explanations, and technical handovers in English or Thai.
---

# Panda Write

Produce documentation engineers can use to understand, operate, and verify the
current system. Review and repair existing documents as well as write new ones.
Use a specification workflow for proposed contracts and design, or a manual
workflow for observed user journeys. A focused code explanation needs no document
workflow; general prose and marketing copy are outside this skill's purpose.

## Inputs and workflow

Establish the audience, document purpose, requested language, format and destination,
source material, and project conventions. Preserve the existing document's format
and language unless asked to change them; explicit user instructions take
precedence. Inspect available evidence before asking for missing facts.

**Ask before guessing.** Each section needs a named source of truth: current
code, a document or system the user references, or the user's answer. Before
drafting, ask one precise question when the source of truth, scope, audience, or
content to include is unclear, sources conflict on a point the document must
state, or a material fact is unknown. Proceed with `Pending Confirmation` only
when the user said to continue with gaps or the answer is known to be unavailable.
Write only what the sources establish and the request needs; ask before adding
sections, examples, features, recommendations, or background beyond them.

1. **Gather evidence.** Read relevant implementation, configuration, schemas or
   migrations, tests, contracts, and existing docs. Trace important behavior from
   entry point through its components and data flow. Verify each feature or
   integration independently, including validation, permissions, errors, retries,
   and lifecycle where relevant. Similar names or modules do not prove identical
   behavior. Keep a short claim-to-source map for material claims.
2. **Define structure.** Organize around the reader's task. Include only useful
   sections: purpose, prerequisites, steps/examples, behavior, troubleshooting,
   operations, or references as the document needs. For a review, identify stale,
   unsupported, or contradictory claims with locations and evidence; edit only
   when the request authorizes updates.
3. **Draft.** Follow the requested or existing language; otherwise use direct
   B2-level English. For Thai, use professional Thai with established technical
   terms and exact identifiers. Separate implementation, configuration, deployed
   state, external-system contracts, confirmed requirements, and proposals.
   Current code establishes implemented paths, not production state or a remote
   system's guarantees. Record contradictions and prefer current implementation
   for claims about implemented behavior. Keep required/actual differences visible.
   When continuing with gaps is authorized, keep verified sections and mark specific
   unresolved facts `Pending Confirmation` with the evidence or decision needed,
   without appending guessed behavior. State facts directly. Do not write absence
   or contrast narration such as "There is no X, but there is Y", "The code does not
   include X; instead...", or "No documentation was found". Include an absence only
   when the reader needs it to act, as a plain fact ("`send_audit` sends no
   `Authorization` header"). Report gaps to the user in the delivery message.
4. **Verify claims.** Check paths, configuration names, commands, example payloads,
   errors, and permissions against source. Verify external behavior against its
   authoritative contract; local callers alone cannot establish it. Run safe
   examples where feasible; record what ran and mark unverified examples honestly. Missing runtime access
   does not justify invented test results or setup steps.
5. **Refine.** Remove filler, duplication, unsupported claims, and conversational
   text from the finished artifact. Delete sections and sentences the sources or
   request do not require, including "limits of this document", "not covered",
   or "the code does not define X" notes; put those in the delivery message.
   Explain responsibilities, conditions, data
   movement, and boundaries directly rather than narrating the investigation.
   Check diagrams against the traced paths; label logical views so they cannot
   imply physical deployment. Link useful source locations and check references.

For a substantial architecture explanation, integration guide, or technical
handover, read [engineering document guidance](references/engineering-documents.md).
Use only sections relevant to the scope; a short README needs no chapter template.

## Output and scope

Deliver the requested artifact plus a short account of its evidence, meaningful
verification, and remaining gaps. When evidence cannot establish a material claim,
ask the precise question needed to resolve it; omit or label it `Pending
Confirmation` only when continuing with gaps is authorized.
The document is ready when a reader can follow it and assess its limits.

**Saved output.** Save a new document at
`.panda-suite/docs/YYYY-MM-DD-<topic>.<ext>` under the active project root, using
the current local date and a short lowercase hyphenated topic. Use Markdown unless
the user asks for another format such as `.docx` or `.pdf`; then keep the Markdown
source beside the exported file. Convert with tools already available; if none
can produce the format, save the Markdown, state that the export was not created,
and ask before installing anything. An explicit path or file name, an existing
document named for update, or a chat-only request takes precedence. In a workspace
with several projects, use the one the request or its sources identify; ask when
several still fit. Do not overwrite another document; choose a distinct name.

Do not stage or commit `.panda-suite/` output, and do not edit ignore files
unasked. If Git would track `.panda-suite/`, say so in the delivery message.
Verify the saved files exist and link them in the response.

Writing authorizes the requested documentation changes, not unrelated application
implementation. A review-only request delivers findings without editing documents.
Preserve source code unless changes were also requested. Omit secret values while
documenting configuration keys and safe placeholders. Safe local examples may run;
deployment, publication, production data changes, or
external side effects require authorization for those actions. Do not install
tools merely to make a guide look tested. This skill stands alone; any handoff
carries the audience, artifact paths, source evidence, unresolved claims, and
authorization.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Kalāma: Check material commands and behavioral claims against available evidence.
