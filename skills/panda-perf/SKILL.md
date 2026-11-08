---
name: panda-perf
description: Investigate performance and memory bottlenecks, algorithmic complexity, redundant queries or N+1 patterns, and query plans; produce evidence-backed optimization diffs and validate behavior and resource trade-offs.
---

# Panda Perf

Find the limiting work and propose the smallest behavior-preserving optimization.
Static complexity analysis identifies candidates; measured runtime impact needs a
representative workload. Use ordinary review for general diff defects, debugging
for an unexplained functional failure, and simplification for unnecessary structure.
A short code explanation does not need profiling.

## Inputs and authorization

Use the slow operation, expected latency/throughput/memory target, input sizes and
distribution, runtime/version, relevant code and tests, profiles, query plans, and
permitted environment. Inspect available evidence before asking for missing facts.
If a target or profiler is absent, state a bounded working scope and continue with
source-supported analysis; do not invent an SLO or production measurement.

Analysis requests are read-only. An optimization request authorizes relevant local
changes; a request for a diff can be satisfied with a proposed patch without
applying it. Distinguish proposed from applied changes. Production profiling,
load tests, dependency installation, database/index changes, external workloads,
and collection/sharing of sensitive traces require authorization covering them.

## Workflow

1. **Bound and reproduce.** Map the operation and cost dimensions: CPU, wall time,
   allocations/retained memory, I/O, query count/rows, locks or contention. Inspect
   workloads and call paths. Record actual reproduction separately from reported
   symptoms; synthetic data establishes only the tested conditions.
2. **Establish a baseline.** Reuse safe existing profilers or create a bounded
   disposable harness when allowed. Record revision, runtime, input shape/size,
   setup/warm-up, repetitions, cache state, concurrency and observable limits.
   Separate setup from measured work and compare equivalent operations. Use
   repeated samples; timing noise or one microbenchmark does not prove an SLO.
3. **Trace cost.** Explain complexity with defined variables and data-structure
   assumptions, including nested iteration, membership checks, copies/sorts, and
   repeated serialization. Attribute hot paths using profiles where available.
   For memory, inspect owners, object lifetime, growth across repeated equivalent
   work, cleanup and bounds; distinguish peak allocation, retained objects, RSS,
   and allocator/GC effects. High RSS alone does not prove a leak.
4. **Inspect data access.** Follow ORM/lazy-load paths and query counts to validate
   N+1 or redundant round trips. Check predicates, joins, pagination, cardinality,
   schema/index definitions and actual plans where available. A sequential scan
   can be appropriate; missing plan/runtime evidence prevents claims of an
   observed unindexed bottleneck. Batching/indexing proposals must preserve
   tenant filters, ordering, duplicates, nulls and transaction/snapshot semantics.
5. **Optimize concretely.** Rank bottlenecks by supported cost and workload impact,
   not aesthetic preference. Supply a minimal unified diff anchored to inspected
   code, or apply the scoped change when authorized. Explain CPU/memory/I/O
   trade-offs and preserved invariants: ordering, equality/hashability, permissions,
   error behavior, mutation/aliasing, freshness and concurrency as relevant.
   Avoid speculative caches, parallelism, indexes or infrastructure when a local
   algorithmic change suffices. If deciding semantics are unknown, give a bounded
   patch for the verified path and mark the broader optimization blocked.
6. **Verify equivalence and cost.** Check the delivered unified diff itself against
   a disposable copy (for example, `git apply --check`), with sufficient context
   for ordinary application; testing a separately typed candidate is insufficient.
   Run meaningful behavior/boundary checks plus comparable before/after measurements
   when possible. Retain regressions and
   noisy or unfavorable samples. Report query counts/operation counts separately
   from timings and distinguish expected asymptotic gains from measured results.
   If verification is unavailable, label the patch Proposed/Unverified and name
   the smallest deciding experiment. Do not claim measured speedup or fixed leak.

For the relevant CPU/memory or database branch, consult
[profiling and query guidance](references/profiling.md). No particular profiler,
language, database, peer skill, or custom runtime is required.

## Output and completion

Deliver scope/workload, ranked bottlenecks with file/line and causal cost evidence,
confidence (Measured, Code-supported, or Hypothesis), baseline limits, concrete
optimization diffs, preserved behavior and resource trade-offs, actual tests and
before/after results, and remaining checks. Report units and samples honestly;
estimated planner costs are not elapsed milliseconds. Include memory/query impact
when material and rollback implications for applied changes.

An analysis is complete when the bottleneck and patch can be assessed against
evidence and invariants. An applied optimization is complete when the scoped
change is verified or its unresolved limits are explicit. Handoffs carry workload,
measurements, assumptions, patch status, unrun checks, and authorization.

## Success discipline

Vīmaṃsā: Measure the relevant cost, challenge the first bottleneck hypothesis,
and preserve behavior before claiming improvement. A faster wrong result fails.
