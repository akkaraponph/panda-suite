# Applied optimization

Changed only `work.py:14-16` behavior: `unique_ids` now uses `list(dict.fromkeys(ids))`. `unique`, data access, history retention, schema and dependencies remain unchanged. Exact built-in integers have compatible equality/hash behavior; insertion-ordered dict keys preserve the first occurrence and the function returns a fresh list. No runtime type validation was added; inputs outside the stated contract are not promised.

## Bottleneck and evidence

**Code-supported:** Previously `unique_ids` delegated to `unique` (`work.py:5-11`), performing a list membership scan for each input. With n inputs and k distinct values, this is O(n*k), quadratic for mostly distinct values. The dict implementation has expected O(n) hash-table work and O(k) additional temporary memory. Hash collision adversarial integers can still cause poor worst-case performance; arbitrary-precision integer hashing also depends on integer size. This is the only ranked bottleneck in the authorized operation; no production profile was supplied.

**Measured synthetic results:** Python 3.14.7, single process/concurrency 1; deterministic prebuilt input, one warm-up and five timed calls per case, result assertions outside timed intervals. Timings include the complete deduplication and result-list creation, excluding input setup. Same harness ran against actual original and changed source in separate processes. No external I/O; CPU cache/GC defaults were uncontrolled, with warm data and no cache flushing. A separate single `tracemalloc` call records Python peak allocations, excluding input allocation; these are not RSS/native or retained-growth measurements.

| Workload | Before median ms | After median ms | Before peak bytes | After peak bytes |
| --- | ---: | ---: | ---: | ---: |
| mostly_distinct_20000 | 738.542417 | 0.203042 | 153696 | 884840 |
| duplicates_20000 | 0.468917 | 0.120125 | 128 | 512 |
| small_6 | 0.000208 | 0.000209 | 32 | 344 |
| empty | 0.000125 | 0.000166 | 0 | 120 |

The typical synthetic case has 20,000 inputs and 18,000 distinct IDs (range -18,000 through -1, followed by the last 2,000 again). All five samples are retained in `before.json` and `after.json`, including the slight small/empty-input regressions, whose sub-microsecond measurements are noise-sensitive. The large-case speedup is local synthetic evidence, not an end-to-end or production SLO result. Peak allocation increases materially because the temporary dict exists during list construction; it is released on return. No cache or long-lived retention was introduced. Query count and I/O behavior are unaffected by this local change.

## Verification and limits

Baseline: `python3 -m unittest -v` passed 3 tests. After change: the same command passed 5 tests, including original generic unhashable behavior, order, duplicates, empty/negative/zero IDs, deterministic randomized equivalence to `unique`, input non-mutation, iterator input and large integers. Both benchmark runs asserted equivalence for every case and timed result.

Applied, locally verified. No production latency, native memory, database, external workload or network checks were run or authorized. No additional checks are necessary for this bounded local task; representative production distribution and memory-budget validation remain prerequisites to broader performance claims. Rollback is reverting `unique_ids` to `return unique(ids)`; there is no persisted state migration.
