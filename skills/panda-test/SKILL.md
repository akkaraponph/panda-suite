---
name: panda-test
description: Design, add, run, or assess effective unit, integration, API, regression, and end-to-end tests when behavior needs verification or existing coverage may miss meaningful failures.
---

# Panda Test

Verify behavior and invariants with useful tests, rather than maximizing test
count. A causal investigation belongs to debugging; test work need not reproduce
the entire debugging workflow. A focused explanation needs no test strategy.

## Inputs and scope

Read requirements, implementation, interfaces, existing tests, fixtures, runner
configuration, and project instructions. Establish what is expected versus merely
implemented. Identify missing contracts before encoding assumptions as assertions.
Use source evidence first; ask when an unresolved rule changes expected results.

A request to create tests authorizes relevant test/fixture changes. Test analysis
alone is read-only. Neither authorizes unrelated production-code fixes. A request
to implement or fix identified behavior may already cover those changes; preserve
that authorization without asking again. Production data, destructive testing,
external side effects, and new infrastructure need authorization covering them.

## Workflow

1. **Understand behavior.** Map requirements to observable inputs, outcomes,
   permissions, state transitions, errors, and data invariants. Examine existing
   assertions as well as test names; a green suite can miss a stated requirement.
2. **Choose boundaries.** Select unit tests for isolated rules, integration tests
   for real component interactions, API tests for contracts, or end-to-end tests
   for a complete journey. Avoid duplicating the same proof across every layer.
   State which real dependencies or mocks each selected level needs.
3. **Design cases.** Prioritize actual risks: normal behavior, invalid/missing
   data, boundary values, dependency/transaction failure, authorization,
   concurrency, duplicates, or idempotency as relevant. Include a discriminating
   regression case for the reported defect. Do not invent business policy.
4. **Implement authorized tests.** Reuse the repository's framework and fixtures.
   Assert externally meaningful outcomes, including unchanged state on failures.
   Prefer safe real dependencies for integration checks; label mock-backed tests
   accurately. Keep data deterministic and cleanup scoped to disposable fixtures.
5. **Execute.** Record exact commands, environment/dependency scope, exit status,
   failures, and limitations. Proposed tests are **Not Run** until executed. An
   unavailable database does not turn a mocked test into an integration pass.
6. **Assess effectiveness.** Check assertions, boundary data, test isolation,
   brittleness, unnecessary mocks, and potential flakes. Where safe, show the
   regression fails against the faulty behavior and passes against a separately
   authorized correction. Do not weaken tests or patch production code to hide a
   failure. If diagnosis is needed, pass evidence to `panda-debugger` when available;
   otherwise report the unresolved defect and smallest useful investigation.

## Output and completion

Report test scope, selected scenarios, implementation paths, actual execution
results, coverage gaps, and remaining risks. Distinguish implemented tests from
executed tests and verified behavior from untested acceptance rules. Missing tools
support a bounded plan or partial result, not invented logs or percentages.
This skill works without Panda Lead; handoffs carry evidence, artifacts, outstanding
checks, and authorization. Consult `buddhist-method` optionally when uncertainty
or repeated failures materially affect the next decision.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Vīmaṃsā: Check whether assertions would detect a plausible violation of the required behavior.
