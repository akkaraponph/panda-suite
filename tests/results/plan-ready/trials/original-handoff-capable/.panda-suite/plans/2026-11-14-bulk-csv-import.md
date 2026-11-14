# Bulk CSV import implementation plan

## Goal and scope

Allow operations staff to paste CSV headed `sku,name,quantity`, import every valid row through `Inventory.add_item`, and receive an added count and rejected rows with source line numbers and human-readable reasons. Implement parsing, validation, import orchestration, and unit tests only. File upload, HTTP endpoints, and persistence are out of scope.

Constraints from `requirements.md`: **Python 3.9 standard library only; no new dependencies.** Quantity must be a positive whole number; SKUs stay unique. One bad row must not stop remaining rows. Do not implement during this planning task.

## Evidence and current behavior

- `requirements.md:1–17` supplies the complete requested behavior and exclusions.
- `inventory.py:6–10`: immutable `Item(sku: str, name: str, quantity: int)`.
- `inventory.py:17–22`: `Inventory.add_item(self, item: Item) -> None` rejects duplicate SKUs with `KeyError`, rejects nonpositive quantities with `ValueError`, then stores the item. It does not enforce integer types; the CSV boundary must enforce whole numbers.
- `inventory.py:24–25`: `get` exposes stored items for assertions.
- `test_inventory.py`: two unittest tests cover insertion and duplicate rejection. `python3 -B -m unittest -v` currently passes both on Python 3.14.7. Python 3.9 compatibility is a separate check; its interpreter has not been established as available.
- This fixture is not a Git repository. No `.gitignore` change or `git check-ignore` applies. No package manager, third-party test runner, or application layer exists.

## Decisions and assumptions

These choices define the proposed CSV boundary; they do not change `Inventory`:

- Use the standard `csv` module's Excel dialect with strict parsing, comma separators, and ordinary double-quote escaping. Accept LF and CRLF and correctly quoted commas and multiline fields.
- Line numbers are one-based physical source lines. A logical record uses its first physical line, including multiline records. Blank physical lines between records are ignored; lines inside a quoted field belong to that record.
- Require the first record to equal exactly `['sku', 'name', 'quantity']`. Empty input, an invalid header, or malformed header returns zero additions and one rejection at line 1 (`missing header` or `expected header: sku,name,quantity`); do not interpret later lines as data. Header errors are input-level failures.
- Each data record requires exactly three fields. Preserve SKU and name strings, including spaces; do not add empty-field restrictions the requirements do not request. SKU comparison remains the existing exact, case-sensitive comparison.
- Strip surrounding quantity whitespace, require one or more ASCII digits, convert to `int`, and require a value greater than zero. Thus `1`, `001`, and ` 2 ` pass; empty, `0`, `-1`, `+1`, `1.0`, and `1e2` fail with `quantity must be a positive whole number`.
- Recovery from malformed quoting must not swallow subsequent valid rows: parse one logical record from the remaining physical lines. On `csv.Error`, reject the attempted record's starting line (`invalid CSV: <parser message>`), advance by one physical line, and retry. On success, advance by the number of physical lines the reader consumed. This recovery can produce separate rejections for continuation lines of malformed records; it preserves subsequent independently valid records. A well-formed multiline record is consumed once.
- Return rejections in source order. A duplicate preserves the existing item; within one batch, the first valid occurrence wins. Convert the expected `KeyError`/`ValueError` from `add_item` to row rejections using `str(exc.args[0])` so duplicate reasons have no exception-added quotes. Unexpected programming errors propagate.

## Review focus

The following less obvious failures belong in the owning task's tests:

1. An unterminated quoted field before a valid row must reject its starting line and still import that later row (tasks 1 and 2).
2. Quoted multiline names must preserve their value and make later rejection line numbers reflect physical lines (tasks 1 and 2).
3. A rejected first occurrence of a SKU must not prevent a later valid occurrence from being added (task 2).
4. A duplicate against an existing item or an earlier accepted row must preserve the original item and allow the next distinct SKU (task 2).
5. Omitted fields, empty quantity, and extra fields must be distinguished from a valid three-field row with empty SKU/name (task 1).

## File map and interfaces

- `inventory.py`: existing storage boundary; unchanged.
- New `bulk_import.py`: result types, parser, and import orchestration below. All annotations must work on Python 3.9.
- New `test_bulk_import.py`: parser and import unittest cases.
- `test_inventory.py`: existing regression suite, unchanged.

Task 1 produces these public contracts in `bulk_import.py`:

- `@dataclass(frozen=True) RejectedRow`: `line_number: int`, `reason: str`.
- `@dataclass(frozen=True) ParsedRow`: `line_number: int`, `item: Item`.
- `parse_csv(text: str) -> List[Union[ParsedRow, RejectedRow]]`: ordered data outcomes, or the single header rejection. Successful headers and blank lines produce no outcome. No inventory is mutated.

Task 2 consumes those exact names and produces:

- `@dataclass(frozen=True) ImportReport`: `added_count: int`, `rejected_rows: List[RejectedRow]`.
- `import_csv(inventory: Inventory, text: str) -> ImportReport`: parse, attempt each `ParsedRow` through the supplied inventory's `add_item`, count successful calls, and merge expected insertion failures into the ordered rejection list. Return ordinary Python objects; no rendering layer.

## Ordered implementation tasks

### 1. Parse and validate CSV with source locations

- [ ] **Objective:** Implement the result types and `parse_csv` contract in `bulk_import.py`, with tests in `test_bulk_import.py`. Prerequisite: this plan is approved for execution. Consumes `Item`; produces `ParsedRow`, `RejectedRow`, and `parse_csv` for task 2.
- [ ] Cover `test_parse_header_and_empty_input`: header-only input returns `[]`; empty text rejects line 1 with `missing header`; wrong order, absent columns, extra columns, or malformed header rejects line 1 with `expected header: sku,name,quantity` and yields no data items.
- [ ] Cover `test_parse_values_and_row_shapes`: verify the exact accepted/rejected quantity examples above; a two-field or four-field row rejects with `expected 3 fields`; `,,1` produces `Item('', '', 1)`; empty quantity gets the quantity reason. Preserve original SKU/name whitespace.
- [ ] Cover `test_parse_csv_locations_and_recovery`: LF/CRLF, escaped quotes, quoted commas, blank lines, and a name spanning lines 2–3 followed by an invalid quantity on line 4. Assert the multiline row starts at line 2 and the rejection is line 4. An unmatched quote on line 2 followed by `B,Bolt,2` on line 3 must yield a line-2 CSV rejection then a valid line-3 row. Check the stable prefix `invalid CSV:` rather than Python-version-specific parser text.
- [ ] Implement the physical-line cursor recovery algorithm in the decisions section, including strict CSV parsing and validation before constructing an `Item`.
- [ ] **Acceptance/check:** `python3 -B -m unittest -v test_bulk_import` passes all parser assertions. Parser calls do not create or modify an inventory. No dependency or storage changes.

### 2. Import independently and report results

- [ ] **Objective:** Add `ImportReport` and `import_csv` to `bulk_import.py`, and orchestration tests in `test_bulk_import.py`. Depends on task 1's exact parser/result contracts and the existing `Inventory.add_item` signature; no other prerequisite.
- [ ] Cover `test_mixed_batch_continues`: prepopulate `A`; submit `B,Bolt,2` (line 2), `C,Nut,0` (line 3), duplicate `A` (line 4), duplicate `B` (line 5), and `D,Washer,3` (line 6). Assert `added_count == 2`, rejection lines `[3, 4, 5]`, exact quantity and `duplicate sku: A`/`duplicate sku: B` reasons, original A and B preserved, and D available.
- [ ] Cover `test_invalid_first_occurrence_can_be_retried`: invalid `B` quantity followed by valid B yields one rejection and one addition. Cover `test_parser_rejections_do_not_stop_import`: malformed quoting then valid row yields one addition; the multiline location fixture preserves the line-4 rejection in the report.
- [ ] Cover `test_report_and_insertion_boundary`: empty/header-only/wrong-header inputs return the parser's expected report with zero calls to `add_item`; a recording Inventory subclass confirms each parsed valid row is passed through `add_item` exactly once. A subclass raising `ValueError('quantity must be positive')` for one item yields that row's reason and continues to the next; a `RuntimeError` propagates.
- [ ] Implement the orchestration and add a short public API docstring giving header, line-number, recovery, and report semantics. Increment the count only after a successful insertion.
- [ ] **Acceptance/check:** `python3 -B -m unittest -v` passes both existing inventory tests and the new parsing/import tests; no source changes beyond the new importer module and its tests.

## Dependencies, risks, and verification

Task 2 follows task 1; separate commits or separate agents are optional execution choices. There are no migrations, deployment steps, persistence changes, or new logging requirements. Imports deliberately retain earlier successful additions when a later row fails; the report tells the caller what happened. Retrying the same input will report previously added SKUs as duplicates rather than inserting them again.

Risks are malformed CSV recovery (task 1 recovery test), inaccurate physical lines (multiline/CRLF assertions), silently accepting non-whole quantities (exact quantity table), and bypassing uniqueness or counting failed inserts (task 2 mixed-batch and recording-subclass tests).

- [ ] Run `python3 -B -m unittest -v`; success means every existing and new test passes.
- [ ] Run `python3.9 -B -m unittest -v` if Python 3.9 is available. This command is proposed, not verified in this fixture; if unavailable, record that compatibility remains unexecuted and inspect for Python 3.10+ syntax/APIs and non-standard imports.
- [ ] Review the diff: `Inventory` behavior unchanged, no dependencies, upload/HTTP/persistence work, or unrelated artifacts.

Requirement coverage: source lines and CSV parsing → task 1 location tests; every valid row via `add_item` and continuation → task 2 boundary/recovery tests; count and per-row report → task 2 mixed batch; positive whole quantities → task 1 value tests; unique SKUs → task 2 duplicate tests; Python 3.9/standard library → both tasks and compatibility verification.

## Execution handoff

Planning only is authorized. Review this plan before implementation. No implementation has started. Two tasks share explicit result types and parsing semantics; choose native execution for the small scope and lower context cost, with a fresh whole-change review afterward. Subagent-driven execution is also supported by the host: a fresh implementer and fresh reviewer for each task, followed by whole-change review, at a higher context cost.

Ready request after review: `Use panda-execute (native) to implement .panda-suite/plans/2026-11-14-bulk-csv-import.md.` The user can instead choose subagent-driven execution. Preserve this artifact, acceptance values, decisions, and the unexecuted Python 3.9 check during handoff.
