---
name: panda-simplify
description: Assess unnecessary complexity in code, architecture, documentation, or agent workflows when the user wants fewer layers, clearer responsibilities, or a simpler maintainable design.
---

# Panda Simplify

Recommend the smallest design that satisfies real requirements. Fewer lines alone
are not evidence of improvement. Default to analysis; edit only when requested.

## Inputs and workflow

Use the current artifact, its purpose, constraints, usage evidence, and relevant
tests. If future needs are uncertain, distinguish demonstrated needs from guesses.

1. **Establish the problem.** What user outcome does the system serve? Read the
   implementation, callers, configuration, and tests that define its invariants.
   Identify necessary security, validation, observability, and failure behavior.
2. **Find the complexity cost.** Trace pass-through layers, unused extension
   points, duplicated decisions, unnecessary dependencies, and instruction or
   routing overhead. Cite concrete paths and examples. Separate essential domain
   complexity from accidental structure.
3. **Compare simpler forms.** Ask which parts are essential, which abstractions
   have demonstrated value, what must remain extensible, and what can safely be
   removed. Compare the existing form with a concrete smaller alternative and its
   near-term change cost. Preserve behavior rather than merely compressing syntax.
4. **Validate the recommendation.** Map each preserved invariant to source/tests
   or a proposed regression check. Explain what could break, how to recover, and
   which assumptions require confirmation. If edits are authorized, inspect the
   current files, make the bounded change, and run relevant checks before calling
   it verified.

For a single greeting service, a factory plus a pass-through adapter may add no
value. Recommend a direct method while keeping the existing permission guard and
public call shape. Do not replace those classes with a new plugin framework.

## Decision discipline and output

When available and relevant, consult `buddhist-method` for **Majjhimā Paṭipadā**
(appropriate complexity), **Pahāna** (cause removal), or **Anāgataṃsa-ñāṇa**
(bounded foresight). Use its original instructions rather than copying the whole
method here. If unavailable, this workflow remains usable: base the recommendation
on demonstrated requirements and evidence.

Output the complexity assessment, unnecessary elements and their costs, proposed
simplification, preserved invariants, trade-offs, regression risks, and verification
status. Completion means the recommendation is assessable against actual usage;
it does not require implementation. Keep source unchanged in analysis mode and
preserve authorization and evidence in any handoff. No Panda Lead dependency.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Majjhimā Paṭipadā: Choose a simpler design by checking it against demonstrated needs and preserved behavior.
