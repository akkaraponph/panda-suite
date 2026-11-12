# Plan: Bulk CSV import

## Goal

Let operations staff paste CSV text with the header `sku,name,quantity` and add
many items at once. Every valid row goes through `Inventory.add_item`. The caller
gets back a report with the number of rows added and, for each rejected row, its
line number and a reason a person can read.

## Scope

- In scope: parsing pasted CSV text, validating each row, importing rows, and
  building the report. All of this goes in one new module with its own tests.
- Out of scope (from `requirements.md`): file upload, HTTP endpoints,
  persistence. No changes to `Inventory` or `Item`.

## Source

- `requirements.md`: requirements 1 to 5, quoted below.
- `inventory.py`: `Item(sku: str, name: str, quantity: int)` is a frozen
  dataclass. `Inventory.add_item(item)` raises `KeyError(f"duplicate sku: {sku}")`
  for an existing SKU and `ValueError("quantity must be positive")` when
  `quantity <= 0`. SKUs are matched exactly, so case and whitespace count.
- `test_inventory.py`: uses `unittest`. `python3 -m unittest -v` from the project
  root runs 2 tests and passes (checked 2026-11-12).

## Constraints (copied from requirements)

1. Parse the CSV text into rows that keep their source line numbers.
2. Import every valid row through the existing `Inventory.add_item`; one bad row
   must not stop the remaining rows.
3. Return a report listing how many rows were added and, for each rejected row,
   its line number and a human-readable reason.
4. Quantity must be a positive whole number. SKUs stay unique.
5. Python 3.9 standard library only; no new dependencies.

Python 3.9 compatibility: the local interpreter is Python 3.15.0, so running the
tests here does not prove 3.9 compatibility. Do not use `match`, `X | Y` type
unions, `dataclass(slots=..., kw_only=...)`, or other features added after 3.9.
Use `typing.List` and `typing.Tuple`, or built-in generics, which 3.9 supports.

## Decisions and assumptions

These are assumptions. The requirements do not settle them, and none of them
changes the structure of the plan. They are fixed here so the implementation and
tests agree. Change them before execution if the product owner disagrees.

- **D1. Line numbers.** Lines are 1-based physical lines of the pasted text, so
  the header is line 1. A row's line is the line where its record starts. This
  matters when a quoted field spans more than one line.
- **D2. Header.** The first non-blank record must equal `sku,name,quantity` after
  stripping each field. The match is case-sensitive. If the text is empty, has
  only blank lines, or has a different header, no row can be read reliably. In
  that case the whole call raises `CsvHeaderError` (a `ValueError` subclass) and
  nothing is imported. A header with no data rows returns
  `ImportReport(added=0, rejected=())`.
- **D3. Blank lines** are skipped silently. They are neither added nor rejected.
- **D4. Whitespace.** Leading and trailing whitespace is stripped from `sku`,
  `name`, and `quantity`. After stripping, `sku` and `name` must not be empty.
- **D5. Quantity.** After stripping, the value must match `[0-9]+` exactly
  (use `re.fullmatch`, not `str.isdigit`, which accepts digits like `²`), and
  `int(value) > 0`. So `0`, `-2`, `+3`, `3.5`, `3.0`, `abc`, and an empty value
  are all rejected.
- **D6. Duplicates.** A SKU that already exists in the inventory, or one that
  appeared on an earlier accepted row in the same paste, is rejected because
  `add_item` raises `KeyError`. The first occurrence wins.
- **D7. Atomicity.** The import is not atomic. Valid rows stay added even when
  other rows are rejected, as requirement 2 asks.

## Review focus

These are inputs the requirements imply but no current test covers, most likely
first. Each one has a test in the task that owns it.

1. **Bad quantity values** (`0`, `-2`, `3.5`, `abc`, empty, ` 4 `). The bad rows
   are rejected with the quantity reason. ` 4 ` is accepted as 4. Owner: Task 2.
2. **Duplicate SKU in the same paste or already in the inventory.** The second
   one is rejected and the import continues. Owner: Task 2.
3. **A quoted name containing a comma or a newline.** The name is parsed whole,
   and the rows after it keep their correct line numbers. Owner: Task 1.
4. **Wrong field count** (`A-1,Bolt` or `A-1,Bolt,3,x`). The row is rejected and
   the next row is still imported. Owner: Task 2.
5. **Missing or wrong header, blank lines, trailing newline.** These follow D2
   and D3. Owner: Task 1.

## File map

| File | Change | Responsibility |
| --- | --- | --- |
| `csv_import.py` | new | Parse rows with line numbers, validate them, call `add_item`, build the report |
| `test_csv_import.py` | new | `unittest` tests for parsing and importing |
| `inventory.py` | unchanged | Existing uniqueness and positive-quantity rules |
| `test_inventory.py` | unchanged | Regression suite |

## Tasks

### Task 1: Parse CSV text into numbered rows

Objective: turn pasted text into data rows that know their source line, using
the standard `csv` module (constraints 1 and 5, D1 to D3).

Files: `csv_import.py`, `test_csv_import.py`. Prerequisites: none.

Interfaces (produced, used by Task 2):

- `class CsvHeaderError(ValueError)` with the message
  `"expected header 'sku,name,quantity'"`.
- `@dataclass(frozen=True) class CsvRow` with fields `line: int` and
  `fields: Tuple[str, ...]`. The fields are raw, not stripped, and their count is
  not checked.
- `def parse_rows(text: str) -> List[CsvRow]` raises `CsvHeaderError` under D2.

Algorithm (left open by the signature): read with
`csv.reader(io.StringIO(text))`. Before each `next()`, the record's start line is
the reader's previous `line_num + 1`. Skip records that are `[]` (blank lines).

- [ ] Write tests in `test_csv_import.py` (`ParseRowsTest`):
  - `test_rows_keep_line_numbers`: `"sku,name,quantity\nA-1,Bolt,3\nB-2,Nut,5\n"`
    gives lines `[2, 3]` and `fields == ("A-1", "Bolt", "3")` for the first row.
  - `test_blank_lines_skipped_and_counted`: `"sku,name,quantity\n\nA-1,Bolt,3\n"`
    gives one row with `line == 3`.
  - `test_quoted_multiline_field`:
    `'sku,name,quantity\nA-1,"Bolt, long\nM8",3\nB-2,Nut,5\n'` gives
    `[CsvRow(2, ("A-1", "Bolt, long\nM8", "3")), CsvRow(4, ("B-2", "Nut", "5"))]`.
  - `test_wrong_header_raises`: `"sku,title,qty\nA-1,Bolt,3"` raises
    `CsvHeaderError`.
  - `test_empty_text_raises`: both `""` and `"\n\n"` raise `CsvHeaderError`.
  - `test_header_only_returns_no_rows`: `"sku,name,quantity\n"` gives `[]`.
  - `test_header_fields_are_stripped`: `" sku , name , quantity \nA-1,Bolt,3"`
    gives one row.
- [ ] Implement `CsvHeaderError`, `CsvRow`, and `parse_rows` in `csv_import.py`.
- [ ] Verify with `python3 -m unittest -v`. Success: all `ParseRowsTest` tests and
  the 2 existing tests pass.

Accept when every test above passes and only `csv`, `io`, `dataclasses`, and
`typing` are imported.

### Task 2: Validate and import rows, return a report

Objective: import every valid row through `Inventory.add_item`, keep going after
bad rows, and report the count added and the reasons for rejected rows
(constraints 2 to 4, D4 to D7).

Files: `csv_import.py`, `test_csv_import.py`. Prerequisites: Task 1.

Interfaces:

- Consumes `parse_rows`, `CsvRow`, `CsvHeaderError` from Task 1, and `Inventory`
  and `Item` from `inventory.py`.
- Produces:
  - `@dataclass(frozen=True) class RejectedRow` with fields `line: int` and
    `reason: str`.
  - `@dataclass(frozen=True) class ImportReport` with fields `added: int` and
    `rejected: Tuple[RejectedRow, ...]`, in source order.
  - `def import_csv(inventory: Inventory, text: str) -> ImportReport`.
    `CsvHeaderError` from `parse_rows` is not caught, so it propagates (D2).

Reason strings (pinned; the first failing check wins, in this order):

| Check | Reason |
| --- | --- |
| field count is not 3 | `expected 3 fields (sku,name,quantity), got {n}` |
| stripped sku is empty | `sku is required` |
| stripped name is empty | `name is required` |
| quantity fails D5 | `quantity must be a positive whole number, got '{raw_stripped}'` |
| `add_item` raises `KeyError` | `duplicate sku: {sku}` (built by `import_csv`, not `str(exc)`, because `str(KeyError)` adds quotes) |

Validate quantity before calling `add_item`. That way the `ValueError` raised by
`add_item` stays a safety net and is not reached for parsed rows. Catch only
`KeyError` around `add_item`, so programming errors are not reported as
rejected rows.

- [ ] Write tests in `test_csv_import.py` (`ImportCsvTest`):
  - `test_imports_valid_rows`: two valid rows give `added == 2`,
    `rejected == ()`, and `inventory.get("B-2").quantity == 5`.
  - `test_bad_row_does_not_stop_import`: rows `A-1,Bolt,3` (line 2),
    `B-2,Nut,abc` (line 3), and `C-3,Washer,7` (line 4) give `added == 2` and
    `rejected == (RejectedRow(3, "quantity must be a positive whole number, got 'abc'"),)`.
    `C-3` is retrievable.
  - `test_quantity_rules`: subTests with `0`, `-2`, `+3`, `3.5`, `3.0`, and an
    empty value are each rejected with the quantity reason. ` 4 ` is accepted
    with quantity `4`.
  - `test_duplicate_in_same_paste`: `A-1,Bolt,3` then `A-1,Nut,1` give
    `added == 1`, `RejectedRow(3, "duplicate sku: A-1")`, and the stored name
    stays `"Bolt"`.
  - `test_duplicate_of_existing_item`: with `A-1` added beforehand, importing
    `A-1,Nut,1` gives `added == 0` and `RejectedRow(2, "duplicate sku: A-1")`.
  - `test_field_count`: `A-1,Bolt` gives the reason with `got 2`, and
    `A-1,Bolt,3,x` gives the reason with `got 4`.
  - `test_required_fields`: `,Bolt,3` gives `sku is required`, and `A-1, ,3`
    gives `name is required`.
  - `test_whitespace_stripped`: `" A-1 , Bolt , 3 "` stores
    `Item("A-1", "Bolt", 3)`.
  - `test_header_error_propagates_and_imports_nothing`: a wrong header raises
    `CsvHeaderError`, and the inventory stays empty.
- [ ] Implement `RejectedRow`, `ImportReport`, and `import_csv` in
  `csv_import.py`.
- [ ] Verify with `python3 -m unittest -v`. Success: all tests pass, including
  the 2 tests in `test_inventory.py`.
- [ ] Check that `inventory.py` and `test_inventory.py` are unchanged.

Accept when every requirement-mapped test passes and one bad row never prevents
a later valid row from being added.

## Requirement traceability

| Requirement | Task | Check |
| --- | --- | --- |
| 1 Parse with line numbers | Task 1 | `test_rows_keep_line_numbers`, `test_quoted_multiline_field`, `test_blank_lines_skipped_and_counted` |
| 2 Import via `add_item`, continue after bad rows | Task 2 | `test_bad_row_does_not_stop_import`, `test_imports_valid_rows` |
| 3 Report count and rejected rows with reasons | Task 2 | exact `ImportReport` and `RejectedRow` assertions in all `ImportCsvTest` tests |
| 4 Positive whole quantity; unique SKUs | Task 2 | `test_quantity_rules`, `test_duplicate_in_same_paste`, `test_duplicate_of_existing_item` |
| 5 Python 3.9 standard library, no dependencies | Tasks 1 and 2 | import review; Python 3.9 not available locally (see Risks) |

## Risks

- **Python 3.9 compatibility cannot be checked locally** (only 3.15.0 is
  installed). Mitigation: avoid features added after 3.9 (see Constraints), and
  run `python3.9 -m unittest -v` wherever 3.9 is available. Until then, this
  check is unverified.
- **Malformed quoting** (for example, an unclosed quote) makes `csv` read the
  rest of the text as one field. That row is then rejected by the field-count or
  quantity checks, and the rows after it are swallowed without any error. This
  is accepted as a known limitation and not tested. Raise it if staff paste
  hand-edited CSV often.
- **`KeyError` from `add_item` is the duplicate signal.** If `Inventory` later
  raises `KeyError` for something else, it will be mislabelled as a duplicate.
  `test_duplicate_of_existing_item` pins the current behavior.

## Verification strategy

From the project root, run `python3 -m unittest -v`. Success means
`test_inventory`, `ParseRowsTest`, and `ImportCsvTest` all pass, with 0 failures
and 0 errors. The Python 3.9 run is still to do.
