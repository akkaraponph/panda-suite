# Proposed integer hot-path optimization

`work.py:15-16` delegates `unique_ids` to `unique`. In `work.py:8-10`, every input searches the growing result list. With n inputs and u distinct IDs, this costs O(nu), worst-case O(n²) for mostly distinct inputs, and O(u) result memory. This is a code-supported algorithmic bottleneck; its synthetic runtime impact was measured below. No production profile or SLO was provided.

Proposed patch only; source is unchanged:

```diff
--- a/work.py
+++ b/work.py
@@ -12,8 +12,8 @@
     return result
 
 
 def unique_ids(ids):
-    return unique(ids)
+    return list(dict.fromkeys(ids))
 
 
 def load_labels(repo, ids, tenant):
```

Dictionary insertion order preserves first occurrence order, and conversion returns a list. Exact built-in integers have compatible equality/hash semantics, including negative and large integers. Empty input and repeated IDs work. `unique` remains untouched, preserving its generic equality behavior and support for lists/dicts; replacing that helper with hashing would violate its contract. The proposal assumes the stated exact-int contract and does not introduce new runtime type validation.

Dictionary construction is expected O(n), with O(u) temporary dictionary memory in addition to the result. Hash collision-heavy integers can degrade performance to O(n²), and hashing very large integers has a cost proportional to their representation; this is not an unconditional linear-time guarantee.

# Verification and measurements

CPython 3.14.7, macOS 27.2 arm64. A disposable in-memory candidate was compared with the imported original. Three existing unittest cases passed. Equivalence passed for 306 list cases (six boundary cases plus 300 seeded random lists), an iterator case, and generic list/dict/equality regressions. Boundary coverage included empty, repeated, negative, and 100-digit integers.

Synthetic timing used a fixed seed (1729), prebuilt inputs, one untimed warm-up per implementation per workload, seven repeated samples with alternating before/after order, single-threaded execution, no external I/O. Each sample included all dictionary construction and result materialization. Setup, assertions, and tracemalloc were outside timings; timeit used its default GC handling. No application cache was involved; no CPU-cache flushing or machine isolation was performed.

| Input | Calls per sample | Original median ms/call | Proposed median ms/call | Median ratio |
|---|---:|---:|---:|---:|
| 20,000 shuffled IDs, 19,000 distinct | 1 | 738.396 | 0.30125 | 2451× faster |
| 20,000 IDs, 16 distinct | 100 | 0.72819 | 0.12198 | 5.97× faster |
| Empty input | 100 | 0.00004625 | 0.00008000 | 1.73× slower |

The empty-input regression is retained, although these tiny durations are sensitive to timing noise. All raw samples are recorded in ACTIONS.md. These are local synthetic measurements, not production latency or proof of an SLO.

Separate tracemalloc runs on the mostly distinct input measured original peak/current at 153,696/153,696 bytes and candidate peak/current at 884,840/152,056 bytes, with 19,000-element output retained. The candidate uses about 5.76× peak traced allocation in this check due to temporary dictionary storage. This is Python traced memory, not native memory or RSS, and is not a leak assessment.

# Scope and remaining checks

Other supplied evidence does not change this focused patch: `load_labels` makes n remote queries and batching is a separate potential optimization whose snapshot semantics require clarification; it was not changed. `RECENT` is intentionally bounded and `HISTORY` has a code-supported unbounded retention risk, with no approved policy to change. The tiny three-row sequential scan and existing index provide no evidence for an index change; planner cost is not elapsed time.

Validate the proposal on the deployed Python version and representative real ID distributions before extrapolating these ratios. No network, installs, production profiling, DB operations, or source edits were performed. Source and test SHA-256 hashes matched before/after. There is no applied change to roll back; after adoption, rollback would restore the one-line delegation.
