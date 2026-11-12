# Bulk CSV Import: Implementation Plan

## Goal

Operations staff paste CSV text with the header `sku,name,quantity`. Each valid
row is added through the existing `Inventory.add_item`. They get back a report
with the number of rows added and, for each rejected row, its line number and a
readable reason. One bad row must not stop the rows after it.

## Scope

In scope: parsing pasted CSV text, checking each row, importing through
`Inventory.add_item`, and building the report.

Out of scope (from `requirements.md`): file upload, HTTP endpoints, persistence.
`Inventory` and `Item` stay unchanged.

## Source and constraints

- Requirements: `requirements.md` (items 1–5 below are its numbered items).
- Constraint (copied exactly): **"Python 3.9 standard library only; no new dependencies."**
- Constraint: "Quantity must be a positive whole number. SKUs stay unique."
- Existing code is `inventory.py` and `test_inventory.py` (unittest).

## Evidence anchors (current behavior)

- `inventory.py:6-10`: `Item` is `@dataclass(frozen=True)` with `sku: str`,
  `name: str`, `quantity: int`. It does no validation itself.
- `inventory.py:17-22`: `Inventory.add_item(item)` raises
  `KeyError(f"duplicate sku: {item.sku}")` if the SKU already exists. It raises
  `ValueError("quantity must be positive")` if `quantity <= 0`. Otherwise it
  stores the item. A SKU is stored only when no error is raised, so a rejected
  call changes nothing.
- `inventory.py:24-25`: `Inventory.get(sku)` raises `KeyError` for an unknown SKU.
  Tests use it to check what was stored.
- `test_inventory.py`: unittest style. Tests import with `from inventory import Inventory, Item`.
- Checked in this workspace: `python3 -m unittest -v` runs the 2 existing tests
  and prints `OK`. The local interpreter is Python 3.15.0. **No Python 3.9
  interpreter is installed**, so 3.9 compatibility can only be checked by
  reading the code (see Risks).
- Checked: `csv.reader(..., strict=True)` raises `csv.Error("unexpected end of
  data")` for an unterminated quote. Without `strict` it silently swallows the
  rest of the text into one field. Blank lines come back as `[]`. A quoted field
  that spans two lines comes back as one record. Reading `reader.line_num + 1`
  before each `next()` gives the 1-based physical line where the record starts.

## Decisions (made by this plan; change here before execution if wrong)

D1. **Line numbers** are 1-based physical lines of the pasted text. The header
    is line 1. A record that spans several lines (a quoted newline) reports the
    line it starts on.
D2. **Header**: the first non-blank record, with each field stripped of
    surrounding whitespace, must equal `("sku", "name", "quantity")` exactly
    (case-sensitive, same order). If it does not, or the text has no non-blank
    record, nothing is imported. The report is `added=0` with one rejection:
    line = that record's line (or `1` for empty text), reason =
    `"missing or invalid header: expected sku,name,quantity"`.
D3. **Blank lines** (records that are `[]`) are skipped. They are neither added
    nor rejected.
D4. **Whitespace**: each field is stripped of surrounding whitespace before
    validation. Stored `sku` and `name` are the stripped values.
D5. **Quantity** must match `re.fullmatch(r"[0-9]+", value)` after stripping,
    and `int(value)` must be `> 0`. So `"007"` → 7 is accepted. `"0"`, `"-1"`,
    `"+5"`, `"2.0"`, `"1e3"`, `""`, and non-ASCII digits such as `"٣"` and `"²"`
    are rejected. (The ASCII regex is needed because `int("٣") == 3` and
    `"²".isdigit()` is `True`.)
D6. **Empty SKU or name** after stripping is rejected. The requirements do not
    mention name. `Item` would accept `""`, but an item without a name is
    assumed to be an operator mistake. Flagged in Unresolved decisions.
D7. **SKU uniqueness** is delegated to `Inventory.add_item`. It is
    case-sensitive and covers SKUs already in the inventory and earlier rows in
    the same paste. The first occurrence wins and later ones are rejected.
D8. **Malformed CSV** (`csv.Error` with `strict=True`) gives one rejection at
    the line where the failing record starts, with reason
    `"malformed CSV: <csv.Error message>"`. Parsing stops there, because the
    reader cannot reliably resync after a broken quote. Rows already parsed
    before that point are still imported. This is the only case where a bad row
    stops later rows. Flagged in Unresolved decisions.
D9. **Rejections** are listed in ascending line order. A row with several
    problems reports only the first failing check, in this order: field count →
    sku → name → quantity → `add_item`.

## Review focus (inputs the requirements imply that are easy to miss)

1. **Duplicate SKU inside one paste.** The expected behavior is that the first
   row is added and the second is rejected with `duplicate sku: A-1`.
   Test: Task 3 `test_duplicate_within_paste`.
2. **Quantity that `int()` accepts but is not a positive whole number**
   (`"0"`, `"-1"`, `"+5"`, `" 2.0"`, `"٣"`). Each should be rejected with the
   quantity reason and not crash. Test: Task 2 `test_quantity_rejections`.
3. **A bad row in the middle.** The rows after it should still be added.
   Test: Task 3 `test_bad_row_does_not_stop_later_rows`.
4. **Line numbers after blank lines or quoted multi-line fields.** The reported
   line should match what the operator sees in the pasted text.
   Test: Task 1 `test_line_numbers_skip_blank_and_multiline`.
5. **Wrong or missing header.** Nothing should be imported, and the header
   problem should be reported clearly. Test: Task 3 `test_bad_header_imports_nothing`.

## File map

| File | Status | Responsibility |
|---|---|---|
| `bulk_import.py` | new | Data types, `parse_csv`, `row_to_item`, `import_csv` |
| `test_bulk_import.py` | new | unittest tests for the three tasks |
| `inventory.py` | unchanged | `Item`, `Inventory.add_item` (existing contract) |
| `test_inventory.py` | unchanged | Regression suite |

## Shared interfaces (defined in `bulk_import.py`)

All of these are module-level names in `bulk_import.py`. Use `typing.Tuple` /
`typing.Union` or builtin generics (`tuple[...]` is valid in 3.9). Do not use
`X | Y` unions, `match`, or `dataclass(slots=..., kw_only=...)`, because these
are 3.10+.

```text
@dataclass(frozen=True) class Rejection:  line: int; reason: str
@dataclass(frozen=True) class CsvRow:     line: int; fields: Tuple[str, ...]
@dataclass(frozen=True) class ParsedCsv:  rows: Tuple[CsvRow, ...]; rejected: Tuple[Rejection, ...]
@dataclass(frozen=True) class ImportReport: added: int; rejected: Tuple[Rejection, ...]
class RowError(ValueError)   # str(err) is the human-readable reason

HEADER: Tuple[str, str, str] = ("sku", "name", "quantity")
HEADER_REASON = "missing or invalid header: expected sku,name,quantity"

def parse_csv(text: str) -> ParsedCsv                       # Task 1
def row_to_item(row: CsvRow) -> Item                        # Task 2, raises RowError
def import_csv(inventory: Inventory, text: str) -> ImportReport   # Task 3
```

## Tasks

### Task 1: Parse CSV text into numbered rows (requirement 1)

**Objective:** Turn pasted text into data rows with their source line numbers.
Header problems and malformed CSV become `Rejection`s, not exceptions.

**Files:** `bulk_import.py` (new), `test_bulk_import.py` (new).
**Prerequisites:** none.
**Interfaces:** consumes `str`. Produces `Rejection`, `CsvRow`, `ParsedCsv`,
`HEADER`, `HEADER_REASON`, and `parse_csv(text: str) -> ParsedCsv`.
`CsvRow.fields` are **stripped** values (D4), with as many fields as the record
had. The field count is not checked here. Data rows exclude the header and
blank lines.

Steps:
- [ ] In `test_bulk_import.py`, add class `ParseCsvTest(unittest.TestCase)` with:
  - `test_rows_keep_line_numbers`: `parse_csv("sku,name,quantity\nA-1,Bolt,3\nB-2,Nut,5\n")`
    → `rows == (CsvRow(2, ("A-1","Bolt","3")), CsvRow(3, ("B-2","Nut","5")))`,
    `rejected == ()`.
  - `test_line_numbers_skip_blank_and_multiline`:
    `"sku,name,quantity\nA-1,\"Big\nBolt\",3\n\nB-2,Nut,5\n"` → rows at lines
    `2` and `5`. The first row's name is `"Big\nBolt"`.
  - `test_fields_are_stripped`: `"sku,name,quantity\n A-1 , Bolt , 3 \n"` →
    `CsvRow(2, ("A-1","Bolt","3"))`.
  - `test_header_whitespace_tolerated`: header `" sku , name , quantity "` is accepted.
  - `test_wrong_header`: `"sku,qty,name\nA-1,3,Bolt\n"` → `rows == ()`,
    `rejected == (Rejection(1, HEADER_REASON),)`.
  - `test_empty_text`: `""` and `"\n\n"` → `rows == ()`,
    `rejected == (Rejection(1, HEADER_REASON),)`.
  - `test_header_after_leading_blank_line`: `"\nsku,name,quantity\nA-1,Bolt,3\n"`
    → one row at line `3`, no rejections.
  - `test_malformed_csv_stops_with_rejection`:
    `"sku,name,quantity\nA-1,Bolt,3\nB-2,\"Nut,5\nC-3,Washer,1\n"` → `rows ==
    (CsvRow(2, ...),)`. `rejected` has exactly one item with `line == 3` and a
    `reason` that starts with `"malformed CSV: "`.
  - `test_crlf_line_endings`: `"sku,name,quantity\r\nA-1,Bolt,3\r\n"` → one row at line 2.
- [ ] Implement in `bulk_import.py`: `csv.reader(io.StringIO(text), strict=True)`.
  Before each `next()`, record `start = reader.line_num + 1`. Skip `[]`. The
  first non-blank record is the header check (D2). Catch `csv.Error` and emit
  `Rejection(start, "malformed CSV: " + str(err))`, then stop (D8). Do not pass
  `newline` handling beyond `io.StringIO(text)`. CRLF is handled by the
  reader. The CRLF test confirms this.
- [ ] Verify: `python3 -m unittest test_bulk_import -v` → all `ParseCsvTest` tests pass.

**Accept when:** all `ParseCsvTest` tests pass, and `parse_csv` never raises for
any `str` input used in the tests.

### Task 2: Validate one row into an `Item` (requirement 4)

**Objective:** Convert one `CsvRow` into an `Item`, or raise `RowError` with a
readable reason.

**Files:** `bulk_import.py`, `test_bulk_import.py`.
**Prerequisites:** Task 1 (`CsvRow`).
**Interfaces:** consumes `CsvRow` (fields already stripped). Produces
`RowError(ValueError)` and `row_to_item(row: CsvRow) -> Item`. Checks run in
D9 order, and the first failure raises. Exact reasons:

| Check | Reason string |
|---|---|
| `len(fields) != 3` | `f"expected 3 fields (sku,name,quantity), got {n}"` |
| sku empty | `"sku is required"` |
| name empty | `"name is required"` |
| quantity fails D5 | `f"quantity must be a positive whole number, got {value!r}"` |

Steps:
- [ ] Add class `RowToItemTest(unittest.TestCase)` with:
  - `test_valid_row`: `row_to_item(CsvRow(2, ("A-1","Bolt","007")))` == `Item("A-1","Bolt",7)`.
  - `test_wrong_field_count`: fields `("A-1","Bolt")` → `RowError` with str
    `"expected 3 fields (sku,name,quantity), got 2"`. Fields
    `("A-1","Bolt","3","x")` → `"... got 4"`.
  - `test_empty_sku`: `("","Bolt","3")` → `"sku is required"`.
  - `test_empty_name`: `("A-1","","3")` → `"name is required"`.
  - `test_quantity_rejections`: use `subTest` for each of `"0"`, `"-1"`, `"+5"`,
    `"2.0"`, `"1e3"`, `""`, `"abc"`, `"٣"`, `"²"`. Each raises `RowError` with
    str `f"quantity must be a positive whole number, got {value!r}"`.
  - `test_first_failure_wins`: `("", "", "0")` → `"sku is required"`.
- [ ] Implement `RowError` and `row_to_item` in `bulk_import.py` using `re.fullmatch(r"[0-9]+", q)`.
- [ ] Verify: `python3 -m unittest test_bulk_import -v` → `ParseCsvTest` and `RowToItemTest` pass.

**Accept when:** every reason string matches the table exactly, and no input
in the tests raises anything except `RowError`.

### Task 3: Import and report (requirements 2, 3, 4)

**Objective:** Import every valid row through `Inventory.add_item`, keep going
after bad rows, and return an `ImportReport`.

**Files:** `bulk_import.py`, `test_bulk_import.py`.
**Prerequisites:** Tasks 1 and 2.
**Interfaces:** consumes `parse_csv`, `row_to_item`, `RowError`,
`Inventory.add_item` (`inventory.py:17`). Produces `ImportReport` and
`import_csv(inventory: Inventory, text: str) -> ImportReport`.

Behavior:
- `parsed = parse_csv(text)`. For each row: call `row_to_item`, then
  `inventory.add_item(item)`. Count successes in `added`.
- `RowError` → `Rejection(row.line, str(err))`.
- `KeyError` from `add_item` → `Rejection(row.line, f"duplicate sku: {item.sku}")`.
  Build this string yourself. Do not use `str(KeyError)`, because it adds
  quotes.
- `ValueError` from `add_item` (should not happen after Task 2) →
  `Rejection(row.line, str(err))`. Catch it after `RowError`, which is a
  `ValueError` subclass.
- `rejected` = `parsed.rejected` + row rejections, sorted by `line` (D9).
- Do not catch bare `Exception`.

Steps:
- [ ] Add class `ImportCsvTest(unittest.TestCase)` with:
  - `test_all_valid`: two valid rows → `ImportReport(added=2, rejected=())`.
    `inv.get("A-1").quantity == 3`.
  - `test_bad_row_does_not_stop_later_rows`:
    `"sku,name,quantity\nA-1,Bolt,3\nB-2,Nut,0\nC-3,Washer,4\n"` → `added == 2`,
    `rejected == (Rejection(3, "quantity must be a positive whole number, got '0'"),)`.
    `inv.get("C-3")` succeeds. `inv.get("B-2")` raises `KeyError`.
  - `test_duplicate_within_paste`: two rows with SKU `A-1` on lines 2 and 3 →
    `added == 1`, `rejected == (Rejection(3, "duplicate sku: A-1"),)`. The
    stored name is the line-2 name.
  - `test_duplicate_of_existing_item`: inventory pre-loaded with
    `Item("A-1","Bolt",3)`. Pasting `A-1,Other,9` → rejected at line 2 with
    `"duplicate sku: A-1"`, and the stored item is unchanged.
  - `test_bad_header_imports_nothing`: `"sku,qty,name\nA-1,3,Bolt\n"` →
    `ImportReport(0, (Rejection(1, HEADER_REASON),))`. `inv.get("A-1")` raises `KeyError`.
  - `test_rejections_sorted_by_line`: a paste with bad rows on lines 4 and 2
    and a malformed record on line 5 gives a report with lines `[2, 4, 5]`.
  - `test_empty_paste`: `""` → `ImportReport(0, (Rejection(1, HEADER_REASON),))`.
- [ ] Implement `ImportReport` and `import_csv`.
- [ ] Verify: `python3 -m unittest -v` (whole directory) → 2 existing tests and
  all new tests pass, output ends with `OK`.
- [ ] Python 3.9 check (by reading, since no 3.9 interpreter is installed):
  `grep -nE '\|[^|]*(None|int|str)|match |kw_only|slots=' bulk_import.py test_bulk_import.py`
  should find no 3.10+ syntax. Imports are only `csv`, `io`, `re`,
  `dataclasses`, `typing`, `unittest`, `inventory`. If `python3.9` is
  available, run `python3.9 -m unittest -v` and expect `OK`.

**Accept when:** all tests pass, `inventory.py` and `test_inventory.py` are
unchanged, and the module imports only the standard library and `inventory`.

## Requirement → task map

| Requirement | Task(s) | Checks |
|---|---|---|
| 1. Parse rows with line numbers | 1 | `ParseCsvTest` |
| 2. Import via `add_item`; bad row doesn't stop the rest | 3 | `test_bad_row_does_not_stop_later_rows`, `test_duplicate_*` |
| 3. Report: added count + per-rejection line and reason | 3 (types in 1) | `ImportCsvTest` exact `ImportReport` equality |
| 4. Positive whole quantity; unique SKUs | 2, 3 | `test_quantity_rejections`, `test_duplicate_*` |
| 5. Python 3.9 stdlib only | 1–3 | import list + 3.9 syntax check in Task 3 |

## Risks

- **3.9 compatibility can't be checked by running it here** (local Python is
  3.15.0). Mitigation: the syntax and import check in Task 3, plus a CI or
  `python3.9` run if one is available.
- **A malformed quote stops parsing** (D8), so rows after it are not imported.
  Mitigation: an explicit rejection with the line number, and a test.
- **`int()` accepts Unicode digits, signs, and whitespace.** Mitigation: the
  ASCII regex (D5) and `test_quantity_rejections`.
- **The `KeyError` message format** from `add_item` includes repr quotes if
  stringified. Mitigation: the reason string is built explicitly, and the test
  checks it exactly.

## Unresolved decisions (confirm before or during execution)

- D6: whether an empty `name` should be rejected. The plan rejects it.
- D8: whether a malformed CSV quote should stop parsing (the plan's choice) or
  whether you want a different recovery strategy.
- D2: whether a wrong header should reject the whole paste (the plan's choice)
  or whether a header-less paste with three columns should be accepted.
- Whether `added` should also list the added SKUs. Requirement 3 asks only for
  "how many rows were added", so the plan returns a count.

## Verification strategy

- Unit tests per task, as above. Final command: `python3 -m unittest -v` in the
  project root, which should print `OK` with 2 existing tests plus all new tests.
- The existing `test_inventory.py` passing is the regression check for the
  unchanged `inventory.py`.
- The Python 3.9 compatibility check is described in Task 3.
