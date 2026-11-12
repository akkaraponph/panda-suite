I finished Tasks 2 and 3 of the bulk CSV import plan. Task 1 had already been done, and I checked it before building on it. The full test suite passes (`python3 -m unittest -v`, 16 tests). This machine only has Python 3.15, so I couldn't run the tests on Python 3.9. The code uses nothing newer than 3.9.

**Task 1 (already done): verified, with one fix.** Its 3 tests passed. One thing didn't match the plan: it says blank lines are skipped, but a line containing only spaces came through as a row and would have been rejected with "expected 3 fields, got 1". I changed `parse_csv` so a line that is empty after trimming is skipped, and added `test_whitespace_only_line_is_blank`. A line like `,,` still counts as a row and is rejected with "sku is required". This is my reading of "blank lines" for a change marked done, so revert it if you meant only truly empty lines.

**Task 2: verified.**
- Added `RowError` and `row_to_item`. They run the four checks in the plan's order with its exact error messages.
- Quantity must match `[0-9]+` and be greater than 0, so `"0"`, `"-1"`, `"+5"`, `"2.0"`, `""` and `"٣"` are all rejected, and `"007"` becomes 7.
- Added the 5 `RowToItemTest` tests.
- To check that the tests catch the Arabic-digit case, I ran a copy that used `value.isdigit()` instead. One test failed as expected, and I deleted the copy.

**Task 3: verified.**
- Added `ImportReport` and `import_csv`. Duplicate SKUs are reported as "duplicate sku: X", and rejections come back sorted by line number.
- Added the 5 `ImportCsvTest` tests. They also check what ends up in the inventory, not only the report.

All three review-focus points are covered by tests:
- **Duplicate in one paste:** the first row is kept and the later one becomes `Rejection(3, "duplicate sku: A-1")`.
- **Odd quantities:** `"0"`, `"+5"` and `"٣"` are rejected.
- **Bad row in the middle:** later rows still import (`added == 2`, one rejection at line 3).

I also checked a few cases by hand. Malformed CSV imports nothing and gives one "malformed CSV: …" rejection. Rows with missing fields, a missing SKU, a zero quantity and a duplicate are each reported on the right line. Spaces around fields are trimmed.

`inventory.py` and `test_inventory.py` are unchanged, and nothing new is needed beyond the standard library. All plan checkboxes are ticked. This folder isn't a git repository, so nothing was committed.

## ACTIONS

**Files read**
- `TASK.txt`
- `<previous>/panda-execute/SKILL.md` (the instruction file TASK.txt names)
- `.panda-suite/plans/2026-11-12-bulk-csv-import.md`
- `requirements.md`
- `inventory.py`
- `bulk_import.py`
- `test_inventory.py`
- `test_bulk_import.py`

**Commands run** (in the project directory)
- `cat TASK.txt`, `find . -type f`, `git status` (not a git repository)
- `cat`/`ls -R` on the panda-execute skill folder
- `python3 --version` (3.15.0) and `python3 -m unittest -v`: 5 tests passed at the start
- Inline Python checks of `parse_csv` and `import_csv` edge cases
- Python scripts that edited `bulk_import.py` and `test_bulk_import.py`
- `python3 -m unittest -v`: 15 passed after Tasks 2–3, then 16 passed after the blank-line fix
- Test-strength check: copied the `.py` files to the sibling folder `../exec-mut`, swapped the regex for `isdigit()` with `sed`, ran the tests (1 failure, as expected), then `rm -rf ../exec-mut`
- `ls`/`which python3.9` (not installed)
- `sed` to tick the plan checkboxes, then `grep` to confirm 9 ticked and 0 unticked

**Files changed**
- `bulk_import.py`: added the `re` and `inventory` imports, `RowError`, `row_to_item`, `ImportReport` and `import_csv`; `parse_csv` now skips whitespace-only lines
- `test_bulk_import.py`: added the `RowToItemTest` and `ImportCsvTest` classes, `ParseCsvTest.test_whitespace_only_line_is_blank`, and the new imports
- `.panda-suite/plans/2026-11-12-bulk-csv-import.md`: ticked the Task 2 and Task 3 checkboxes

**Files created:** none in the project. The temporary `../exec-mut` copy was deleted.
