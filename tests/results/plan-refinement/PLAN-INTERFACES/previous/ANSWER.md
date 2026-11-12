I've saved the implementation plan to `.panda-suite/plans/2026-11-12-bulk-csv-import.md`. It is written for an engineer who hasn't seen this conversation. I didn't change any source or test files. The existing suite still passes (2 tests); the new tests are only planned, not written.

**What the plan does:** It adds a new `csv_import.py` next to `inventory.py`. Every row goes through the existing `Inventory.add_item`, and `inventory.py` itself stays unchanged.
- `parse_csv(text)` checks the header and returns each data row with the line number it starts on.
- `import_csv(inventory, text)` checks each row, adds the valid ones and returns a report: how many rows were added, plus a line number and reason for each rejected row.
- A bad row is recorded in the report and the import moves on to the next row.
- Duplicate SKUs and invalid quantities come back as rejected rows rather than exceptions.

There are three ordered tasks:
1. Parse the text and track line numbers, with tests.
2. Check each row and import it, with tests.
3. Run the full suite and check Python 3.9 compatibility.

Every requirement maps to a task and a check.

**Things I checked that shaped the plan:**
- **Line numbers:** Python's CSV reader reports the line a record *ends* on, so a name containing a line break would be reported one line late. The plan tracks the line each row starts on instead.
- **Quantity:** `int()` accepts `"+3"`, `"1_000"` and non-ASCII digits. So the plan only accepts plain digits 0–9 with a value above 0. `"007"` is accepted as 7.
- **Duplicates:** `add_item` signals a duplicate with a `KeyError`, which adds extra quotes when turned into text. The importer writes its own message instead (`duplicate sku: A-1`).
- **Testing the broken-CSV case:** lowering the CSV field size limit reliably triggers a CSV parse error (`csv.Error`), so that case can be tested.

**Choices I made where the requirements were silent.** Each one is written down in the plan and backed by a test, so any of them can be changed:
- A missing or wrong header raises `ValueError` before anything is added, so the inventory is unchanged.
- Blank lines are skipped and don't appear in the report.
- Spaces around values are trimmed, and a row with an empty SKU or name is rejected.
- A row with more or fewer than 3 fields is rejected.
- If a SKU appears twice in the paste, the first row is added and the second is rejected.
- There is no rollback: rows added before a bad row stay added.

**Still open:**
- **Badly broken CSV:** in the plan, a CSV parse error stops reading at that point, because the reader can't be resumed safely. The remaining rows are not imported, which goes against "one bad row must not stop the rest" for that one case. Whoever owns the requirements should either accept this or ask for the whole paste to be rejected up front.
- **Python 3.9:** only Python 3.15 is installed here. The plan lists what to avoid for 3.9, but the 3.9 run must be reported as not run unless an engineer has a 3.9 interpreter.

The workspace isn't a Git repository, so I didn't update `.gitignore`.

To implement it, say: "Use panda-execute to implement `.panda-suite/plans/2026-11-12-bulk-csv-import.md`." Saving the plan doesn't authorize implementation by itself.

---

## ACTIONS

**Files read**
- `<workspace-root>/PLAN-INTERFACES-old/TASK.txt`
- `<workspace-root>/old-skill/panda-plan/SKILL.md` (named in TASK.txt)
- `.../PLAN-INTERFACES-old/requirements.md`
- `.../PLAN-INTERFACES-old/inventory.py`
- `.../PLAN-INTERFACES-old/test_inventory.py`

**Commands run** (in the project root)
- `cat TASK.txt`, `find . -type f`; `cat` of the skill file and project files; `ls -R` of the `old-skill/panda-plan` folder (it contains only `SKILL.md`)
- `git rev-parse --show-toplevel`: not a Git repository
- `ls -la`, `python3 --version` (3.15.0), `python3 -m unittest -v` (2 tests, OK), `date +%F`
- `python3 -c` checks of how `int()` parses `'1_000'`, `' +3 '` and `'٣'`; of CSV reader line numbers on a row with a line break and a blank line; and of `csv.field_size_limit` triggering a CSV parse error
- `which python3.9` (not found)
- `mkdir -p .panda-suite/plans`
- Two inline `python3` scripts that edited the plan file, then `grep` to check it was consistent

**Files created**
- `<workspace-root>/PLAN-INTERFACES-old/.panda-suite/plans/2026-11-12-bulk-csv-import.md`

No source, test or other files were changed.
