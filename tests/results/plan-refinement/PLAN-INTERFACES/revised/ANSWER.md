I've written a three-task implementation plan for the bulk CSV import. It's saved at `<workspace-root>/PLAN-INTERFACES-new/.panda-suite/plans/2026-11-12-bulk-csv-import.md`. No source or test files were changed.

**How the plan is built:**
- **New files:** `bulk_import.py` and `test_bulk_import.py`. `inventory.py` and `test_inventory.py` stay as they are.
- **Exact interfaces:** the plan gives every name and signature in full so each task can be done without this conversation:
  - `Rejection(line, reason)`, `CsvRow(line, fields)`, `ParsedCsv(rows, rejected)`, `ImportReport(added, rejected)`
  - `RowError(ValueError)`, `HEADER`, `HEADER_REASON`
  - `parse_csv(text) -> ParsedCsv`, `row_to_item(row) -> Item`, `import_csv(inventory, text) -> ImportReport`
- **Task 1, parsing:** turns the pasted text into rows that keep their line numbers. A wrong header or broken CSV becomes a rejection in the report instead of an error.
- **Task 2, checking one row:** converts a row into an `Item`, or rejects it with a fixed reason. The reasons cover the wrong number of fields, an empty SKU, an empty name, and a quantity that isn't a positive whole number.
- **Task 3, importing:** adds rows through the existing `Inventory.add_item` and keeps going after a bad row. It builds the report with rejections in line order and turns a duplicate-SKU error into `duplicate sku: <sku>`.
- **Tests:** each task names its tests and the exact expected values. The plan also maps each of the five requirements to a task, and lists risks and a review focus.

**Things I checked in this workspace before writing it:**
- The 2 existing tests pass with `python3 -m unittest -v`.
- Python's `csv` module needs `strict=True` to report an unclosed quote. Without it, the rest of the text silently becomes one field.
- Python's `int()` accepts non-English digits such as `"٣"`. The plan therefore requires the quantity to be plain digits 0–9.

**Decisions I made where the requirements were silent (please confirm or change them in the plan before anyone starts):**
1. **Empty name:** the plan rejects a row with an empty name.
2. **Broken CSV quote:** parsing stops at that line and reports it, so later rows aren't imported. This is the one case where a bad row stops the rest.
3. **Wrong or missing header:** the whole paste is rejected and nothing is imported.
4. **The report:** it gives only the number of rows added, not which SKUs were added.

**Limits:**
- Python 3.9 isn't installed here (the local version is 3.15.0). The 3.9-only rule can only be checked by reading the code, and the plan includes a search for newer syntax for that.
- The workspace isn't a Git repository, so I skipped the `.gitignore` update and the `git check-ignore` check.

To build it, you can say: "Use panda-execute to implement `.panda-suite/plans/2026-11-12-bulk-csv-import.md`." The plan on its own doesn't approve starting the work.

---

## ACTIONS

**Files read:**
- `<root>/TASK.txt`
- `<root>/requirements.md`
- `<root>/inventory.py`
- `<root>/test_inventory.py`
- `<repo>/skills/panda-plan/SKILL.md` (named by TASK.txt). I also listed that `skills/panda-plan/` folder; `SKILL.md` is the only file in it.

`<root>` = `<workspace-root>/PLAN-INTERFACES-new`

**Commands run:**
1. `cat TASK.txt` and `find . -type f` in `<root>`
2. `cat` of `requirements.md`, `inventory.py`, `test_inventory.py` and `SKILL.md`; `ls -R` of the `skills/panda-plan` folder
3. In `<root>`:
   - `git rev-parse --show-toplevel`: not a Git repository
   - `date +%F`: 2026-11-12
   - `python3 --version`: 3.15.0
   - `python3 -m unittest -v`: 2 tests, OK
   - An inline Python script testing how `csv.reader` handles line numbers, blank lines, multi-line fields, unclosed quotes, CRLF line endings and NUL bytes, plus `int`/`isdigit` on non-English digits
4. `python3 -c` testing `csv.reader(strict=True)` on broken quotes (it reports both errors), then `command -v python3.9`, which found nothing. The command exited 1 only because of that `command -v`.
5. `mkdir -p <root>/.panda-suite/plans`

**Files created:**
- `<root>/.panda-suite/plans/2026-11-12-bulk-csv-import.md`
- Directory `<root>/.panda-suite/plans/`

**Files changed:** none.
