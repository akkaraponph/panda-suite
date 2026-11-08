# Memory retention assessment

Scope: read-only source analysis and bounded local synthetic checks. No source edits, production profiling or external data access.

## Findings

1. **HISTORY is the supported unbounded-retention risk (Code-supported, synthetic growth Measured).** `work.py:22,29–30` creates a module-owned list and appends one strong reference per call, with no trimming or cleanup in this file. After n calls it retains n references plus reachable payload graphs. Shared objects are not copied. Context explicitly requires all-payload diagnostics but supplies no approved retention policy. This establishes a growth risk, not an unintended production leak. Removing HISTORY silently changes observable behavior.
2. **RECENT retains at most ten payload references (Code-supported, Measured locally).** `work.py:21,25–26` uses `deque(maxlen=10)` and evicts the oldest reference on overflow. Count is bounded; bytes are not bounded without a payload-size limit. Ten large or subsequently mutated payloads can consume substantial memory. An evicted payload remains alive if HISTORY or another owner still references it.
3. **High RSS alone cannot prove RECENT leaks.** No RSS/native measurement is supplied. RSS includes native allocations and allocator-resident pages; it can remain high after Python objects become unreachable. Traced Python allocations, peak allocations, retained objects and process RSS are different measures. The colleague's attribution is unsupported.

## Actual checks

CPython 3.14.7, single process/thread. Each path began with both containers cleared and GC, followed by tracing. Three consecutive batches each allocated and recorded 100 fresh 16-KiB bytearrays; GC preceded each sample. Payload allocation is deliberately included to observe retention. Current traced bytes are baseline-subtracted; peaks are raw traced bytes. Harness bookkeeping contributes small overhead. These are repeated equivalent batches within one run per path, not independent production samples.

| Path | Calls | Entries | Current traced delta, bytes | Peak traced bytes |
|---|---:|---:|---:|---:|
| RECENT | 100 | 10 | 165,802 | 182,451 |
| RECENT | 200 | 10 | 166,018 | 182,715 |
| RECENT | 300 | 10 | 166,170 | 182,819 |
| HISTORY | 100 | 100 | 1,645,060 | 1,645,314 |
| HISTORY | 200 | 200 | 3,290,080 | 3,290,334 |
| HISTORY | 300 | 300 | 4,935,196 | 4,935,450 |

After clearing both containers and GC, traced deltas were 1,904 bytes and 608 bytes respectively. Clearing occurred only in this disposable process. A weak-reference check confirmed that a payload recorded in both containers survived RECENT eviction, then became unreachable after HISTORY was cleared. This demonstrates ownership without RSS inference.

All 3 supplied unittest tests passed (IDs, generic unhashables, bounded RECENT). No optimized implementation was tested because none was applied. No measured speedup or production savings are claimed.

## Safe optimization direction

Keep the established last-ten RECENT behavior. Prioritize establishing HISTORY's required diagnostic lifetime and consumers: whether all payloads must remain available, how long, whether consumers depend on object identity or later mutations, and whether persistent storage is acceptable. Only then choose an approved retention/storage design. A bounded deque would discard diagnostics and bound entry count only; it would not guarantee a byte bound. Sampling, clearing, removing history or changing payload representation also changes semantics and requires an established contract.

No behavior-preserving retention diff is justified by the available evidence, so none is supplied or applied. A concrete safe next experiment is an authorized representative local allocation/ownership trace with RECENT-only, HISTORY-only and shared payloads, repeated batches and cleanup. Obtain separately authorized RSS/native measurements if the RSS report needs attribution. This is an investigation direction, not an invented retention policy.

Remaining limits: real payload distribution, other owners/call sites, diagnostic consumers and native/RSS behavior are unknown; no production profile or SLO was supplied. Broader memory optimization is blocked on retention semantics. There are no before/after optimization results or rollback steps because source behavior was preserved.
