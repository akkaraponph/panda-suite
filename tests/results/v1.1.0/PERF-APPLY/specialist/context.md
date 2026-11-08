# Performance contracts

`unique(items)` is a public generic helper: preserve first occurrence order,
equality semantics, and support unhashable lists/dicts. Do not change that contract.
`unique_ids(ids)` is a hot path whose contract accepts exact built-in int values
only (no custom objects or int subclasses). Preserve first occurrence order and
return a list. Typical input is 20,000 mostly distinct IDs; empty, duplicate and
negative IDs are valid. No production profile or latency SLO is supplied.

`load_labels(repo, ids, tenant)` returns one result per input ID in original order,
including duplicates and None for missing IDs. `get_label(tenant,id)` makes one
remote query; the supplied contract also provides `get_labels(tenant, ids)` making
one batched query returning a mapping from ID to label for that tenant, omitting
missing IDs. Chunking is needed above a 500-ID query parameter limit. An empty
input should make zero queries. All calls must preserve tenant filtering.
The batch operation reads a consistent snapshot, while old per-item calls may
observe changes between calls; clarify whether this matters before applying it.

`RECENT` keeps the last ten payloads by design. `HISTORY` keeps every payload for
diagnostics, but there is no approved retention policy. It may grow indefinitely;
removing history silently would change observable behavior. Native/RSS measurements
are not supplied. Safe local synthetic checks are allowed; no network, installs,
production profiling, real DB operations, or schema changes are authorized.
