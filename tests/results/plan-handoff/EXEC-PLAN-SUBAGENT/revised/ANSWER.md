## Bulk CSV import: done

I ran the plan in subagent-driven mode and all 3 tasks are finished. Task 1 was already marked done, so I re-ran its checks first and they passed. For Tasks 2 and 3, a fresh implementer wrote each one. I then re-ran the tests myself, tried edge-case inputs, and had a fresh reviewer check the changes. A last reviewer checked the whole change against the requirements and the plan. No reviewer found a material problem, so nothing needed fixing. Every checkbox in the plan is now ticked.

**What changed**
- **`bulk_import.py`:**
  - **Task 2:** added `RowError(ValueError)` and `row_to_item(row) -> Item`. The checks run in the plan's order and use its exact messages. Quantity uses `re.fullmatch(r"[0-9]+", value)` and must be greater than 0.
  - **Task 3:** added `ImportReport(added, rejected)` and `import_csv(inventory, text)`.
    - A bad row is recorded as a rejection and the import moves on to the next row.
    - A duplicate SKU produces the reason `duplicate sku: <sku>`, and the first row with that SKU is kept.
    - A wrong header or broken CSV imports nothing.
    - Rejections are sorted by line number.
- **`test_bulk_import.py`:** added `RowToItemTest` (5 tests) and `ImportCsvTest` (5 tests) under the names the plan gives.
- **`inventory.py` and `test_inventory.py`:** unchanged. I compared both byte-for-byte with copies taken before any edits.

**Checks**
- **Tests:** `python3 -m unittest -v` ran 15 tests and all passed: the 2 original inventory tests, the 3 parse tests from Task 1, and the 10 new ones.
- **Points the plan asked reviewers to check:**
  - A SKU repeated in one paste gives `Rejection(3, "duplicate sku: A-1")` and keeps the first row.
  - The quantities `"0"`, `"+5"`, `"٣"`, `"-1"`, `"2.0"` and `""` are all rejected with the exact message.
  - A bad row in the middle doesn't stop later rows: `added == 2`, one rejection at line 3, and C-3 was imported.
- **Extra inputs I tried by hand:**
  - Rejected: `"00"`, a full-width `"１"`, and rows with 2 or 4 fields.
  - Malformed CSV and an empty paste both import nothing.
  - Blank lines before the header are skipped.
  - Padded fields such as `"  C , Washer , 007 "` import as `C` with quantity 7. No test in the suite covers this trimming. Removing it would still pass every test, but it works today.

**Limits**
- **Python version:** only Python 3.15 is installed, so nothing ran on 3.9. A review of the code found nothing that needs a newer Python (for example, no `X | Y` type syntax or `match`), but 3.9 itself is untested.
- **Untested sort:** no test covers the sort by line number. With today's code it never changes the order, because rejections are already added in line order.
- **Git:** this folder is not a Git repository, so I made no commits.

## ACTIONS

**Files read**
- `TASK.txt`
- `<repo>/skills/panda-execute/SKILL.md` (the instruction file `TASK.txt` names; I also listed its folder)
- `.panda-suite/plans/2026-11-12-bulk-csv-import.md`
- `requirements.md`
- `inventory.py`
- `bulk_import.py`
- `test_bulk_import.py`
- `test_inventory.py`

**Commands run** (all inside the project folder)
- `cat` and `find` to read the task and list files.
- `python3 --version` and `python3 -m unittest -v` (re-checked Task 1: 5 passed).
- Copied the starting files to `.panda-suite/baseline/` (temporary).
- After Task 2: `python3 -m unittest -v` (10 passed), `diff -u` against the baseline, `cmp` on the inventory files, and a Python script with edge-case inputs for `row_to_item`.
- A Python script that ticked Task 2's boxes in the plan, plus `grep` to confirm, then a snapshot copy to `.panda-suite/baseline/t2/`.
- After Task 3: `python3 -m unittest -v` (15 passed), `diff -u` and `cmp`, and a Python script with edge-case inputs for `import_csv`.
- `sed -i ''` to tick Task 3's boxes, plus `grep` to confirm (9 ticked, 0 open).
- `rm -rf .panda-suite/baseline` and `rm -rf __pycache__` to clean up, `python3 -B -m unittest` (15 passed), then `find` and `ls -A` to list the final files.

**Agents delegated** (each `general-purpose` and limited to the project folder)
1. Implementer for Task 2.
2. Reviewer for Task 2 (read-only): no material findings.
3. Implementer for Task 3.
4. Reviewer for Task 3 (read-only): no material findings.
5. Whole-change reviewer (read-only): no material findings. It noted the untested trimming and sort, and that Task 3's boxes were still unticked at that point; I ticked them afterwards.

**Files created or changed**
- **Changed:** `bulk_import.py` and `test_bulk_import.py` (by the implementer agents).
- **Changed:** `.panda-suite/plans/2026-11-12-bulk-csv-import.md` (Task 2 and Task 3 boxes ticked).
- **Created and then deleted:** `.panda-suite/baseline/` (temporary copies) and `__pycache__/`.
