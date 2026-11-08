# Proposed optimization — not applied

Scope: `load_labels` in `work.py:17–18` and the captured plan in `small-plan.txt`. No production profile, latency objective, DB server, timings, or buffers are available. Findings below concern query counts and source behavior, not measured database speed.

1. **Code-supported:** `load_labels` performs n remote queries for n input IDs, including duplicates. This is the actionable round-trip cost candidate. Wall-time dominance remains unmeasured.
2. **Code-supported:** the tiny-table sequential scan is reasonable for a three-row, unfiltered `SELECT id`. An index already exists in the supplied snapshot. `cost=0.00..1.03` is a planner estimate, not milliseconds; nothing links this plan to `load_labels`, proves a slow query, or supports a new index.

The following concrete patch uses the existing tenant-scoped batch API and at most 500 IDs per call. It deliberately retains repeated IDs in each request, avoiding extra assumptions about ID normalization. It reduces query count to ceil(n/500), with zero calls for empty input.

```diff
--- a/work.py
+++ b/work.py
@@ -17,2 +17,8 @@
 def load_labels(repo, ids, tenant):
-    return [repo.get_label(tenant, item) for item in ids]
+    ids = list(ids)
+    result = []
+    for start in range(0, len(ids), 500):
+        chunk = ids[start:start + 500]
+        labels = repo.get_labels(tenant, chunk)
+        result.extend(labels.get(item) for item in chunk)
+    return result
```

**Application is gated on a freshness decision:** is it acceptable for IDs within a batch to share a consistent snapshot instead of observing changes between individual reads? For inputs above 500, separate batch calls may see different snapshots; the supplied API does not establish one snapshot across the entire operation. If whole-operation consistency is required, this patch alone cannot establish it. No change has been applied while that decision remains open.

For stable data, reconstructing results from each mapping preserves original ordering, duplicates, `None` for omitted IDs, tenant filtering on every call, negative IDs, and the 500-ID limit. Mapping entries whose label is `None` remain `None`. Materializing `ids` also accepts finite generators, but consumes them before querying instead of interleaving iteration with reads; callers relying on iteration side effects, partial reads before an iterator error, or per-item failure timing need review. Batch failures can likewise differ from individual-query failures. No unsupported equality/hashability contract is added beyond the supplied mapping-based API.

Resource trade-offs: O(n) result reconstruction plus O(n) input materialization and at most 500 IDs/mapping entries per batch. Additional retained input memory is O(n); the old result already requires O(n). Remote query/response sizes increase per call. No speculative cache, concurrency, schema change, or history retention change is proposed. `unique`, `unique_ids`, `RECENT`, and `HISTORY` remain outside this task.

## Actual local verification

Python 3.14.7; isolated, sequential fake repository; deterministic stable data; no network, DB, cache warmup, timings, production profiler, or installs. Candidate executed only in an in-memory namespace; `work.py` preserved. Nine cases compared the original and candidate, including generators, empty input, singleton, duplicates, missing/negative ID, 499/500/501 boundaries, duplicate IDs across the 500 boundary, 1,001 IDs, and 20,000 IDs. Two tenant-specific checks also passed.

| Input count | Original fake query calls | Proposed fake query calls |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| 5 | 5 | 1 |
| 499 | 499 | 1 |
| 500 | 500 | 1 |
| 501, distinct | 501 | 2 |
| 501, repeated | 501 | 2 |
| 1,001 | 1,001 | 3 |
| 20,000 | 20,000 | 40 |

**Measured:** only these synthetic operation counts and stable-data equivalence. **Unverified:** actual query construction/tenant enforcement inside the real repository, real parameter accounting, DB latency/throughput, row/byte transfer, allocation/RSS, errors, and concurrent visibility. The contract specifies a 500-ID limit; if the real limit instead includes the tenant bind, reduce the chunk size to its verified remaining ID budget. The smallest next deciding steps are the snapshot acceptance decision and an authorized repository integration check of tenant predicates and boundary parameter counts. Representative repeated end-to-end measurements would then determine actual latency impact. No speedup factor or SLO attainment is claimed.
