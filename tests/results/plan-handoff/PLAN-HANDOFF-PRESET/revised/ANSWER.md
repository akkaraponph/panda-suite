## Answer to the user

I've saved the plan at `.panda-suite/plans/2026-11-12-bulk-csv-import.md`. Nothing has been implemented. The only change to your project is the new plan file.

**What it covers:** two tasks, both in a new `csv_import.py` with tests in a new `test_csv_import.py`. `inventory.py` stays unchanged.

1. **Parse the CSV.** `parse_csv(text) -> List[CsvRow]` checks the header and keeps each row's line number in the original text. That number is the line where the row starts, so a quoted field that spans several lines doesn't throw off later rows. I checked how Python's `csv` module counts lines before choosing this approach.
2. **Import the rows.** `import_csv(inventory, text) -> ImportReport(added, rejected)` checks each row and adds the valid ones through `Inventory.add_item`. A bad row doesn't stop the rest, and each rejected row gets its line number and a fixed reason message.

The plan spells out each function's inputs and outputs. That way the subagent building Task 2 can work from the plan alone, without needing to see Task 1's code.

**Please check these choices.** `requirements.md` doesn't settle them, so I made a call on each:
- **Bad header:** a wrong or missing header, or empty input, raises `CsvImportError` and nothing is imported. It is not reported as a rejected row.
- **Blank SKU or name:** rows with these are rejected. The requirements don't mention this case.
- **Quantity:** after trimming spaces it must be digits only and at least 1, so `007` is accepted as 7. It is checked against a pattern rather than relying on `int()` alone, because `int()` also accepts values like `1_0` and `+3`.
- **Repeated SKUs:** if the same SKU appears twice in one paste, the first is added and the later one is rejected as `duplicate sku: <sku>`. Rows already added stay added (nothing is rolled back).
- **Malformed CSV:** if Python's `csv` module raises an error, for example on a NUL character, nothing is imported. If you'd rather keep the rows before that point, decide that before Task 1 starts.

**Open check:** Python 3.9 compatibility can't be tested here, because the only interpreter on this machine is Python 3.15. The plan has the reviewer read the code for newer syntax, or run `python3.9 -m unittest -v` if a 3.9 interpreter is available.

**Verification:** each task ends with `python3 -m unittest -v`. When both are done, all 19 tests should pass (the 2 existing ones plus 17 new). The folder isn't a Git repository, so I didn't add a `.gitignore` rule.

**Next step:** you've already chosen subagent-driven execution. Each task gets a fresh agent to build it and a fresh reviewer to check it, then the whole change is reviewed once at the end. Please review the plan, especially the choices above. When you're happy with it, use this request:

> Use panda-execute (subagent-driven) to implement `.panda-suite/plans/2026-11-12-bulk-csv-import.md`.

Do you approve the plan as written, or should any of those choices change first?

## ACTIONS

- **Read:** `TASK.txt`, `requirements.md`, `inventory.py`, `test_inventory.py`, `<repo>/skills/panda-plan/SKILL.md` (via `cat`)
- **Commands run:**
  - `ls -la` (listed the project folder)
  - `git rev-parse --show-toplevel` (result: not a Git repository)
  - `python3 --version` (Python 3.15.0)
  - `python3 -m unittest -v` (the 2 existing tests pass)
  - `date +%F`
  - `python3 -I -c ...` (checked how the `csv` module counts lines and what `int()` accepts)
  - `mkdir -p .panda-suite/plans`
- **Created:** `<workspace-root>/PLAN-HANDOFF-PRESET-new/.panda-suite/plans/2026-11-12-bulk-csv-import.md`
- **Changed:** none
