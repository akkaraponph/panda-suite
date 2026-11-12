# Implementation plan: Bulk CSV import

Source requirements: `requirements.md`. Existing code: `inventory.py` (`Item`, `Inventory`), `test_inventory.py` (unittest).
This plan is self-contained. Execute tasks in order; each task ends with its own verification.

## Context you need

- `Item` is a frozen dataclass `Item(sku: str, name: str, quantity: int)`.
- `Inventory.add_item(item)` raises `KeyError("duplicate sku: ...")` if the SKU exists and `ValueError("quantity must be positive")` if `quantity <= 0`. It is the only way to add items and must stay the import path (requirement 2). Do not change `inventory.py`.
- Tests use `unittest` and run from the project root with `python3 -m unittest -v`. Baseline: 2 tests, all passing.
- Target is **Python 3.9, standard library only**. The local interpreter may be newer, so do not use 3.10+ features: no `X | Y` type unions (use `Optional`/`Union`), no `match`, no `dataclass(slots=True, kw_only=True)`. Built-in generics like `list[int]` are fine in 3.9.
- Out of scope: file upload, HTTP endpoints, persistence. Do not add any.

## Decisions made for this plan (requirements are silent on these)

| Topic | Decision |
|---|---|
| Location | New module `inventory_import.py` beside `inventory.py`; tests in new `test_inventory_import.py`. |
| Line numbers | 1-based physical lines of the pasted text; the header is line 1. A row whose quoted field spans several lines reports the line where the row **starts**. |
| Header | After stripping whitespace around each column name, the header must be exactly `sku,name,quantity` (case-sensitive, that order). A leading UTF-8 BOM (`﻿`) is removed first. Empty input or a wrong header is a whole-input error (`ImportFormatError`), not a rejected row, and nothing is imported. |
| Blank rows | Lines where every field is empty after stripping are skipped silently. They are neither added nor rejected. |
| Whitespace | `sku`, `name` and `quantity` values are stripped of surrounding whitespace before validation and before building the `Item`. |
| Empty fields | Empty `sku` or empty `name` rejects the row. |
| Quantity | Accepted only if the stripped value fully matches `[0-9]+` (ASCII digits) and `int(value) > 0`. So `"5"` and `"007"` are valid; `"0"`, `"-1"`, `"+3"`, `"2.0"`, `"1e3"`, `""` and non-ASCII digits are rejected. |
| Duplicates | Detected by `add_item` raising `KeyError`. Covers SKUs already in the inventory and repeats within the same CSV; the first occurrence wins, later ones are rejected. |
| Partial success | Valid rows are added even when other rows are rejected (requirement 2). No rollback. |
| Malformed CSV (`csv.Error`) | Raise `ImportFormatError` naming the line. Because parsing finishes before any row is added, the inventory is unchanged. |

If a reviewer disagrees with any decision, only the affected task changes.

## Public interface (create exactly these names)

```python
# inventory_import.py
from dataclasses import dataclass
from typing import List, Union
from inventory import Inventory, Item

EXPECTED_HEADER = ("sku", "name", "quantity")

class ImportFormatError(ValueError):
    """The input as a whole cannot be read: empty, wrong header, or malformed CSV."""

@dataclass(frozen=True)
class SourceRow:
    line: int            # 1-based line where the row starts
    values: List[str]    # raw fields as read by csv.reader (not stripped)

@dataclass(frozen=True)
class RejectedRow:
    line: int
    reason: str          # human-readable, e.g. "quantity must be a positive whole number, got '0'"

@dataclass(frozen=True)
class ImportReport:
    added: int
    rejected: List[RejectedRow]   # in source line order

def parse_rows(text: str) -> List[SourceRow]: ...
def validate_row(row: SourceRow) -> Union[Item, RejectedRow]: ...
def import_csv(inventory: Inventory, text: str) -> ImportReport: ...
```

Reason strings (use these exact texts so tests and staff see stable messages):

| Case | Reason |
|---|---|
| Wrong field count | `expected 3 fields (sku,name,quantity), got N` |
| Empty SKU | `sku is required` |
| Empty name | `name is required` |
| Bad quantity | `quantity must be a positive whole number, got '<raw stripped value>'` |
| Duplicate SKU | `duplicate sku '<sku>'` |
| Other `ValueError` from `add_item` (safety net) | `rejected by inventory: <str(exc)>` |

`ImportFormatError` messages: `input is empty; expected header sku,name,quantity`, `line 1: expected header sku,name,quantity, got <comma-joined stripped header>`, `line N: malformed CSV: <csv.Error text>`.

## Tasks

### Task 1: Parse CSV text into line-numbered rows (requirement 1)

Files: create `inventory_import.py` (module docstring, `EXPECTED_HEADER`, `ImportFormatError`, `SourceRow`, `RejectedRow`, `ImportReport`, `parse_rows`); create `test_inventory_import.py` with class `ParseRowsTest`.

Implementation notes:
- Remove a leading `﻿` from `text`.
- Read with `csv.reader(io.StringIO(text, newline=""))` so quoted newlines and `\r\n` are handled by the csv module.
- Track the start line: before each `next(reader)`, `start = reader.line_num + 1`; `reader.line_num` after the call is the end line. csv.reader yields `[]` for an empty line, so the count stays accurate.
- First row is the header. If there is no row at all, or the header is all blank, raise the empty-input `ImportFormatError`. If the stripped header tuple is not `EXPECTED_HEADER`, raise the header `ImportFormatError`.
- For each later row: skip it if every field is empty after stripping; otherwise append `SourceRow(start, row)`.
- Wrap iteration in `try/except csv.Error` and re-raise as `ImportFormatError` with the line number.
- `parse_rows` does no field validation.

Tests (each a separate method):
1. Header plus two data rows gives two `SourceRow`s with lines 2 and 3 and the raw values.
2. Blank lines between rows are skipped and later rows keep their true line numbers (e.g. data on lines 2 and 4).
3. A quoted name containing a newline counts as one row; the row after it reports the correct line.
4. `\r\n` line endings give the same line numbers as `\n`.
5. Header with spaces (` sku , name , quantity `) and a leading BOM are accepted.
6. Empty string and whitespace-only string raise `ImportFormatError`.
7. Wrong header (`sku,qty,name`) raises `ImportFormatError`, and the message mentions line 1.
8. A row with the wrong field count is still returned (validation happens later).

Done when: `python3 -m unittest -v` passes, with the 2 existing tests and the new `ParseRowsTest` tests.

### Task 2: Validate one row into an `Item` or a rejection (requirement 4, row-level part)

Depends on: Task 1.
Files: `inventory_import.py` (add `validate_row` and a private helper such as `_parse_quantity(raw: str) -> Optional[int]`); `test_inventory_import.py` (add `ValidateRowTest`).

Implementation notes:
- Check in this order and return the first failure as `RejectedRow(row.line, reason)`: field count is 3, SKU is not empty, name is not empty, quantity is valid.
- Quantity: `re.fullmatch(r"[0-9]+", value)` then `int(value) > 0`. Do not rely on `str.isdigit()` or bare `int()`. `int()` accepts `"+3"`, `" 3"`, `"1_000"` and non-ASCII digits.
- On success return `Item(sku, name, quantity)` built from stripped values.
- Duplicates are not checked here. That needs the inventory (Task 3).

Tests: one valid row returns the expected `Item` with whitespace stripped. Rejections use the exact reason text and the row's line for: 2 fields, 4 fields, empty sku, whitespace-only name, quantity values `0`, `-1`, `+3`, `2.5`, `1e3`, `abc`, `""`, and `"١"` (Arabic-Indic one). `"007"` is accepted as 7.

Done when: the full suite passes.

### Task 3: Import rows through `Inventory.add_item` and report (requirements 2, 3, 4)

Depends on: Tasks 1 and 2.
Files: `inventory_import.py` (add `import_csv`); `test_inventory_import.py` (add `ImportCsvTest`).

Implementation notes:
- Call `parse_rows(text)` first and let `ImportFormatError` propagate. Nothing has been added at that point.
- For each `SourceRow` in order: `validate_row`; if that gives a `RejectedRow`, record it and continue. Otherwise call `inventory.add_item(item)` inside `try`:
  - `except KeyError`: record `duplicate sku '<sku>'`.
  - `except ValueError as exc`: record `rejected by inventory: {exc}`.
  - on success: increment `added`.
- Catch only those two exception types. Other exceptions are bugs and should surface.
- Return `ImportReport(added=..., rejected=[...])`.

Tests:
1. All rows valid: `added == N`, `rejected == []`, and each item is retrievable with `inventory.get`.
2. Mixed file (valid, bad quantity, valid, wrong field count, valid): `added == 3`; rejected lines and reasons are exact and in order. The valid rows after the bad ones are present, which proves one bad row does not stop the rest.
3. SKU already in the inventory before the import: the row is rejected as duplicate and the existing item is unchanged.
4. The same SKU twice in the CSV: the first is added and the second is rejected with its own line number.
5. A bad header raises `ImportFormatError` and the inventory is unchanged (`get` of a SKU from the CSV raises `KeyError`).
6. A header-only input returns `ImportReport(0, [])`.

Done when: the full suite passes.

### Task 4: Final check

- Run `python3 -m unittest -v` from the project root. Every test passes and the 2 original tests are unchanged.
- If a Python 3.9 interpreter is available, run the suite with it too (`python3.9 -m unittest -v`). If none is available, check by reading the code that it has no 3.10+ syntax, and say in the handoff that 3.9 was not run.
- Check that `inventory.py` is unchanged (`git diff inventory.py` if under version control) and that the only imports are standard library modules (`csv`, `io`, `re`, `dataclasses`, `typing`) plus `inventory`.

## Risks

- **Line numbers with multi-line quoted fields:** the start-line tracking in Task 1 depends on `reader.line_num` semantics. Test 3 in Task 1 guards this.
- **Error-message coupling:** duplicate detection relies on `add_item` raising `KeyError`. If `inventory.py` changes that contract, Task 3 test 3 and test 4 fail. That is intended.
- **Partial imports:** staff could re-paste a whole file after fixing one row. The earlier rows then come back as duplicates. This is expected with "SKUs stay unique" and no rollback. The report makes it visible.
