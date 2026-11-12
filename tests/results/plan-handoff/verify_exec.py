"""Grade an EXEC-PLAN-* workspace against the plan-execute fixture's plan.

Usage: python3 verify_exec.py <workspace> <fixture>
Checks exact plan names, reason strings, test names, untouched originals,
plan checkboxes, and a real unittest run. Prints one line per check.
"""

import filecmp
import importlib
import re
import subprocess
import sys
from pathlib import Path

ws, fixture = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (f" ({detail})" if detail else ""))


for f in ("inventory.py", "test_inventory.py", "requirements.md"):
    check(f"{f} unchanged", filecmp.cmp(ws / f, fixture / f, shallow=False))

run = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v"], cwd=ws,
                     capture_output=True, text=True)
m = re.search(r"Ran (\d+) tests?", run.stderr)
check("unittest passes", run.returncode == 0, m.group(0) if m else run.stderr[-200:])

tests = (ws / "test_bulk_import.py").read_text()
for t in ("test_valid_row", "test_wrong_field_count", "test_empty_sku", "test_empty_name",
          "test_quantity_rejections", "test_all_valid", "test_bad_row_does_not_stop_later_rows",
          "test_duplicate_within_paste", "test_duplicate_of_existing_item",
          "test_bad_header_imports_nothing", "class RowToItemTest", "class ImportCsvTest"):
    check(f"plan test name {t}", t in tests)

sys.path.insert(0, str(ws))
sys.dont_write_bytecode = True
b = importlib.import_module("bulk_import")
inv_mod = importlib.import_module("inventory")
for n in ("RowError", "row_to_item", "ImportReport", "import_csv"):
    check(f"plan name {n}", hasattr(b, n))
if all(hasattr(b, n) for n in ("RowError", "row_to_item", "import_csv")):
    check("RowError subclasses ValueError", issubclass(b.RowError, ValueError))
    cases = [(("A-1", "Bolt"), "expected 3 fields, got 2"), (("", "Bolt", "3"), "sku is required"),
             (("A-1", "", "3"), "name is required"),
             (("A-1", "Bolt", "+5"), "quantity must be a positive whole number, got '+5'"),
             (("A-1", "Bolt", "٣"), "quantity must be a positive whole number, got '٣'")]
    for fields, reason in cases:
        try:
            b.row_to_item(b.CsvRow(2, fields))
            got = "no error"
        except b.RowError as e:
            got = str(e)
        check(f"reason for {fields!r}", got == reason, got)
    check("valid row 007", b.row_to_item(b.CsvRow(2, ("A-1", "Bolt", "007"))) == inv_mod.Item("A-1", "Bolt", 7))
    inv = inv_mod.Inventory()
    rep = b.import_csv(inv, "sku,name,quantity\nA-1,Bolt,3\nA-1,Nut,2\nB-2,Nut,0\nC-3,Washer,4\n")
    check("import report", rep.added == 2 and [(r.line, r.reason) for r in rep.rejected] ==
          [(3, "duplicate sku: A-1"), (4, "quantity must be a positive whole number, got '0'")],
          repr(rep))

plan = (ws / ".panda-suite/plans/2026-11-12-bulk-csv-import.md").read_text()
check("all plan boxes checked", "- [ ]" not in plan, f"{plan.count('- [ ]')} unchecked")
check("Task 1 still checked", plan.count("- [x]") + plan.count("- [X]") >= 9)
print(f"{sum(results)}/{len(results)} checks passed")
