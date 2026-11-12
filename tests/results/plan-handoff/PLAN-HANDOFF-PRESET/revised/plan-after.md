# Bulk CSV import: implementation plan

## Goal

Operations staff paste CSV text with the header `sku,name,quantity`. Every valid
row is added through the existing `Inventory.add_item`. They get back a report
with the number of rows added and, for each rejected row, its line number and a
reason a person can read.

## Scope

- In scope: parsing pasted CSV text, importing rows row by row, the import report.
- Out of scope (from `requirements.md`): file upload, HTTP endpoints, persistence.
- No change to `Inventory` or `Item` in `inventory.py`.

## Source and constraints

- Requirement: `requirements.md`, items 1 to 5.
- Current behavior: `inventory.py`. `Inventory.add_item(item: Item) -> None` raises
  `KeyError(f"duplicate sku: {item.sku}")` for a repeated SKU and
  `ValueError("quantity must be positive")` when `quantity <= 0`. `Item` is a frozen
  dataclass `(sku: str, name: str, quantity: int)`.
- Existing tests: `test_inventory.py` (`unittest`). The command
  `python3 -m unittest -v` run in the project root currently passes 2 tests.
- Constraints copied from the requirement:
  - "Quantity must be a positive whole number. SKUs stay unique."
  - "Python 3.9 standard library only; no new dependencies."
  - "one bad row must not stop the remaining rows."
- The local interpreter is Python 3.15. Running the tests on it does not prove 3.9
  compatibility (see Risks).

## Assumptions and decisions (please confirm while reviewing)

These choices are not stated in the requirement. The plan uses them as written.

1. **Line numbers are physical, 1-based, and the header is line 1.** A row's line
   number is the line where the row starts. This matters for a quoted field that
   contains a newline.
2. **The header is checked first.** After trimming whitespace from each cell, the
   first non-blank line must be exactly `sku`, `name`, `quantity` in that order.
   Text that is empty, has only blank lines, or has a wrong header raises
   `CsvImportError` with a message, and nothing is imported. This is a problem with
   the whole input, so it is not a row rejection.
3. **Blank lines are skipped.** They are not counted as added or rejected.
4. **Whitespace is trimmed from every field.** A row is rejected if its SKU or name
   is empty after trimming. The requirement does not cover blank SKU or name; this
   is the plan's choice.
5. **"Positive whole number" means ASCII digits only and a value of at least 1.**
   After trimming, the quantity must fully match `[0-9]+`. Leading zeros are
   allowed (`007` gives 7). The plan does not rely on `int()` alone because, as
   checked locally, `int("1_0") == 10` and `int(" +3 ") == 3`.
6. **Duplicates are handled by `add_item`.** A SKU already in the inventory, or one
   repeated in the CSV, is rejected by the existing `KeyError`. With repeats in the
   CSV, the first one wins.
7. **A failed import is not rolled back.** The rows already added stay added. This
   follows from requirement 2.

## Review focus

These are inputs the requirement implies but does not test directly. Each has a
test in the task that owns it.

1. **A duplicate SKU inside the same paste.** Expected: the first row is added, and
   the later row is rejected with the line number and `duplicate sku: <sku>`.
   (Task 2)
2. **Quantity of `0`, `-1`, `1.5`, `abc`, `1_0`, `+3`, or blank.** Expected: each one
   is rejected with `quantity must be a positive whole number`, and the rows after
   it are still imported. (Task 2)
3. **A row with too few or too many fields.** Expected: rejected with
   `expected 3 fields, got N`. (Task 2)
4. **A quoted name that contains a newline.** Expected: the line numbers of all
   later rows stay correct. (Task 1)
5. **A wrong or missing header.** Expected: `CsvImportError` is raised and nothing
   is imported. (Task 1)

## Files and responsibilities

| File | Status | Responsibility |
|------|--------|----------------|
| `csv_import.py` | new | `CsvImportError`, `CsvRow`, `parse_csv` (Task 1); `RejectedRow`, `ImportReport`, `import_csv` (Task 2) |
| `test_csv_import.py` | new | `unittest` tests for both tasks |
| `inventory.py` | unchanged | `Inventory.add_item` is the only write path |
| `test_inventory.py` | unchanged | regression suite |

## Tasks

### Task 1: Parse CSV text into numbered rows

**Objective:** Requirement 1. Turn pasted text into rows that keep their source
line numbers, and check the header.

**Files:** `csv_import.py` (new), `test_csv_import.py` (new).
**Prerequisites:** none.

**Interfaces it produces** (Task 2 uses these exact names):

```python
class CsvImportError(ValueError): ...

@dataclass(frozen=True)
class CsvRow:
    line: int               # 1-based physical line where the row starts; header is line 1
    fields: List[str]       # raw cells as csv.reader returned them, not trimmed

def parse_csv(text: str) -> List[CsvRow]: ...   # data rows only, header excluded
```

**Steps:**

- [ ] In `csv_import.py`, use `csv.reader(io.StringIO(text))`. Get each row's start
  line from the reader's `line_num` *before* the row is read, plus 1. A local check
  on a quoted field containing a newline showed that `line_num` after the read gives
  the row's last line, not its first.
- [ ] Skip rows that are `[]` (blank lines), including blank lines before the header.
- [ ] If the first non-blank row, with each cell trimmed, is not
  `["sku", "name", "quantity"]`, raise
  `CsvImportError("missing or invalid header: expected sku,name,quantity")`. Raise
  the same error when there is no non-blank row at all.
- [ ] If `csv.Error` is raised while reading (for example, a NUL character), raise
  `CsvImportError(f"line {n}: {err}")`. Do not return a partial result, because the
  reader cannot be trusted to continue after the error.
- [ ] Use Python 3.9 syntax only: `typing.List`, no `X | Y` unions, no `match`, no
  `dataclass(slots=..., kw_only=...)`.
- [ ] Add `ParseCsvTest` to `test_csv_import.py` with these tests:
  - `test_rows_keep_line_numbers`: `"sku,name,quantity\nA-1,Bolt,3\nA-2,Nut,5\n"`
    returns `[CsvRow(2, ["A-1","Bolt","3"]), CsvRow(3, ["A-2","Nut","5"])]`.
  - `test_blank_lines_skipped_but_counted`: `"sku,name,quantity\n\nA-1,Bolt,3\n"`
    returns one row with `line == 3`.
  - `test_multiline_quoted_field_keeps_later_line_numbers`:
    `'sku,name,quantity\nA-1,"Big\nBolt",3\nA-2,Nut,5\n'` returns rows at lines 2
    and 4, and the first name is `"Big\nBolt"`.
  - `test_header_with_spaces_accepted`: `" sku , name , quantity \nA-1,Bolt,3"`
    returns one row at line 2.
  - `test_wrong_header_raises`: `"sku,qty,name\nA-1,3,Bolt"` raises `CsvImportError`.
  - `test_empty_text_raises`: `""` and `"\n\n"` each raise `CsvImportError`.
  - `test_header_only_returns_empty`: `"sku,name,quantity\n"` returns `[]`.

**Acceptance:** all `ParseCsvTest` tests pass. `parse_csv` never trims or validates
data cells.

**Verify:** run `python3 -m unittest -v` in the project root. Success means every
test passes: the 2 existing tests and the 7 new ones.

### Task 2: Import rows and build the report

**Objective:** Requirements 2, 3, and 4. Validate each row, add the valid ones
through `Inventory.add_item`, and report the rejected ones without stopping.

**Files:** `csv_import.py`, `test_csv_import.py`.
**Prerequisites:** Task 1.

**Interfaces:**

- Uses `parse_csv`, `CsvRow`, and `CsvImportError` from Task 1, and
  `Inventory` and `Item` from `inventory.py`.
- Produces:

```python
@dataclass(frozen=True)
class RejectedRow:
    line: int
    reason: str

@dataclass
class ImportReport:
    added: int
    rejected: List[RejectedRow]   # in line order

def import_csv(inventory: Inventory, text: str) -> ImportReport: ...
```

`import_csv` lets `CsvImportError` from `parse_csv` propagate, and in that case
nothing is added.

**Steps:**

- [ ] For each `CsvRow`, check the following in this order and record the first
  failure as `RejectedRow(row.line, reason)`. Use these exact reasons:
  - The number of fields is not 3: `f"expected 3 fields, got {len(fields)}"`
  - The SKU is empty after trimming: `"sku is required"`
  - The name is empty after trimming: `"name is required"`
  - The trimmed quantity does not fully match `[0-9]+`, or its `int` value is less
    than 1: `"quantity must be a positive whole number"`
- [ ] For a row that passes, call
  `inventory.add_item(Item(sku, name, int(quantity)))` with the trimmed values.
  Catch `KeyError` and use the reason `f"duplicate sku: {sku}"`. Do not use
  `str(err)`, because that wraps the message in quotes. Catch `ValueError` and use
  `str(err)`. Any other exception propagates.
- [ ] Count `added` only when `add_item` returns without raising.
- [ ] Add `ImportCsvTest` to `test_csv_import.py`. Each test starts from a new
  `Inventory()`.
  - `test_all_valid_rows_added`: two valid rows give `added == 2`, `rejected == []`,
    and `inv.get("A-2").quantity == 5`.
  - `test_bad_row_does_not_stop_later_rows`:
    `"sku,name,quantity\nA-1,Bolt,0\nA-2,Nut,5\n"` gives `added == 1`,
    `rejected == [RejectedRow(2, "quantity must be a positive whole number")]`, and
    A-2 is in the inventory.
  - `test_invalid_quantities_rejected`: test each of `0`, `-1`, `1.5`, `abc`, `1_0`,
    `+3`, and `""` (use `subTest`). Each is rejected with
    `"quantity must be a positive whole number"`.
  - `test_quantity_with_spaces_and_leading_zero_accepted`: `" 007 "` is added with
    quantity 7.
  - `test_duplicate_within_csv_rejected`: rows `A-1,Bolt,3` (line 2) and `A-1,Nut,1`
    (line 3) give `added == 1`,
    `rejected == [RejectedRow(3, "duplicate sku: A-1")]`, and
    `inv.get("A-1").name == "Bolt"`.
  - `test_duplicate_of_existing_item_rejected`: the inventory already holds A-1, and
    importing A-1 is rejected with `"duplicate sku: A-1"`.
  - `test_wrong_field_count_rejected`: `A-1,Bolt` gives `"expected 3 fields, got 2"`,
    and `A-1,Bolt,3,x` gives `"expected 3 fields, got 4"`.
  - `test_blank_sku_and_name_rejected`: `" ,Bolt,3"` gives `"sku is required"`, and
    `"A-1, ,3"` gives `"name is required"`.
  - `test_rejected_lines_follow_source_with_multiline_field`: a quoted multi-line
    name in the row on line 2, then a bad row, gives a reported line of 4.
  - `test_bad_header_imports_nothing`: a wrong header raises `CsvImportError`, and
    `inv._items` is still empty. Alternatively, check that `inv.get` raises
    `KeyError` for the row's SKU.

**Acceptance:** all `ImportCsvTest` tests pass. One bad row never stops the later
rows. Every rejected row has its source line and one of the exact reasons above.
`inventory.py` is unchanged.

**Verify:** run `python3 -m unittest -v` in the project root. Success means every
test passes: the 2 existing tests, the 7 from Task 1, and the 10 new ones.

## Requirement traceability

| Requirement | Task | Check |
|-------------|------|-------|
| 1. Parse into rows with line numbers | 1 | `ParseCsvTest` line-number and multi-line tests |
| 2. Import through `add_item`, keep going after a bad row | 2 | `test_bad_row_does_not_stop_later_rows` |
| 3. Report the added count and each rejected row's line and reason | 2 | `ImportReport` assertions in every `ImportCsvTest` |
| 4. Positive whole quantity; SKUs unique | 2 | quantity and duplicate tests |
| 5. Python 3.9 standard library only | 1, 2 | only `csv`, `io`, `re`, `dataclasses`, `typing`; 3.9 syntax rules in Task 1 (manual review) |

## Risks

- **Python 3.9 compatibility is not tested.** Only Python 3.15 is available here.
  The reviewer should check for 3.10+ syntax by reading the code. If a 3.9 interpreter
  is available, run `python3.9 -m unittest -v`. Treat this as an open check.
- **Line numbers with multi-line fields.** This is covered by tests in both tasks.
- **`int()` accepts more than "whole number"** (`1_0`, `+3`). Covered by the regex
  rule and `test_invalid_quantities_rejected`.
- **Malformed CSV (`csv.Error`).** Handled as an error for the whole input, with no
  partial import. If staff should instead get partial results for this case, that is
  a policy change to decide before Task 1.

## Verification strategy

Each task ends with `python3 -m unittest -v` in the project root. The final check is
the full suite: 19 tests passing (2 existing, 7 from Task 1, 10 from Task 2).
Python 3.9 compatibility is checked by reading the code unless a 3.9 interpreter is
available.
