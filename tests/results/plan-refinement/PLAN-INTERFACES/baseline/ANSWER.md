I wrote the implementation plan to `<workspace-root>/PLAN-INTERFACES-baseline/PLAN.md`. No code was implemented; the existing 2 tests still pass.

**How the plan is built:**
- **Location:** a new module `inventory_import.py` and a new test file `test_inventory_import.py`. `inventory.py` is not changed.
- **Interface:** it names exactly what to create: `parse_rows(text) -> List[SourceRow]`, `validate_row(row) -> Union[Item, RejectedRow]`, `import_csv(inventory, text) -> ImportReport`, an `ImportFormatError(ValueError)`, and frozen dataclasses for `SourceRow`, `RejectedRow` and `ImportReport`. The rejection messages are fixed strings so tests and staff see the same text.
- **Tasks:** four, in order:
  1. Parse the CSV text into rows that keep their line numbers.
  2. Check each row (field count, required SKU and name, quantity).
  3. Import valid rows through `Inventory.add_item`, catching only `KeyError` (duplicate SKU) and `ValueError`, and build the report.
  4. Final check, including a Python 3.9 compatibility check.
- **Each task** lists its files, implementation notes, specific test cases, and a "done when" check (`python3 -m unittest -v` passes). The plan ends with a short list of risks.

**Decisions I made where the requirements are silent** (each is written into the plan so a reviewer can change it):
- **Line numbers:** counted from 1, with the header as line 1. A quoted field that spans several lines is reported at the line where its row starts.
- **Bad input as a whole:** an empty input, a wrong header or malformed CSV raises `ImportFormatError` and imports nothing. It is not reported as a rejected row.
- **Blank lines and spaces:** blank lines are skipped. Spaces around fields are removed, and an empty SKU or name rejects the row.
- **Quantity:** it must be plain ASCII digits (`[0-9]+`) and greater than 0. The plan warns against bare `int()`, which accepts `"+3"`, `" 3"`, `"1_000"` and Arabic-Indic digits. I ran a check to confirm this.
- **Duplicate SKUs:** a SKU that is already in the inventory, or repeated in the same paste, is rejected; the first occurrence wins. Valid rows are added even when others are rejected, with no rollback.

**Checked here:** I ran a check confirming that the line-tracking method in Task 1 reports the right line numbers for quoted fields that span lines, blank lines and `\r\n` line endings.

**Python version:** the local interpreter is 3.15, not 3.9. The plan tells the engineer not to use features newer than 3.9 and to run the tests on 3.9 if it is available.

ACTIONS
- Files read: `TASK.txt`, `requirements.md`, `inventory.py`, `test_inventory.py` (all in `<workspace-root>/PLAN-INTERFACES-baseline/`)
- Commands run (in that directory):
  - `cat TASK.txt` and `find . -type f`
  - `cat -n requirements.md inventory.py test_inventory.py`
  - `python3 --version`, `python3 -m unittest -v` (2 tests, OK) and `ls -a`
  - a `python3 -c` check of the csv line tracking and `int()` behaviour; it created no files
- Files created: `<workspace-root>/PLAN-INTERFACES-baseline/PLAN.md`
- Files changed: none
