# Plan: Bulk CSV import

## Goal

Let operations staff paste CSV text with the header `sku,name,quantity` and add
many items to an `Inventory` in one call. Valid rows go in through the existing
`Inventory.add_item`. The call returns a report with the number of rows added and,
for each rejected row, its line number and a human-readable reason.

## Scope

- In scope: parsing CSV text with source line numbers, importing each row on its
  own, building the report, and unit tests.
- Out of scope (from `requirements.md`): file upload, HTTP endpoints, persistence.
  Also out of scope: changing `Inventory` or `Item`. `Inventory.add_item` stays
  the only way rows get in.

## Source and constraints

- Requirement: `requirements.md` (items 1 to 5).
- Current code: `inventory.py`. `Item(sku: str, name: str, quantity: int)` is a
  frozen dataclass. `Inventory.add_item` raises `KeyError(f"duplicate sku: {sku}")`
  for a SKU that already exists and `ValueError("quantity must be positive")` when
  quantity is 0 or less. It does no other checks.
- Existing tests: `test_inventory.py` (stdlib `unittest`, 2 tests). Run with
  `python3 -m unittest -v` from the project root; this passes today (2 tests, OK).
- Project-wide constraints, copied from the requirement:
  - "Quantity must be a positive whole number. SKUs stay unique."
  - "Python 3.9 standard library only; no new dependencies."
  - "one bad row must not stop the remaining rows."
- The project is not a Git repository and has no build or lint configuration.

## Decisions taken in this plan (please confirm)

The requirement does not settle these. Each one is a choice I made; changing it
changes the tests named below.

- **D1 Header problems are reported, not raised.** If the text is empty, or line 1
  is not exactly `sku,name,quantity` (after trimming spaces around each field),
  `import_csv` adds nothing and returns `added=0` with a single rejection on line 1:
  `"expected header sku,name,quantity"`. The alternative would be to raise
  `ValueError`.
- **D2 Blank lines are skipped silently.** They are not counted and not reported.
  Line numbers still count them.
- **D3 Fields are trimmed.** Spaces around each field are removed before checks, so
  ` A-1 ` becomes `A-1`.
- **D4 SKU and name are required.** A blank SKU or name after trimming is rejected.
  `Item` does not check this today, so this rule is new. It is added in the
  importer only.
- **D5 Line numbers are physical lines in the pasted text, counted from 1.** The
  header is line 1. A row with a quoted field that spans several lines is reported
  at the line where it starts.
- **D6 Rejections are listed in input order.** When one row has several problems,
  only the first failed check is reported, in this order: field count, SKU, name,
  quantity, then `add_item`.

## Review focus

Inputs the requirement implies but nothing tests yet. Each has a test in the task
that owns it.

1. **Duplicate SKU inside the same paste.** The first row is added and the second
   is rejected with reason `duplicate sku: A-1`. Rows after it still import.
   Test: `test_duplicate_sku_within_paste` (Task 2).
2. **Quantity that `int()` would accept but is not a plain whole number**, such as
   `+3`, ` 1_000`, `3.0`, `1e3`, `-2`, `0`, or a Unicode digit like `٣`. All are
   rejected with `quantity must be a positive whole number`. Test:
   `test_quantity_rules` (Task 2).
3. **SKU that already exists in the inventory** before the import. Rejected with
   `duplicate sku: <sku>`, and the existing item is left as it was. Test:
   `test_existing_sku_rejected` (Task 2).
4. **Wrong number of fields**, such as `A-1,Bolt` or `A-1,Bolt,3,extra`. Rejected
   with `expected 3 fields, got N`, and later rows still import. Test:
   `test_wrong_field_count` (Task 2).
5. **Line numbers after blank lines, CRLF line endings, and multi-line quoted
   fields.** Reported line numbers match what the user sees in the pasted text.
   Test: `test_line_numbers` (Task 1).

## Files and responsibilities

| File | Change | Responsibility |
|---|---|---|
| `csv_import.py` | new | Parse CSV text into numbered rows, check each row, call `Inventory.add_item`, build the report |
| `test_csv_import.py` | new | `unittest` tests for parsing and import |
| `inventory.py` | none | Existing `Item` and `Inventory.add_item` |
| `test_inventory.py` | none | Existing regression suite |

## Tasks

### Task 1: Parse CSV text into numbered rows

Objective: turn pasted text into rows that keep their starting line number
(requirement 1).

Files: `csv_import.py` (new), `test_csv_import.py` (new).
Prerequisites: none.

Interfaces produced:

```python
@dataclass(frozen=True)
class SourceRow:
    line: int               # 1-based physical line where the record starts
    fields: Tuple[str, ...] # raw fields as csv.reader returns them, not trimmed

def parse_rows(text: str) -> List[SourceRow]
```

Use `typing.List` and `typing.Tuple` for annotations so the module runs on
Python 3.9.

- [ ] Read with `csv.reader(io.StringIO(text, newline=""))`. A record starts at
      the previous record's `reader.line_num + 1`; the first record starts at 1.
      This was checked against `csv` with CRLF, a blank line, and a quoted field
      that spans two lines.
- [ ] Return every record, including the header row. Leave out blank lines
      (`csv.reader` yields `[]` for them) (D2).
- [ ] Do not trim fields here. Trimming happens in Task 2.
- [ ] Add `test_line_numbers` to `test_csv_import.py`. For the text
      `"sku,name,quantity\r\nA-1,Bolt,3\n\nB-2,\"Multi\nline\",4\nC-3,Nut,2"`,
      assert that `[r.line for r in parse_rows(text)] == [1, 2, 4, 6]` and that
      the row on line 4 has fields `("B-2", "Multi\nline", "4")`.
- [ ] Add `test_empty_text`: `parse_rows("") == []`.

Acceptance: line numbers match the physical lines in the text, blank lines are
skipped, and quoted commas and newlines stay inside a field.

Verify: `python3 -m unittest test_csv_import -v` shows both tests passing.

### Task 2: Import rows and return the report

Objective: import each valid row through `Inventory.add_item`, keep going after a
bad row, and report the results (requirements 2, 3, 4).

Files: `csv_import.py`, `test_csv_import.py`.
Prerequisites: Task 1.

Interfaces consumed: `parse_rows(text) -> List[SourceRow]` from Task 1;
`Item` and `Inventory.add_item` from `inventory.py`.

Interfaces produced:

```python
EXPECTED_HEADER = ("sku", "name", "quantity")

@dataclass(frozen=True)
class Rejection:
    line: int
    reason: str

@dataclass(frozen=True)
class ImportReport:
    added: int
    rejected: Tuple[Rejection, ...]

def import_csv(inventory: Inventory, text: str) -> ImportReport
```

Reason strings (exact values; tests assert them):

| Case | Reason |
|---|---|
| Empty text, or first row is not the header (D1) | `expected header sku,name,quantity` (line 1) |
| Wrong number of fields | `expected 3 fields, got N` |
| Blank SKU after trimming (D4) | `sku is required` |
| Blank name after trimming (D4) | `name is required` |
| Quantity is not a positive whole number | `quantity must be a positive whole number` |
| `add_item` raises `KeyError` | the error's message, `duplicate sku: <sku>` |

Steps:

- [ ] Compare the first row's trimmed fields with `EXPECTED_HEADER`. If they do
      not match, or there are no rows, return
      `ImportReport(0, (Rejection(1, "expected header sku,name,quantity"),))`
      without calling `add_item` (D1).
- [ ] For each later row, check in the D6 order. Treat quantity as valid only when
      the trimmed text matches `re.fullmatch(r"[0-9]+", q)` and `int(q) > 0`. Do
      not use plain `int()` or `str.isdigit()`, because they accept `+3`, `1_000`,
      and Unicode digits.
- [ ] Call `inventory.add_item(Item(sku, name, quantity))`. On `KeyError`, record
      a rejection with `err.args[0]`. Do not use `str(err)`, because it adds
      quotes. Catch only `KeyError` and `ValueError`. Other exceptions are bugs
      and should be raised.
- [ ] Count added rows. Return rejections as a tuple in input order.
- [ ] Add these tests to `test_csv_import.py`:
  - `test_imports_valid_rows`: header plus `A-1,Bolt,3` and `B-2,Nut,5` gives
    `added == 2`, `rejected == ()`, and `inventory.get("B-2").quantity == 5`.
  - `test_bad_row_does_not_stop_import`: rows `A-1,Bolt,3`, `B-2,Nut,abc`,
    `C-3,Washer,1` give `added == 2` and
    `rejected == (Rejection(3, "quantity must be a positive whole number"),)`,
    and `C-3` is in the inventory.
  - `test_quantity_rules`: each of `0`, `-2`, `+3`, `3.0`, `1e3`, `1_000`, `٣`,
    and an empty value is rejected with
    `quantity must be a positive whole number`; ` 7 ` is accepted as 7.
  - `test_duplicate_sku_within_paste`: `A-1,Bolt,3` then `A-1,Nut,1` gives
    `added == 1`, `rejected == (Rejection(3, "duplicate sku: A-1"),)`, and
    `inventory.get("A-1").name == "Bolt"`.
  - `test_existing_sku_rejected`: the inventory already holds `A-1`; importing
    `A-1,Other,2` gives `added == 0`, the rejection reason is
    `duplicate sku: A-1`, and the stored item keeps its original name.
  - `test_wrong_field_count`: `A-1,Bolt` is rejected with
    `expected 3 fields, got 2` and `B-2,Nut,1,x` with `expected 3 fields, got 4`;
    a valid row after them is still added.
  - `test_blank_sku_and_name`: `,Bolt,3` gives `sku is required` and `A-1, ,3`
    gives `name is required`.
  - `test_header_required`: an empty string and text starting with
    `name,sku,quantity` each give `added == 0` and a single rejection
    `Rejection(1, "expected header sku,name,quantity")`, and the inventory stays
    empty.
  - `test_header_with_spaces_accepted`: header ` sku , name , quantity ` is
    accepted (D3).

Acceptance: every valid row is added through `add_item`; every rejected row
appears once with its starting line number and the exact reason above; a bad row
never stops later rows; the existing tests still pass.

Verify: `python3 -m unittest -v` from the project root runs the 2 existing tests
and all new tests, and the output ends with `OK`.

## Requirement map

| Requirement | Task | Checks |
|---|---|---|
| 1. Parse rows with source line numbers | Task 1 | `test_line_numbers`, `test_empty_text` |
| 2. Import through `add_item`; one bad row does not stop the rest | Task 2 | `test_imports_valid_rows`, `test_bad_row_does_not_stop_import`, `test_wrong_field_count` |
| 3. Report added count and line plus reason per rejection | Task 2 | Every Task 2 test asserts `added` and exact `Rejection` values |
| 4. Positive whole quantity; unique SKUs | Task 2 | `test_quantity_rules`, `test_duplicate_sku_within_paste`, `test_existing_sku_rejected` |
| 5. Python 3.9 stdlib only | Tasks 1 and 2 | Only `csv`, `io`, `re`, `dataclasses`, `typing` imported; see risk R1 |

## Risks

- **R1 Python 3.9 compatibility cannot be checked here.** The local interpreter is
  Python 3.15.0, and no `python3.9` is installed. Mitigation: use `typing.List`
  and `typing.Tuple`, no `match` statements, no `X | Y` type unions, and no
  `dataclass(slots=True)` or `kw_only`. An implementer with a 3.9 interpreter
  should run the suite with it. Until then, 3.9 support is unverified.
- **R2 The reason for duplicates depends on the text of `add_item`'s `KeyError`.**
  If `inventory.py` changes that message, `test_duplicate_sku_within_paste` and
  `test_existing_sku_rejected` fail. That failure is intended.
- **R3 Large pastes.** The whole text is held in memory. No size limit is stated,
  and none is added.

## Verification strategy

1. After Task 1: `python3 -m unittest test_csv_import -v`; both tests pass.
2. After Task 2: `python3 -m unittest -v`; the 2 existing tests and all new tests
   pass, and the output ends with `OK`.
3. Check imports: `grep -n "^import\|^from" csv_import.py` lists only stdlib
   modules and `inventory`.
4. Where available, repeat step 2 with a Python 3.9 interpreter (R1).

## Open decisions

D1 to D6 above are working decisions. D1 (whether a header problem is reported or
raised) and D4 (whether blank SKU and name are rejected) matter most. Confirm them
before implementation.
