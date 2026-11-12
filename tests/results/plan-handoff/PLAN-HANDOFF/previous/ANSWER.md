I've written the plan for the bulk CSV import and saved it to `.panda-suite/plans/2026-11-12-bulk-csv-import.md`. No source or test files were changed.

**The plan:**
- **Task 1:** Add `parse_rows(text) -> List[CsvRow]` in a new `csv_import.py`, using the standard `csv` module. Each row records the line where it starts. A missing or wrong header raises `CsvHeaderError`.
- **Task 2:** Add `import_csv(inventory, text) -> ImportReport(added, rejected)`. Each row is checked for field count, required `sku` and `name`, and a whole-number quantity, then added with `Inventory.add_item`. A duplicate SKU comes back from `add_item` as a `KeyError`. Bad rows go into the report with their line number and a fixed reason message, and the import carries on.
- Each task lists the tests to write, using the exact inputs and expected values. A table maps each of the five requirements to its task and tests.

I checked one detail: Python's `csv` module, with the line-tracking method in the plan, gives the right start line for rows after blank lines and after a quoted name that spans two lines.

**Decisions to confirm.** The requirements don't settle these, so the plan records them as assumptions. Change any of them before implementation if they're wrong:
1. **Header:** if the header is missing or wrong, or the text is empty, the whole import is rejected with an error and nothing is added. Any other bad row is only listed in the report.
2. **Blank lines and spaces:** blank lines are skipped and don't appear in the report. Spaces around `sku`, `name` and `quantity` are trimmed, and `sku` and `name` can't be empty.
3. **Quantity:** only plain digits greater than zero are accepted. `+3`, `3.0`, `3.5`, `0` and negative numbers are rejected.
4. **Duplicates:** if a SKU is already in the inventory or appears twice in the paste, the first one is kept and the later one is rejected.
5. **No undo:** valid rows stay added even when other rows are rejected.

**Not yet checked:**
- **Python 3.9:** only Python 3.15.0 is installed here, so the 3.9 requirement can't be tested yet. The plan lists the newer language features to avoid and asks for a test run on Python 3.9 later.
- **Broken quoting:** a quote that is opened and never closed can merge the following rows into one field without any warning. The plan accepts this as a known limitation.

The folder isn't a Git repository, so I didn't add a `.gitignore` entry for `.panda-suite/`.

When you want it built, you can say: "Use panda-execute to implement `.panda-suite/plans/2026-11-12-bulk-csv-import.md`." Saving the plan doesn't mean the implementation is approved.

---

ACTIONS
- Read: `TASK.txt`, `../prev/panda-plan/SKILL.md` (the instruction file TASK.txt names), `requirements.md`, `inventory.py`, `test_inventory.py`
- Commands run:
  - `cat` and `find` to read TASK.txt and list the project files
  - `git rev-parse --show-toplevel` (result: not a git repository)
  - `ls -la`
  - `python3 --version` (3.15.0)
  - `python3 -m unittest -v` (2 tests, OK)
  - `date +%F`
  - `mkdir -p .panda-suite/plans`
  - `python3 -I -c` with a short inline script to check how `csv.reader` numbers lines (no files written)
- Created: `.panda-suite/plans/2026-11-12-bulk-csv-import.md`
- Changed: none
