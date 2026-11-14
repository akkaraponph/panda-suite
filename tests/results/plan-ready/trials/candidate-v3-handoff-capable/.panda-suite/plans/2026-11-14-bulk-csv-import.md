# Bulk CSV import implementation plan

## Goal, scope, sources, and constraints

Add an in-memory Python API for operations staff to import pasted CSV and receive a partial-success report. No implementation is authorized by this plan.

Requirements from `requirements.md`: R1 parse rows with source line numbers; R2 route each valid row through `Inventory.add_item` and continue after rejected rows; R3 report added count and each rejection's line/reason; R4 positive whole-number quantity and unique SKUs; R5 Python **3.9 standard library only**, no new dependencies. File upload, HTTP endpoints, and persistence are excluded.

Current sources: `inventory.py` defines frozen `Item(sku: str, name: str, quantity: int)`, `Inventory.add_item(item: Item) -> None`, and `Inventory.get(sku: str) -> Item`. `add_item` raises `KeyError` for duplicates before checking quantity and raises `ValueError` for nonpositive quantity. `test_inventory.py` asserts successful insertion and duplicate rejection only. Preserve those public interfaces and their current behavior, including direct callers' validation behavior.

## Proposed decisions and contracts

These are implementation choices for the new API, not claims about existing behavior:

- New module `csv_import.py`, depending on `inventory.py`; inventory must not depend on the importer. New public function `import_csv(inventory: Inventory, text: str) -> ImportReport` mutates the supplied inventory and returns a report.
- Frozen dataclasses: `RejectedRow(line_number: int, reason: str)` and `ImportReport(added_count: int, rejected_rows: Tuple[RejectedRow, ...])`. Rejections are in source order. Use `typing.Tuple` for Python 3.9 compatibility. No report includes inventory internals.
- A CSV record occupies one physical source line. Use `csv.reader([line], strict=True)` independently for each nonblank physical line, supporting quoted commas and escaped quotes. Embedded newlines in quoted fields are unsupported; reject affected physical lines instead of allowing one malformed quote to consume later valid rows. This explicit line-oriented dialect is a proposed scope choice for pasted item rows. Source line numbers are one-based and include blank lines. Preserve physical line endings when passing lines to the reader (`splitlines(keepends=True)`), so quoted embedded newline fragments are rejected.
- First physical line must parse to exactly `['sku', 'name', 'quantity']`. No BOM or whitespace normalization for headers. Empty text, a blank/malformed/wrong header produces `RejectedRow(1, 'expected header sku,name,quantity')`, zero additions, and no processing of later lines. Header-only input is a successful empty import. Non-string input is outside this typed API contract; do not add speculative coercion or a new public runtime error guarantee.
- After the header, skip whitespace-only physical lines; they do not count as added or rejected. Reject malformed CSV with reason prefix `invalid CSV:` and wrong field counts with `expected 3 fields`. Continue on the next physical line.
- Preserve parsed SKU and name exactly, including spaces and empty strings; requirements do not impose additional SKU/name validation. Quantity alone is stripped of surrounding whitespace and must match ASCII `[0-9]+` and convert to an integer greater than zero. Accept `01` as 1. Reject empty/whitespace, `0`, negatives, signs, fractions, exponent notation, underscores, and non-ASCII digits with `quantity must be a positive whole number`. Conversion failures, including runtime integer conversion limits, are row rejections with that reason.
- Duplicate matching is exactly the existing case-sensitive SKU matching, both against preexisting inventory and earlier successful rows. First successful occurrence wins. A row failing parsing/quantity validation never reserves its SKU.
- Every validated row becomes `Item(sku, name, quantity)` and is passed once to `Inventory.add_item`. Increment added count only after that call returns. Convert its `KeyError` into `duplicate sku: <sku>` without exception-string quotation artifacts; convert its `ValueError` to a human-readable rejection. Do not catch arbitrary exceptions: unexpected programming/dependency failures propagate and earlier successful additions remain. Expected row failures never roll back successful rows.
- Internal parser contract: `_parse_row(line: str, line_number: int) -> Item` raises `ValueError` with the reasons above for CSV/shape/quantity failures. Header handling and blank-line skipping belong to `import_csv`. `_parse_row` is private; no separate parsed-row model is needed.

## Affected files

| File | Responsibility |
| --- | --- |
| `csv_import.py` (new) | Report dataclasses, private row parser, public import orchestration |
| `test_csv_import.py` (new) | Parser and import behavior, report content, delegation, and failure isolation |
| `inventory.py` | Existing dependency; no planned changes |
| `test_inventory.py` | Existing regression suite; preserve |

## Ordered tasks

- [ ] **T1 — Define reports and parse one source row.** Requirements R1, R3, R4, R5. No prerequisites. Add the exact proposed dataclasses and `_parse_row(line: str, line_number: int) -> Item` in `csv_import.py`, and focused tests in `test_csv_import.py`. Produces these types and helper for T2; the helper does not insert inventory entries. It must parse quoted commas/escaped quotes and preserve SKU/name, convert valid digit quantities, and raise `ValueError` for malformed CSV, field counts other than three, and invalid quantities using the contract above. `line_number` is carried by orchestration into `RejectedRow`, not added to `Item`. Verify positive values and leading zeros, surrounding quantity whitespace, empty/zero/negative/fraction/sign/exponent/underscore/Unicode quantities, empty SKU/name, two/four fields, unmatched quotes, and a quoted newline fragment. Assertions must inspect returned `Item` fields or error reasons, not merely absence of exceptions. Planned command: `python3 -m unittest -v test_csv_import`.

- [ ] **T2 — Import all rows with observable partial success.** Requirements R1–R5. Prerequisite T1. Consume `Item`, `_parse_row`, `RejectedRow`, and `ImportReport` exactly as specified above; produce `import_csv(inventory: Inventory, text: str) -> ImportReport`. Add its docstring describing the line-oriented dialect, exact header, partial mutation, and report semantics. In `test_csv_import.py`, exercise header validation, blank lines, line ordering, mixed validity, and duplicates. Use an `Inventory` spy/subclass to prove each valid item calls `add_item` exactly once, and use `get` to prove final inventory contents and unchanged rejected duplicates. Inject a `ValueError` on one otherwise valid item and prove the following valid row is still added. Inject an unexpected `RuntimeError` and assert propagation plus preservation of prior additions. Preserve existing inventory callers and tests. Planned command: `python3 -m unittest -v`. Document an API example in the new public function docstring showing `added_count` and `rejected_rows` access. No extra infrastructure or unrelated validation changes.

## Review focus and discriminating checks

| Likely omission or wrong implementation | Required result and owning check |
| --- | --- |
| Stops on a bad quantity or duplicate | T2 mixed fixture: existing `EXIST`; header line 1, `A,Bolt,2` line 2, `B,Nut,0` line 3, blank line 4, `EXIST,Other,1` line 5, `A,Other,4` line 6, `C,Washer,3` line 7. Assert count 2, rejection lines exactly `[3,5,6]`, nonempty specific reasons, A/C inserted and EXIST unchanged. |
| Uses `int` alone and accepts `1_0` or `+2` | T1 invalid-quantity table asserts rejection for both and all contract cases. |
| Naively splits commas or numbers filtered rows | T1 quoted-name fixture retains comma; T2 blank-line fixture retains physical line numbers. |
| Malformed quote consumes subsequent records | T2 unmatched quote on line 2 followed by `OK,Name,1` on line 3 yields one line-2 rejection and one addition. Quoted multiline fragments are rejected as specified. |
| Counts before insertion or bypasses inventory | T2 spy verifies calls, injected `ValueError` yields no increment, and subsequent row succeeds; unexpected exception propagates. |

## Requirement traceability and evidence

| Requirement | Tasks | Check / expected evidence |
| --- | --- | --- |
| R1 source lines | T1, T2 | Quoting and blank/malformed-line tests assert exact source lines and parsed values. |
| R2 continue and delegate | T2 | Mixed fixture, spy calls, injected row failure; later valid items retrievable. |
| R3 report | T1, T2 | Exact count, rejection ordering, line integers, and specific human-readable reasons. Empty/header-only input cases assert exact reports. |
| R4 whole quantities / uniqueness | T1, T2 | Quantity table, existing/intra-batch duplicate tests; rejected row followed by valid row of same SKU succeeds. |
| R5 Python 3.9 stdlib | T1, T2 | Review imports and syntax; run complete unittest suite using Python 3.9 when available. No dependency files added. |
| Preserved API | T2 | Existing `test_inventory.py` remains green without changes. |

Baseline observation: `python3 -m unittest -v` currently passes its two existing tests. This proves no importer acceptance behavior. No new checks have run; all task checks remain planned. Python 3.9 runtime availability has not been verified; running under another `python3` alone cannot prove 3.9 compatibility.

No deployment, migration, or versioned release boundary is requested; release gates are omitted. This is additive in-memory behavior. Recovery from expected bad rows is continuation; callers can discard a newly created Inventory to abandon an import. There is no transactional rollback or persistence. The report is the requested operational visibility; no telemetry subsystem is needed.

## Readiness and handoff

**EXECUTION-READY** for T1 and T2 under the explicit proposed CSV dialect and API choices above. No unresolved implementation blockers. First unblocked task: T1. Remaining evidence gaps: all new acceptance tests and actual Python 3.9 execution. Checkboxes remain unchecked until acceptance evidence exists.

Recommend **native** execution: two small tasks with one private parser/type dependency and bounded in-memory impact; one fresh whole-change reviewer is proportional. The host also supports subagent-driven execution, with a fresh implementer and reviewer for each task followed by whole-change review. User review and execution authorization are still required. Ready-to-use request: `Use panda-execute (native) to implement .panda-suite/plans/2026-11-14-bulk-csv-import.md`.

Workspace is not a Git repository, so repository `.gitignore`, tracked-plan detection, and `git check-ignore` do not apply; no ignore file or index changes are planned.
