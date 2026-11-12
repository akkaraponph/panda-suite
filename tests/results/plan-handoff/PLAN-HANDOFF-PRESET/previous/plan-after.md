# Plan: Bulk CSV import

**Goal.** Operations staff paste CSV text with the header `sku,name,quantity`.
Every valid row is added through the existing `Inventory.add_item`. They get back
a report: how many rows were added, plus the line number and a readable reason
for each rejected row.

**Scope.** One new module, `bulk_import.py`, and its tests, `test_bulk_import.py`.
`inventory.py` stays unchanged.
**Out of scope** (from `requirements.md`): file upload, HTTP endpoints, persistence.

**Source.** `requirements.md` (items 1–5), `inventory.py`, `test_inventory.py`.

**Constraints (copied from `requirements.md`).**
- Quantity must be a positive whole number. SKUs stay unique.
- One bad row must not stop the remaining rows.
- Python 3.9 standard library only; no new dependencies.

**Execution model.** Each task is meant to be handed to a separate implementer
that sees only that task. Tasks therefore repeat the exact names they use.

## Review focus

These are inputs the requirements imply but do not spell out. Each one has a
test in the task that owns it.

1. **The same SKU twice in one paste.** Expect the first occurrence to be added
   and the second rejected with `duplicate sku: <sku>` at its own line. A SKU
   that already exists in the inventory is rejected the same way. (Task 2)
2. **Quantity forms that Python's `int()` accepts but that are not plain whole
   numbers**: `+3`, `1_000`, `٣` (Arabic-Indic digit), `2.5`, `-1`, `0`, and
   empty. All are rejected with `quantity must be a positive whole number`.
   ` 4 ` (surrounding spaces) is accepted as 4, and `007` is accepted as 7.
   (Task 2)
3. **Line numbers after blank lines or a quoted field that spans lines.** The
   reported line is the row's first physical line in the pasted text. The
   header is line 1. (Task 1)
4. **Wrong column count** (too few or too many fields). The row is rejected with
   `expected 3 fields (sku,name,quantity), got N`. (Task 2)
5. **Missing or wrong header, or empty input.** `import_csv` raises
   `ValueError("CSV header must be: sku,name,quantity")`, and nothing is added.
   (Task 1 raises; Task 2 checks that the inventory is unchanged.)

## Evidence anchors

- `inventory.py:16` `Inventory.add_item(item: Item) -> None`. It raises
  `KeyError(f"duplicate sku: {item.sku}")` for a duplicate SKU and
  `ValueError("quantity must be positive")` for `quantity <= 0`. It is the only
  write path into the inventory.
- `inventory.py:6` `Item` is a frozen dataclass: `sku: str, name: str,
  quantity: int`. It does not validate the type of `quantity` or check for blank
  strings.
- `test_inventory.py`: existing tests use `unittest` and import with
  `from inventory import ...` from the project root.
- Checked locally: `python3 -m unittest -v` from the project root runs 2 tests,
  OK.
- Local interpreter is Python 3.15.0. No `python3.9` is installed (see Risks).
- `csv.reader` was checked locally. A blank line yields `[]`, and a
  whitespace-only line yields `['  ']`. `reader.line_num` is the *last* physical
  line consumed, so a quoted multi-line field ends at a later line than it
  starts. In non-strict mode an unterminated quote at the end of input does
  **not** raise.
- The project is not a Git repository.

## File map

| File | Responsibility | Task |
|---|---|---|
| `bulk_import.py` (new) | `HEADER`, `ParsedRow`, `parse_csv`; then `RejectedRow`, `ImportReport`, `import_csv` | 1, 2 |
| `test_bulk_import.py` (new) | `ParseCsvTest` (Task 1), `ImportCsvTest` (Task 2) | 1, 2 |
| `inventory.py` | Unchanged; called through `Inventory.add_item` | n/a |

## Decisions (defaults chosen; confirm or change before execution)

- **D1. Header handling.** The first CSV record must equal `sku,name,quantity`
  after stripping a leading BOM (`﻿`) and whitespace around each field
  name. Matching is case-sensitive. If the header is missing, wrong, or the
  input is empty, `parse_csv` raises `ValueError("CSV header must be:
  sku,name,quantity")` and the whole import aborts before anything is added.
  *Alternative:* return a report with one rejection at line 1.
- **D2. Blank rows.** A record whose fields are all empty after `strip()`
  (including `[]`) is skipped silently. It is neither added nor rejected.
- **D3. Field trimming.** `sku`, `name`, and `quantity` are each `strip()`ped
  before validation and before the `Item` is built.
- **D4. Required text fields.** An empty `sku` is rejected with
  `sku is required`. An empty `name` is rejected with `name is required`.
  `requirements.md` is silent on this; the default rejects both.
- **D5. Positive whole number.** After stripping, the quantity is accepted only
  if it is non-empty, `str.isascii()` and `str.isdigit()` are both true, and
  `int(value) > 0`. Every other value is rejected with
  `quantity must be a positive whole number`.
- **D6. Report shape.** The report gives only `added` (a count) and
  `rejected`, ordered by line. It does not list which SKUs were added, because
  the requirement asks only for "how many".
- **D7. NUL bytes / malformed records.** Any field containing `\x00` is rejected
  with `row contains a NUL byte`. If a `csv.Error` is raised while reading a
  record, it becomes a parse error on that record and reading continues (see
  Task 1). This keeps behavior the same on Python 3.9 (where the csv module
  raises on NUL) and on newer versions (where it does not).

## Tasks

### Task 1: Parse CSV text into numbered rows

- [ ] **Objective.** Add `parse_csv`, which turns pasted text into data rows that
  keep their source line numbers and validates the header.
- **Files.** Create `bulk_import.py` and `test_bulk_import.py`.
- **Prerequisites.** None.
- **Interfaces (produces; Task 2 consumes these exact names).** All are in
  `bulk_import.py`. They use `typing.Tuple`, `typing.List`, and
  `typing.Optional` for Python 3.9 compatibility; do not use `X | None` or
  `match`.
  - `HEADER: Tuple[str, str, str] = ("sku", "name", "quantity")`
  - `@dataclass(frozen=True) class ParsedRow:` with fields `line: int`,
    `fields: Tuple[str, ...]`, and `error: Optional[str] = None`.
    `fields` holds the raw, unstripped values from `csv.reader`. `error` is
    set only when the csv module raised on that record; in that case
    `fields == ()`.
  - `def parse_csv(text: str) -> List[ParsedRow]`
- **Behavior to implement.**
  - [ ] Read with `csv.reader(io.StringIO(text))`. Strip one leading `﻿`
    from `text` first.
  - [ ] Header: apply D1. On failure, raise
    `ValueError("CSV header must be: sku,name,quantity")`.
  - [ ] Line number of a record is `previous reader.line_num + 1`, where the
    previous value starts at 0. This is the record's *first* physical line.
    The header is line 1.
  - [ ] Skip blank records (D2). Do not emit them.
  - [ ] Wrap each `next(reader)` in `try/except csv.Error as e`. On error,
    append `ParsedRow(line, (), f"malformed CSV: {e}")` and continue reading.
    Stop on `StopIteration`.
  - [ ] Do no field validation here. Column count, quantity, and the NUL check
    all belong to Task 2.
- **Tests (`class ParseCsvTest(unittest.TestCase)` in `test_bulk_import.py`).**
  - [ ] `test_rows_keep_line_numbers`: input
    `"sku,name,quantity\nA-1,Bolt,3\nA-2,Nut,5\n"` gives
    `[ParsedRow(2, ("A-1","Bolt","3")), ParsedRow(3, ("A-2","Nut","5"))]`.
  - [ ] `test_blank_lines_skipped_but_counted`: input
    `"sku,name,quantity\n\nA-1,Bolt,3\n   \nA-2,Nut,5\n"` gives rows at lines
    3 and 5 only.
  - [ ] `test_multiline_quoted_field_uses_first_line`: input
    `'sku,name,quantity\nA-1,"Bolt\nlong",3\nA-2,Nut,5\n'` gives line 2 with
    name `"Bolt\nlong"`, then line 4.
  - [ ] `test_bom_and_padded_header_accepted`: input
    `"﻿ sku , name ,quantity\nA-1,Bolt,3"` gives one row at line 2. This
    also covers input without a trailing newline.
  - [ ] `test_bad_header_raises`: each of `""`, `"A-1,Bolt,3\n"`,
    `"SKU,Name,Quantity\n"`, and `"sku,name\n"` raises `ValueError` with the
    message `CSV header must be: sku,name,quantity`.
  - [ ] `test_header_only_gives_no_rows`: `"sku,name,quantity\n"` gives `[]`.
  - [ ] `test_wrong_field_count_passed_through`: `"sku,name,quantity\nA-1,Bolt\n"`
    gives `[ParsedRow(2, ("A-1","Bolt"))]`. The parser does not reject it.
- **Acceptance.** All `ParseCsvTest` tests pass, and the existing
  `test_inventory.py` still passes.
- **Verify.** Run `python3 -m unittest -v` from the project root. Success means
  all tests pass and none error.
  The `csv.Error` branch cannot be triggered on Python 3.11+ with ordinary
  input. Review it by reading the code; do not force it with mocks.

### Task 2: Validate rows, import them, and report

- [ ] **Objective.** Add `import_csv`. It adds every valid row through
  `Inventory.add_item`, keeps going past bad rows, and returns a report.
- **Files.** Edit `bulk_import.py` and `test_bulk_import.py`. Do not edit
  `inventory.py`.
- **Prerequisites.** Task 1 is merged.
- **Interfaces.**
  - *Consumes* from `bulk_import.py`: `parse_csv(text: str) ->
    List[ParsedRow]`. `ParsedRow` has `line: int`, `fields: Tuple[str, ...]`
    (raw and unstripped), and `error: Optional[str]`. `parse_csv` raises
    `ValueError` for a bad header. *Consumes* from `inventory.py`: `Inventory`,
    `Item(sku: str, name: str, quantity: int)`, and `Inventory.add_item(item)`,
    which raises `KeyError("duplicate sku: <sku>")` or `ValueError`.
  - *Produces*:
    - `@dataclass(frozen=True) class RejectedRow:` with `line: int` and
      `reason: str`
    - `@dataclass(frozen=True) class ImportReport:` with `added: int` and
      `rejected: Tuple[RejectedRow, ...]`, in ascending line order
    - `def import_csv(inventory: Inventory, text: str) -> ImportReport`. Lets the
      `ValueError` from `parse_csv` propagate; this happens before any add.
- **Per-row rules, in this order.** The first failure is the reason. Messages
  are exact.
  - [ ] `row.error` is set → reason is `row.error`.
  - [ ] `len(fields) != 3` → `expected 3 fields (sku,name,quantity), got {n}`.
  - [ ] Any field contains `"\x00"` → `row contains a NUL byte`.
  - [ ] Strip all three fields (D3). Empty sku → `sku is required`. Empty name →
    `name is required`.
  - [ ] Quantity fails D5 → `quantity must be a positive whole number`.
  - [ ] Call `inventory.add_item(Item(sku, name, quantity))`.
    - `KeyError as e` → reason `e.args[0]`, which gives
      `duplicate sku: <sku>`. Do not use `str(e)`, because it adds quotes.
    - `ValueError as e` → reason `str(e)`. This is a backstop; D5 should make
      it unreachable.
    - Any other exception propagates.
  - [ ] Count successful adds into `added`.
- **Tests (`class ImportCsvTest(unittest.TestCase)` in `test_bulk_import.py`).**
  Each test starts from a fresh `Inventory()` unless stated otherwise.
  - [ ] `test_all_valid_rows_added`: two valid rows give
    `ImportReport(added=2, rejected=())`, and `inv.get("A-1").quantity == 3`.
  - [ ] `test_bad_row_does_not_stop_later_rows`:
    `"sku,name,quantity\nA-1,Bolt,3\nA-2,Nut,0\nA-3,Washer,7\n"` gives
    `added == 2`, `rejected == (RejectedRow(3, "quantity must be a positive
    whole number"),)`, and `inv.get("A-3")` exists.
  - [ ] `test_invalid_quantities_rejected`: one row each with quantity `0`,
    `-1`, `2.5`, `+3`, `1_000`, `٣`, `abc`, and an empty quantity. Every row is
    rejected with `quantity must be a positive whole number`, at its own line,
    and `added == 0`.
  - [ ] `test_quantity_whitespace_and_leading_zeros_accepted`: `" 4 "` stores
    4 and `"007"` stores 7.
  - [ ] `test_duplicate_within_paste`: `A-1` on lines 2 and 3 gives
    `added == 1`, the rejection `RejectedRow(3, "duplicate sku: A-1")`, and the
    line 2 item is kept.
  - [ ] `test_duplicate_of_existing_item`: `A-1` is pre-added with
    `Item("A-1","Old",1)`. Importing `A-1` gives `RejectedRow(2, "duplicate
    sku: A-1")`, and `inv.get("A-1").name == "Old"`.
  - [ ] `test_wrong_field_count`: `A-1,Bolt` gives `expected 3 fields
    (sku,name,quantity), got 2`, and `A-1,Bolt,3,x` gives `... got 4`.
  - [ ] `test_blank_sku_or_name`: ` ,Bolt,3` gives `sku is required`, and
    `A-1, ,3` gives `name is required`.
  - [ ] `test_fields_are_stripped`: ` A-1 , Bolt ,3` stores
    `Item("A-1","Bolt",3)`.
  - [ ] `test_nul_byte_rejected`: a row with `"Bo\x00lt"` as the name gives
    `row contains a NUL byte`.
  - [ ] `test_bad_header_adds_nothing`: `"A-1,Bolt,3\n"` raises `ValueError`,
    and the inventory has no `A-1`, so `inv.get("A-1")` raises `KeyError`.
  - [ ] `test_rejections_in_line_order_with_blank_lines`: input that has a blank
    line and two bad rows reports both rejections in ascending order, with the
    physical line numbers.
- **Acceptance.** Each requirement in `requirements.md` items 2–4 has a passing
  test above. `inventory.py` is unchanged. Only `csv`, `io`, `dataclasses`,
  and `typing` are imported, besides `inventory`.
- **Verify.** Run `python3 -m unittest -v` from the project root. Success means
  all `ParseCsvTest`, `ImportCsvTest`, and `InventoryTest` tests pass. Also run
  `grep -nE "^(import|from) " bulk_import.py`, which should show only stdlib
  modules and `inventory`.

## Requirement → task map

| Requirement | Task | Check |
|---|---|---|
| 1. Parse rows that keep line numbers | 1 | `test_rows_keep_line_numbers`, `test_blank_lines_skipped_but_counted`, `test_multiline_quoted_field_uses_first_line` |
| 2. Import through `add_item`; a bad row does not stop the rest | 2 | `test_bad_row_does_not_stop_later_rows`, `test_all_valid_rows_added` |
| 3. Report the added count and each rejected line with a reason | 2 | Every `ImportCsvTest` asserts the `ImportReport` exactly |
| 4. Positive whole quantity; unique SKUs | 2 | `test_invalid_quantities_rejected`, `test_duplicate_within_paste`, `test_duplicate_of_existing_item` |
| 5. Python 3.9 stdlib only | 1, 2 | Import grep and 3.9-safe typing; full 3.9 run is unavailable (see Risks) |

## Risks

- **No Python 3.9 interpreter here.** Tests run on Python 3.15, which can hide
  syntax that 3.9 lacks (`X | Y`, `match`, `dataclass(slots=...)`). Mitigation:
  the interfaces pin `typing` forms, and a reviewer should check for 3.10+
  syntax. Running the tests under a real 3.9 interpreter is **an unverified
  check** until one is available.
- **Version differences in the `csv` module.** NUL bytes raise `csv.Error` on
  3.9/3.10 and parse normally on newer versions. D7 makes both paths end in a
  rejection. The `csv.Error` path cannot be exercised on the local interpreter.
- **`int()` is too permissive.** It accepts `+3`, `1_000`, and Unicode digits.
  D5 and `test_invalid_quantities_rejected` guard against this.
- **The KeyError message gets quoted.** `str(KeyError("x"))` gives `'x'`.
  The plan pins `e.args[0]`, and the duplicate tests check the exact text.

## Verification strategy

Each task is accepted only when `python3 -m unittest -v` passes from the project
root, including the existing `test_inventory.py`. No build, linter, or CI
configuration exists in the project. Python 3.9 compatibility is checked by
review only (see Risks).
