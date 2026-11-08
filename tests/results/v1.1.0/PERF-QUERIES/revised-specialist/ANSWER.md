`load_labels` has a code-supported repeated-round-trip cost: work.py:17–18 issues exactly n remote queries for n input IDs, including duplicates. The repository contract rules out an implicit cache. This is the only proposed change; no input files were modified. No production profile, SLO, DB server, profiler, execution timing, or buffers are available, so wall-time impact is unmeasured.

Proposed patch — conditional on freshness approval

```diff
--- a/work.py
+++ b/work.py
@@ -1,5 +1,6 @@
 """Synthetic local workload; no production profiler or database is included."""
 from collections import deque
+from itertools import islice
 
 
 def unique(items):
@@ -15,7 +16,12 @@
 
 
 def load_labels(repo, ids, tenant):
-    return [repo.get_label(tenant, item) for item in ids]
+    pending = iter(ids)
+    result = []
+    while chunk := list(islice(pending, 500)):
+        labels = repo.get_labels(tenant, chunk)
+        result.extend(labels.get(item) for item in chunk)
+    return result
 
 
 RECENT = deque(maxlen=10)
```

Each call passes the original tenant. Iterating the original chunk reconstructs order and duplicates independently of mapping order; `.get` supplies None for absent IDs. Empty input issues zero queries. The supplied limit is explicitly 500 IDs per query, so each chunk contains at most 500 IDs. If an actual adapter instead counts tenant or other bind parameters within a total of 500 parameters, its supported ID capacity must be established and the chunk size adjusted before application.

The patch uses ceil(n/500) calls, without deduplication, and performs O(n) reconstruction under ordinary constant-time mapping lookup assumptions. It needs O(500) temporary IDs and mapping entries beyond the O(n) returned list, assuming the repository returns only requested IDs. It streams iterable input in chunks; it does not consume the entire iterable up front. Mapping keys must have the repository's normal ID equality semantics. No global cache, parallelism, schema change, generic helper change, or retention change is proposed.

Freshness is a deciding semantic change: old reads can see changes between any two IDs, while each batch sees one consistent snapshot. Duplicates within a batch therefore share the batch result. Multiple chunks are separate calls and are not established to share one snapshot. Before applying, establish whether per-item freshness is observable and whether per-batch snapshots are acceptable; if one snapshot across all IDs is required, a repository transaction/snapshot contract is needed. Chunking also fetches up to 500 iterable items before the query and changes remote failure timing and partial side effects; validate callers that depend on these. The patch is reviewable and locally checked, but application is blocked on these semantic decisions.

The captured sequential scan is not an established bottleneck. small-plan.txt describes only three rows and SELECT id FROM tiny_table with no selective predicate: reading the tiny table sequentially can be appropriate even with an existing id index. cost=0.00..1.03 is a planner estimate in cost units, not milliseconds. There is no evidence connecting this unrelated plan to the repository's label query, or establishing missing indexes, poor selectivity, stale statistics, or actual slow execution. No index recommendation is supported.

Evidence ranking: (1) repeated label queries, Code-supported, directly addressed by this conditional patch; (2) the tiny-table scan, Hypothesis only as a performance issue and low priority given three rows. The context's unique_ids and history concerns are outside this requested query optimization; this patch leaves their contracts intact.

Verification

Python 3.14.7: all three supplied baseline tests passed. The first `git apply --check` found an incorrect unified-diff hunk count; corrected that header in this answer, re-extracted the delivered diff and verified `git apply --check` successfully. Applied only to a temporary work.py copy and reran all three supplied tests against the candidate module: all passed. A static fake repository compared baseline and candidate for 10 cases across two tenants (20 comparisons): empty, duplicates within and across chunks, missing IDs, zero/negative IDs, reverse mapping iteration order, iterator input, and lengths 499, 500, 501, 1,000, 1,001 and 20,000. All output equivalence, tenant, chunk bound, flattened original-ID sequence and exact query-count assertions passed. Observed fake calls: 0→0, 500→1, 501→2, 1,000→2, 1,001→3 and 20,000→40. These are operation counts, not DB timings. SHA-256 checks confirmed supplied inputs unchanged during verification. No network, installs, real DB operations or latency benchmarks were performed. Static fake data cannot validate concurrency visibility or the real tenant SQL predicate.

Remaining checks: approve the freshness/iterator/error semantics above; inspect the real get_labels implementation to confirm its tenant predicate, ID bind budget, omitted-key behavior and snapshot scope. With an authorized representative DB environment, compare actual label-query plans, query counts, rows/bytes, and repeated end-to-end timings under realistic latency, cardinalities, cache state and concurrency. No measured latency speedup or production SLO claim follows from this synthetic check. Nothing was applied, so no rollback is required.
