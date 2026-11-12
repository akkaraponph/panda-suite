# Bulk CSV Import: Implementation Plan

**Goal:** import pasted CSV rows through `Inventory.add_item` and report
rejected rows with line numbers (`requirements.md`).

**Constraints:** Python 3.9 standard library only; `inventory.py` and
`test_inventory.py` stay unchanged. Run tests with `python3 -m unittest -v`.

**Decisions:** blank lines are skipped; fields are stripped; a wrong header or
malformed CSV rejects the whole paste (nothing imported); quantity must match
`[0-9]+` and be greater than 0; the first occurrence of a SKU wins.

## Review focus

1. Duplicate SKU inside one paste: first row added, later row rejected
   (Task 3 `test_duplicate_within_paste`).
2. Quantities `int()` accepts but are not plain positive digits: `"0"`, `"+5"`,
   `"٣"` (Task 2 `test_quantity_rejections`).
3. A bad row in the middle does not stop later rows
   (Task 3 `test_bad_row_does_not_stop_later_rows`).

## Task 1: Parse CSV text into numbered rows

**Files:** `bulk_import.py`, `test_bulk_import.py`.
**Produces:** `Rejection(line: int, reason: str)`, `CsvRow(line: int, fields: Tuple[str, ...])`,
`ParsedCsv(rows, rejected)`, `HEADER`, `HEADER_REASON`, `parse_csv(text: str) -> ParsedCsv`.

- [x] Tests in `ParseCsvTest`: `test_rows_keep_line_numbers`, `test_wrong_header`,
  `test_malformed_csv_rejects_whole_paste`.
- [x] Implement `parse_csv` with `csv.reader(io.StringIO(text), strict=True)`.
- [x] Verify: `python3 -m unittest -v` passes.

## Task 2: Validate one row into an `Item`

**Files:** `bulk_import.py`, `test_bulk_import.py`.
**Consumes:** `CsvRow` from Task 1.
**Produces:** `class RowError(ValueError)` and `row_to_item(row: CsvRow) -> Item`.
Checks run in this order and the first failure raises `RowError` with exactly:

| Check | Reason |
| --- | --- |
| `len(fields) != 3` | `f"expected 3 fields, got {n}"` |
| empty sku | `"sku is required"` |
| empty name | `"name is required"` |
| quantity not `[0-9]+` or not > 0 | `f"quantity must be a positive whole number, got {value!r}"` |

- [ ] Tests in `RowToItemTest`: `test_valid_row` (`CsvRow(2, ("A-1", "Bolt", "007"))`
  → `Item("A-1", "Bolt", 7)`), `test_wrong_field_count` (2 fields → `"expected 3 fields, got 2"`),
  `test_empty_sku`, `test_empty_name`, `test_quantity_rejections` (subTest over
  `"0"`, `"-1"`, `"+5"`, `"2.0"`, `""`, `"٣"`).
- [ ] Implement `RowError` and `row_to_item` in `bulk_import.py` using
  `re.fullmatch(r"[0-9]+", value)`.
- [ ] Verify: `python3 -m unittest -v` passes.

## Task 3: Import rows and report

**Files:** `bulk_import.py`, `test_bulk_import.py`.
**Consumes:** `parse_csv`, `row_to_item`, `RowError`, `Inventory.add_item`.
**Produces:** `ImportReport(added: int, rejected: Tuple[Rejection, ...])` and
`import_csv(inventory: Inventory, text: str) -> ImportReport`.
`RowError` → `Rejection(row.line, str(err))`; `KeyError` from `add_item` →
`Rejection(row.line, f"duplicate sku: {item.sku}")` (build the string; do not use
`str(KeyError)`). Rejections are sorted by line.

- [ ] Tests in `ImportCsvTest`: `test_all_valid`, `test_bad_row_does_not_stop_later_rows`
  (`"sku,name,quantity\nA-1,Bolt,3\nB-2,Nut,0\nC-3,Washer,4\n"` → `added == 2`,
  one rejection at line 3), `test_duplicate_within_paste` (→ `Rejection(3, "duplicate sku: A-1")`),
  `test_duplicate_of_existing_item`, `test_bad_header_imports_nothing`.
- [ ] Implement `ImportReport` and `import_csv`.
- [ ] Verify: `python3 -m unittest -v` passes with the 2 original tests and all new tests.
