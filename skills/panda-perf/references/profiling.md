# Profiling and query guidance

## CPU and algorithmic work

Define n/m and average/worst-case assumptions. A loop over n inputs with list
membership over m elements is generally O(nm); building a hash set can yield
expected O(n+m) while consuming extra memory and requiring hashable values.
Preserve output order and duplicate semantics rather than blindly returning a set.
Consider small workloads, expensive hashes and adversarial cases. Benchmark the
same result, including any required index construction; avoid timing only the
lookup while charging construction to the old path.

Use runtime-native tooling already available. The [Python profiling documentation](https://docs.python.org/3/library/debug.html)
links profilers, timeit, and tracemalloc; choose the installed runtime's tools.
Separate CPU samples from end-to-end latency and profiler overhead. Report
repetitions, data shape, units and summary statistics appropriate to samples;
do not manufacture p95/p99 values from a handful of unrelated runs.

## Memory

Trace ownership through caches, listeners, closures, queues, slices/views and
request histories. Inspect cleanup on success, error and cancellation. Compare
retained allocations after repeated equivalent work and appropriate cleanup;
document GC/allocator behavior and profiler blind spots. Allocation traces may
omit native memory and do not equal process RSS. A finite bounded cache is not
automatically a leak; unbounded retained state can be a code-supported growth
risk without an observed production leak. Bound or remove retention only when
the required lifetime, diagnostics and consumer behavior allow it.

## Database and concurrency

Count the initial query plus per-item queries; an ORM loop may use prefetching,
an identity map, or a cache, so inspect effective behavior. Batching can introduce
parameter limits, reorder results or alter transaction visibility. Preserve
authorization predicates and handle missing/duplicate keys. Compare round trips,
rows/bytes, latency and memory for representative cardinalities.

Read index definitions and plans before recommending new indexes. Consider
selectivity, composite order, functions/casts, collation, statistics, write cost
and locking. An index in migrations is not proof of a deployed index or its use.
The [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
distinguishes estimates from execution evidence. `EXPLAIN ANALYZE` executes the
statement and can cause side effects; ordinary read-only analysis does not
authorize running it against production or writes. A transaction rollback does
not erase all external effects. Use provided plans or an authorized disposable
environment and state its limits.

Adding concurrency may move the bottleneck into pools, locks, CPU, rate limits
or downstream systems. Measure queueing and bound in-flight work; preserve
cancellation, ordering, backpressure and data consistency. Propose infrastructure
changes only when workload evidence justifies their added operational cost.
