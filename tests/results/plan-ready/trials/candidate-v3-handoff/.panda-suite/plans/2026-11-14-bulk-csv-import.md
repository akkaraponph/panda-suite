# Bulk CSV inventory import

## Goal, scope, and sources

Add a callable bulk import for operations staff pasting `sku,name,quantity` CSV. Return successes and row-specific rejections while preserving valid additions. Planning only; implementation is not authorized by this artifact.

Mandatory requirements from `requirements.md`: R1 parse rows with source line numbers; R2 call `Inventory.add_item` for each valid row and continue after rejection; R3 report added count and each rejected line/reason; R4 positive whole-number quantities and unique SKUs; R5 Python 3.9 standard library only. No uploads, HTTP endpoints, persistence, dependencies, or changes to direct inventory callers.

Established source: `inventory.py` defines frozen `Item(sku: str, name: str, quantity: int)`, `Inventory.add_item(self, item: Item) -> None`, and `Inventory.get(self, sku: str) -> Item`. Duplicate SKU raises `KeyError` before quantity validation; nonpositive quantity raises `ValueError`. It does not enforce integer types itself. Preserve these signatures and behavior. `test_inventory.py` asserts successful addition/get and duplicate rejection only.

## Proposed contract and decisions

All new interfaces below are proposed. Put them in `csv_import.py`; import `Inventory` and `Item` from `inventory`, never access `_items`. Dependencies point from CSV import to inventory, with no reverse dependency.

- `@dataclass(frozen=True) ParsedRow`: `line_number: int`, `sku: str`, `name: str`, `quantity_text: str`.
- `@dataclass(frozen=True) ImportErrorRow`: `line_number: int`, `reason: str`.
- `@dataclass(frozen=True) ImportReport`: `added: int`, `errors: List[ImportErrorRow]`.
- `parse_csv(text: str) -> Tuple[List[ParsedRow], List[ImportErrorRow]]`.
- `import_csv(inventory: Inventory, text: str) -> ImportReport`.

Use `typing.List` and `typing.Tuple`, compatible with Python 3.9. Reasons are nonempty human-readable strings; do not make callers parse them. Errors are returned in ascending source-line order. Each rejected source row contributes one error.

Proposed paste-format policy: one CSV record per physical line, parsed with standard-library `csv.reader([line], strict=True)`. This preserves deterministic recovery after malformed quotes. Quoted commas and doubled quotes work; embedded newlines in quoted fields are rejected as separate malformed physical rows. This is an explicit format limitation, not a capability of general CSV. Document it in the importer docstring and tests. If multiline fields become required, revise framing and recovery together before implementing that expansion.

Header is physical line 1 and must parse exactly as `['sku', 'name', 'quantity']` in that order. Empty input, blank first line, missing/extra/reordered columns, BOM, or malformed header produce `ImportReport(0, [ImportErrorRow(1, 'expected header sku,name,quantity')])`; do not process later lines without a valid header. This file-level failure differs from a rejected data row.

Use `text.splitlines()` for line numbering (LF and CRLF); a final line terminator creates no additional row. After a valid header, each physical line must parse into exactly three fields. A blank or whitespace-only data line is rejected, as are too few/many fields and CSV syntax errors; later physical lines continue. Retain SKU/name strings exactly, including spaces and case. Empty SKU/name fields remain accepted because the existing inventory accepts them and requirements add no restriction. Duplicate comparison remains exact and case-sensitive. Do not silently trim or normalize fields.

Quantity text must match ASCII `[0-9]+` and convert to an integer greater than zero. Accept `01` as 1. Reject omission (wrong column count), empty string, whitespace, sign prefixes, decimal/exponent notation, non-ASCII digits, zero, and negatives. Catch integer-conversion `ValueError` (including runtime digit-limit rejection) as a row error. Pass an actual `int` to `Item`; do not change `Inventory.add_item` to enforce importer rules globally.

`parse_csv` returns shape/syntax rejections and parsed rows; an invalid header returns no parsed rows and one error at line 1. `import_csv` validates quantities, calls `add_item` in source order, increments `added` only after a successful call, converts `KeyError`/`ValueError` from that call to row errors, and merges errors in source order. Use a readable duplicate reason such as `duplicate sku: A-1`, without KeyError's display quotes. Catch these exceptions only around expected conversion/addition operations; unexpected exceptions propagate. No retries, batch rollback, or all-or-nothing transaction. Earlier successes survive later rejected rows; repeating an import rejects previously added SKUs, and a rejected first occurrence must not reserve its SKU.

## Files and responsibilities

| File | Responsibility |
| --- | --- |
| `csv_import.py` (new) | Report/row models, CSV parsing, validation, orchestration; docstring documents public entry point and paste-format limitation |
| `test_csv_import.py` (new) | Parser and end-to-end import assertions, including continuation and compatibility |
| `inventory.py` | Reused unchanged as the sole insertion/uniqueness authority |
| `test_inventory.py` | Existing regressions retained unchanged |

## Ordered work

- [ ] **T1 — Parse the paste format and retain source lines.** Requirements R1, R3, R5. Prerequisites: none. Create the three proposed dataclasses and `parse_csv(text: str) -> Tuple[List[ParsedRow], List[ImportErrorRow]]` in `csv_import.py`; produce exactly the types and header/data-line behavior above for T2. Add parser tests in `test_csv_import.py`. Acceptance/check C1: exact header plus `A-1,"Bolt, large",3` returns `ParsedRow(2, 'A-1', 'Bolt, large', '3')`; escaped quotes preserve text; CRLF and trailing newline retain correct numbering without a phantom row. C2: every invalid header variant returns no rows and exactly one line-1 error. C3: malformed quote, blank row, wrong column count, then a valid row preserve the valid row and report the actual rejected physical lines, with nonempty reasons. A parser that aborts at the first bad row, silently skips blanks, or splits quoted commas must fail these checks. Confirm the documented multiline limitation with a rejected embedded-newline fixture. Verification: parser cases in `python3 -m unittest -v test_csv_import`.

- [ ] **T2 — Import valid rows and account for every outcome.** Requirements R2–R5. Prerequisite: T1; consumes `ParsedRow`, `ImportErrorRow`, `ImportReport`, and `parse_csv` with their exact contracts above. Produce `import_csv(inventory: Inventory, text: str) -> ImportReport`. Add end-to-end tests to `test_csv_import.py` and entry-point examples in its module docstring. Acceptance/check C4: mixed valid, invalid quantity, existing duplicate, in-batch duplicate, and later valid rows produce the exact added count and error line list, nonempty meaningful reasons, and inventory contents asserted with `get`; rejected unique SKUs remain absent. Include a first invalid quantity followed by a valid row with the same SKU, which must succeed. C5: a parameterized quantity matrix covers `1`, `01`, `0`, `-1`, `+1`, `1.0`, `1e2`, empty, spaces, and non-ASCII digits; test a missing column separately. Assert success values are integers and failures do not mutate inventory. C6: an `Inventory` subclass recording calls proves each eligible row goes through `add_item`; a subclass raising `ValueError` for one SKU proves a later valid row still imports; a subclass raising `RuntimeError` proves unexpected failures are not swallowed. C7: exact SKU/name preservation, empty fields, repeat import, and header failure all follow the contract; an invalid header makes zero insertion calls. Assert errors remain source-ordered when parsing and insertion errors interleave. Verification: `python3 -m unittest -v`; inspect imports for standard-library-only usage and validate syntax/runtime on Python 3.9 where available.

T1 → T2 is the only dependency. Checkboxes remain unchecked until implementation and the named checks produce evidence.

## Review focus

| Easily missed behavior | Expected outcome | Owning check |
| --- | --- | --- |
| Malformed row followed by valid row | Reject malformed physical line; import following valid line | T1/C3, T2/C4 |
| Invalid first occurrence of SKU | Later valid occurrence succeeds | T2/C4 |
| Parse and insertion errors interleaved | One source-ordered report, accurate count | T2/C4, C7 |
| Existing adder accepts noninteger positive values | Importer rejects fractional text without altering adder behavior | T2/C5; existing regressions |
| Invalid header with valid-looking following rows | Zero insertion calls, line-1 error | T1/C2, T2/C7 |

## Traceability and expected evidence

| Requirement | Tasks | Checks | Evidence to obtain |
| --- | --- | --- | --- |
| R1 source-numbered CSV | T1 | C1–C3 | Parsed-field and exact-line assertions |
| R2 reuse adder; continue | T2 | C4, C6 | Recording adder calls, post-failure inventory contents |
| R3 counts/rejection report | T1, T2 | C2–C4, C7 | Exact count, error count/order/lines and readable reasons |
| R4 positive integer and unique SKU | T2 | C4, C5, C7 | Quantity matrix, existing/in-batch/repeat duplicate assertions |
| R5 Python 3.9 stdlib | T1, T2 | C1–C7; import/runtime inspection | Full suite on Python 3.9 and dependency inspection |

Planning observations: `python3 -m unittest -v` currently passes the two existing tests. This does not establish any import behavior or Python 3.9 compatibility. No project runner/configuration exists in the supplied fixture; unittest command is confirmed from the current suite. Python 3.9 availability has not been checked; its run remains an evidence gap, and the execution environment's `python3` version is not assumed to be 3.9. No release/deployment/migration boundary is requested, so no release gates are defined.

Risks: the single-physical-line paste format must stay visible to callers; arbitrary multiline CSV requires a separate recovery decision. Partial successes intentionally remain on failure; the report is the source of outcome visibility. Inventory owns live state; no concurrent-use guarantee exists in the current code, and none is introduced. Reverting the new importer module/callers is feasible; imported in-memory additions have no bulk rollback facility and expire with the owning inventory instance. No persistent migration is involved.

## Readiness and handoff

**EXECUTION-READY** for the proposed paste-format contract above. First unblocked task: T1. No blocked task IDs or unresolved implementation decisions; future multiline support is outside this proposed contract. Evidence gaps: all new checks are planned only, and Python 3.9 execution remains unverified. Review the explicit CSV format and field policies before authorizing implementation.

Recommend native execution: two sequential tasks share a small typed interface and affect only an in-memory inventory; one whole-change review is proportional. Ready-to-use request: `Use panda-execute (native) to implement .panda-suite/plans/2026-11-14-bulk-csv-import.md.` This plan is not authorization to implement.
