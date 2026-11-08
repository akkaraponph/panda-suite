# Optimization proposal

`unique_ids` delegates to `unique`, which linearly searches the growing result list for each item. For mostly distinct input this makes roughly n(n−1)/2 equality comparisons: O(n²) time with O(n) result storage. This is the demonstrated local bottleneck, not a production profiling finding.

Apply this concrete diff only to the integer-specific helper:

```diff
--- a/work.py
+++ b/work.py
@@ -11,7 +11,7 @@
 
 
 def unique_ids(ids):
-    return unique(ids)
+    return list(dict.fromkeys(ids))
 
 
 def load_labels(repo, ids, tenant):
```

Dictionary insertion order preserves first occurrence order; the final conversion returns a list. Exact built-in integers are hashable and their equality semantics agree with dictionary key matching. Empty input, duplicates, negative integers, large integers, and iterable inputs remain supported. `unique` remains unchanged, retaining its generic equality behavior and support for unhashable lists/dicts. No validation is added for values already excluded by the `unique_ids` contract.

Expected time is O(n) with ordinary hash distribution, plus O(k) dictionary storage for k distinct IDs alongside the returned list. Hash collisions can worsen dictionary performance; this is not a universal worst-case linear guarantee, and enormous integer hashing has additional bit-length cost. The optimization trades auxiliary memory for speed.

# Local verification

The three supplied unittest tests passed. An in-memory patched module matched the original on 257 deterministic integer list cases and their iterator equivalents, three generic-helper cases, and the representative benchmark input. Cases included empty, duplicate-only, negative, distinct, randomized, and arbitrary-size integers. Both source and proposed implementations were executed in isolated namespaces; source was not edited.

On CPython 3.14.7, 20,000 shuffled integers containing 18,000 distinct values (90% distinct), with one warmup each and seven single-call samples per implementation in alternating order:

| Measurement | Before | Proposed |
|---|---:|---:|
| Median duration | 0.686792 s | 0.000314375 s |
| Observed duration range | 0.686331–0.705534 s | 0.000293541–0.000398958 s |

The ratio of medians was about 2,185× in this bounded synthetic microbenchmark. This is evidence for this workload and machine only; no production latency SLO, production profile, or memory/RSS measurement was supplied. Short candidate timings are susceptible to runtime noise. `work.py` SHA256 remained `367b0450aa96c95e3fcd25412a7a33b04f52d32a102b3a64d959823e530f94b0`.

# Other supplied context

`load_labels` has an independent remote-query amplification opportunity: deduplicate IDs for tenant-scoped `get_labels(tenant, chunk)` calls in chunks of at most 500, combine mappings, then reconstruct one result per original ID using mapping lookup with `None` for missing values. Empty input should issue no queries. Before applying that separate change, clarify whether the consistent batch snapshot is acceptable compared with per-item calls observing changes. No batching change is included here.

`RECENT` already has its intended ten-item bound. `HISTORY` may grow indefinitely, but changing retention requires an approved policy; do not silently remove history. The three-row synthetic sequential scan does not establish a database bottleneck or justify another index, especially with an existing index and no timings/buffers. No network, installs, database actions, or schema changes were performed.
