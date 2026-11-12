The plan is saved at `.panda-suite/plans/2026-11-12-bulk-csv-import.md`. No source or test files were changed.

It has two tasks, one per subagent run, and each one names the exact interfaces it uses:

1. **Parse the CSV text** (`parse_csv` in a new `bulk_import.py`). It turns the pasted text into rows that keep the line number where each row starts in the paste, and checks the header.
2. **Import and report** (`import_csv`). It checks each row, adds it through the existing `Inventory.add_item`, keeps going past bad rows, and returns a report with the number added and the line number and reason for each rejected row.

Each task lists its test names, the exact values and messages to assert, and the check command `python3 -m unittest -v`. The 2 existing tests pass with that command. Every requirement maps to a task and a test, and the plan lists five likely failure cases with their own tests, including the same SKU twice in one paste.

**Decisions to confirm before it's built.** The requirements don't cover these, so I chose defaults. They are D1–D7 in the plan; these five are the most likely to need a change:
- **D1, wrong or missing header:** the whole import stops before anything is added. The alternative is to report one rejection at line 1.
- **D2, blank lines:** they are skipped and don't appear in the report.
- **D4, blank SKU or name:** both are rejected.
- **D5, quantity:** only plain digits greater than zero are accepted, with spaces around them trimmed. Python's `int()` alone would also accept values like `+3`, `1_000` or non-ASCII digits, and the plan rejects those. Leading zeros are accepted, so `007` is stored as 7.
- **D6, report contents:** it gives the added count only, not which SKUs were added.

**Python 3.9 is not checked.** This machine only has Python 3.15 and no 3.9. The plan sticks to code that works in 3.9 and says a reviewer should check for newer syntax, but running the tests under 3.9 hasn't been done. One error-handling path only runs on 3.9 or 3.10, so it can't be tested here either.

The folder isn't a Git repository, so I didn't add a `.gitignore` entry for `.panda-suite/`.

Once you've read the plan, you can start the build with: "Use panda-execute to implement `.panda-suite/plans/2026-11-12-bulk-csv-import.md`, one task at a time with subagents." The saved plan doesn't by itself mean you've approved building it.

---

ACTIONS
- Read: `TASK.txt`, `<previous>/panda-plan/SKILL.md`, `requirements.md`, `inventory.py`, `test_inventory.py`
- Commands run: `find . -type f`; `ls -la`; `git rev-parse --show-toplevel` (result: not a git repository); `python3 --version` (3.15.0); `python3 -m unittest -v` (2 tests, OK); `date +%F`; a `python3 -I -c` check of how `csv.reader` handles line numbers, blank lines, unterminated quotes and NUL bytes, and of `int("5_000")` and `"٥".isdigit()`; `which python3.9 python3.10` (not found); `ls .panda-suite` (did not exist); `mkdir -p .panda-suite/plans`
- Created: `<workspace-root>/PLAN-HANDOFF-PRESET-prev/.panda-suite/plans/2026-11-12-bulk-csv-import.md`
- Changed: none
