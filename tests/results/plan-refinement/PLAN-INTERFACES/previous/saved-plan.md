# Plan: Bulk CSV import into `Inventory`

## Goal

Let operations staff paste CSV text with the header `sku,name,quantity` and add
many items at once. Every valid row goes through the existing
`Inventory.add_item`. A bad row never stops later rows. The caller gets back a
report with the number of rows added and, for each rejected row, its line number
and a readable reason.

## Scope

In scope:

- A pure parsing step that turns CSV text into rows, each with its source line
  number.
- An import step that validates each row, calls `Inventory.add_item`, and builds
  the report.
- Unit tests for both steps.

Out of scope (from `requirements.md`): file upload, HTTP endpoints, persistence.
Changing `Inventory.add_item` or `Item` is also out of scope. The importer works
with them as they are.

## Sources and constraints

- `requirements.md`: requirements R1–R5 below.
- `inventory.py`: `Item(sku: str, name: str, quantity: int)` is a frozen
  dataclass. `Inventory.add_item(item)` raises `KeyError("duplicate sku: …")` if
  the SKU already exists and `ValueError("quantity must be positive")` if
  `quantity <= 0`. Otherwise it stores the item. It does not check types or
  blank strings. The store is a plain in-memory dict, with no transactions.
- `test_inventory.py`: tests use `unittest` and import modules by their flat
  names from the project root (`from inventory import Inventory, Item`).
- Constraint: Python 3.9 standard library only, with no new dependencies.

| ID | Requirement (from `requirements.md`) |
|----|--------------------------------------|
| R1 | Parse CSV text into rows that keep their source line numbers. |
| R2 | Import every valid row through `Inventory.add_item`. One bad row must not stop the rest. |
| R3 | Return a report with the count of rows added and, for each rejected row, its line number and a readable reason. |
| R4 | Quantity must be a positive whole number. SKUs stay unique. |
| R5 | Python 3.9 standard library only. No new dependencies. |

## Evidence anchors

These were checked in the workspace on 2026-11-12:

- `python3 -m unittest -v` in the project root runs 2 tests and prints `OK`.
- The local interpreter is Python 3.15.0, and no `python3.9` is installed. The
  existing check cannot prove 3.9 compatibility (see Risk K1).
- In this Python, `int()` accepts `" +3 "`, `"1_000"` and the Arabic-Indic digit
  `"٣"`. So using `int()` alone to check quantity would let in values that are
  not plain whole numbers (see D3).
- `csv.reader(...).line_num` reports the *last* physical line of a record. A
  quoted field that spans lines 2–3 reports `3`. A blank line comes back as an
  empty list `[]`. The start line of a record is therefore
  `previous line_num + 1`.
- With `csv.field_size_limit(10)`, a 50-character field on line 3 raises
  `csv.Error: field larger than field limit (10)` with `line_num == 3`. This
  gives Task 2 a reliable way to test the `csv.Error` path on Python 3.15.
- The workspace is not a Git repository, so no `.gitignore` update applies to
  this plan file.

## Decisions taken in this plan

The requirements leave these points open. Each choice is a default that the
plan's tests lock in. If a stakeholder disagrees, change the decision and its
test together.

- **D1 Line numbers.** Line numbers are 1-based physical lines of the pasted
  text, and the header is line 1. A record that spans several lines (a quoted
  newline) is reported at its *first* line.
- **D2 Header.** The first non-blank record must be exactly `sku`, `name`,
  `quantity` in that order. Each header cell is trimmed of surrounding
  whitespace before comparison, the match is case-sensitive, and one leading
  UTF-8 BOM (`﻿`) is ignored. If the input has no header or the wrong
  header, the importer raises `ValueError` before any `add_item` call, so the
  inventory is unchanged. With no valid header no row can be read, so this is
  not a row-level rejection. Input that holds only a header gives
  `added=0, rejected=[]`.
- **D3 Quantity.** Trim surrounding whitespace, then require the value to fully
  match `[0-9]+` (ASCII digits only), then require `int(value) > 0`. This
  rejects `""`, `"0"`, `"-1"`, `"+3"`, `"3.0"`, `"1e3"`, `"1_000"`, `"٣"` and
  `"abc"`. Leading zeros are accepted, so `"007"` becomes 7.
- **D4 SKU and name.** Trim surrounding whitespace from both. Reject a row whose
  SKU or name is empty after trimming. `Item` and `add_item` allow empty
  strings, but an empty SKU is never a sensible key. Uniqueness is checked on
  the trimmed SKU and is case-sensitive, the same as the existing dict.
- **D5 Blank lines.** A record that is entirely empty (`[]`) or whose cells are
  all whitespace is skipped silently. It is neither added nor rejected.
- **D6 Field count.** A non-blank row must have exactly 3 fields. If it has more
  or fewer, the row is rejected with a reason that gives the count, for example
  `expected 3 fields (sku,name,quantity), got 4`.
- **D7 Duplicates.** If a SKU is already in the inventory or appeared earlier in
  the same paste, the row is rejected through `add_item`'s `KeyError`. The first
  occurrence wins. The reason is written by the importer as
  `duplicate sku: <sku>`. Do not use `str(KeyError)`, because that adds extra
  quotes around the message.
- **D8 Partial import.** There is no rollback. Rows added before a rejected row
  stay added (R2), so the report is the record of what happened.
- **D9 Report order.** Rejections are listed in ascending line order, which is
  the order they are found.

## Interfaces

New module `csv_import.py` in the project root, next to `inventory.py`:

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class CsvRow:
    line: int            # 1-based first physical line of the record (D1)
    fields: List[str]    # raw cells as returned by csv.reader, untrimmed

@dataclass(frozen=True)
class RowError:
    line: int
    reason: str          # readable, e.g. "quantity must be a positive whole number: '0'"

@dataclass(frozen=True)
class ImportReport:
    added: int
    rejected: List[RowError]

@dataclass(frozen=True)
class ParsedCsv:
    rows: List[CsvRow]
    malformed: Optional[RowError]  # set when csv.Error stopped reading (K2); None otherwise

def parse_csv(text: str) -> ParsedCsv:
    """Validate the header (D2) and return the data rows after it.
    Blank records are dropped (D5). Raises ValueError on missing or wrong header.
    A csv.Error after the header ends reading: the rows so far are returned and
    malformed = RowError(start_line, "malformed CSV: <msg>")."""

def import_csv(inventory: Inventory, text: str) -> ImportReport:
    """parse_csv, then validate each row and call inventory.add_item.
    Raises only what parse_csv raises (header problems). Every row-level
    problem becomes a RowError."""
```

How errors reach the caller:

| Input condition | Outcome |
|-----------------|---------|
| `text == ""`, only whitespace or blank lines, or wrong header | `ValueError` from `parse_csv` / `import_csv`. Inventory unchanged. |
| Header only | `ImportReport(added=0, rejected=[])` |
| Wrong field count | `RowError`, then continue |
| SKU or name empty or only whitespace | `RowError`, then continue |
| Quantity missing, empty, non-numeric, zero, negative, signed, decimal, or non-ASCII digits | `RowError`, then continue. `add_item` is not called. |
| Duplicate SKU (already in the inventory or earlier in the paste) | `KeyError` from `add_item` is caught → `RowError("duplicate sku: X")`, then continue |
| `ValueError` from `add_item` (backstop, not expected after D3) | caught → `RowError(str(exc))`, then continue |
| `csv.Error` while reading a data record | `RowError(line, "malformed CSV: …")` as the last rejection. Reading stops there (K2). |

Only `KeyError` and `ValueError` from `add_item` are caught. Any other exception
is a bug and must propagate.

## File map

| File | Change | Responsibility |
|------|--------|----------------|
| `csv_import.py` | new | `CsvRow`, `ParsedCsv`, `RowError`, `ImportReport`, `parse_csv`, `import_csv` |
| `test_csv_import.py` | new | `unittest` tests for parsing, validation and import |
| `inventory.py` | none | existing `Item` / `Inventory` contract (read only) |
| `test_inventory.py` | none | existing regression suite, must stay green |

## Tasks

### Task 1: Parse CSV text with line numbers (R1, R5)

Objective: implement `CsvRow`, `RowError`, `ParsedCsv` and `parse_csv` in `csv_import.py`.
Prerequisites: none.

- [ ] Create `csv_import.py` with stdlib imports only (`csv`, `io`, `re`,
      `dataclasses`, `typing`).
- [ ] Read with `csv.reader(io.StringIO(text))`. Track the start line of each
      record as `previous reader.line_num + 1`, starting at 1 (D1).
- [ ] Remove one leading `﻿` from `text` before parsing (D2).
- [ ] Skip blank records (D5). Treat the first non-blank record as the header
      and validate it (D2). Raise `ValueError("missing header: expected
      sku,name,quantity")` or `ValueError("invalid header: expected
      sku,name,quantity, got …")`.
- [ ] Return the remaining non-blank records as `CsvRow`s inside `ParsedCsv`.
      Do not check field counts here. That is Task 2's job.
- [ ] If `csv.Error` is raised while reading a record after the header, stop
      reading and set `malformed = RowError(start_line, f"malformed CSV: {exc}")`.
      A reader that raised has no defined resume point (K2). A `csv.Error` while
      reading the header raises `ValueError` instead, the same as a wrong header.
- [ ] Write tests in `test_csv_import.py`, class `ParseCsvTest`:
  - [ ] header plus 2 rows → row lines `[2, 3]`, `malformed is None`
  - [ ] a blank line between rows → the line after it keeps its physical
        number, and the blank line is not returned
  - [ ] a quoted name with an embedded newline on lines 2–3 → `line == 2`, and
        the next record gets line 4
  - [ ] `"\r\n"` line endings give the same line numbers as `"\n"`
  - [ ] leading BOM and `" sku , name , quantity "` are both accepted
  - [ ] `""`, `"\n\n"`, `"SKU,name,quantity"`, `"sku,quantity,name"` and
        `"sku,name"` each raise `ValueError`
  - [ ] header only → `rows == []`, `malformed is None`

Acceptance: every listed case passes. `parse_csv` never touches an `Inventory`.
Verify: `python3 -m unittest test_csv_import -v`.

### Task 2: Validate rows and import them through `add_item` (R2, R3, R4)

Objective: implement `ImportReport` and `import_csv`.
Prerequisites: Task 1.

- [ ] For each `CsvRow`, check in this order and record the first failure only:
      field count (D6), then trimmed SKU not empty (D4), then trimmed name not
      empty (D4), then quantity (D3, using
      `re.fullmatch(r"[0-9]+", value.strip())` followed by `> 0`).
- [ ] For a valid row, build `Item(sku, name, int(qty))` and call
      `inventory.add_item`. Catch `KeyError` → `RowError(line, f"duplicate sku:
      {sku}")` and `ValueError` → `RowError(line, str(exc))`. Increase `added`
      only after `add_item` returns.
- [ ] Reasons must be readable sentences that quote the bad value with
      `repr()`, so blanks and spaces are visible. Examples:
      `quantity must be a positive whole number: '0'`, `sku is empty`,
      `name is empty`, `expected 3 fields (sku,name,quantity), got 2`.
- [ ] After processing `parsed.rows`, append `parsed.malformed` to `rejected`
      if it is set (it always has the highest line number, so D9 order holds).
      State in the `import_csv` docstring that structurally malformed CSV is the
      one case where later text is not processed (K2). If you prefer another
      policy, escalate it rather than inventing one.
- [ ] Write tests in `test_csv_import.py`, class `ImportCsvTest`, using a fresh
      `Inventory()` for each test:
  - [ ] 3 valid rows → `added == 3`, `rejected == []`, and each item can be
        read with `inventory.get`
  - [ ] a bad row in the middle (quantity `"abc"` on line 3) → rows on lines 2
        and 4 are added, `rejected == [RowError(3, …)]` (R2)
  - [ ] quantities `"0"`, `"-1"`, `"+3"`, `"3.0"`, `"1_000"`, `"٣"`, `""` and
        `" "` are each rejected. `" 5 "` and `"007"` are accepted as 5 and 7.
  - [ ] duplicate inside the paste → first row added, second rejected with
        `duplicate sku: A-1`
  - [ ] SKU already in the inventory before import → rejected, and the existing
        item is unchanged
  - [ ] empty SKU, empty name, 2 fields and 4 fields → each rejected with its
        own reason
  - [ ] wrong header → `ValueError`, and the inventory is unchanged (it still
        has its preloaded item and nothing else)
  - [ ] the report keeps line order across several rejections
  - [ ] multi-line quoted row followed by a bad row → the bad row's line is
        correct
  - [ ] `csv.Error` path: temporarily lower `csv.field_size_limit()` in the
        test (restore it in `finally`/`addCleanup`), paste a row whose name is
        longer than the limit after one valid row → valid row added, last
        rejection is `malformed CSV: …` at the oversized row's line. Confirm
        this triggers `csv.Error` on the interpreter used. If it does not, test
        `parse_csv`'s handling with a patched reader and say so in the test
        docstring.

Acceptance: all of R2–R4 are shown by the tests above, and no exception other
than the header `ValueError` escapes `import_csv` for any listed input.
Verify: `python3 -m unittest test_csv_import -v`.

### Task 3: Full regression and compatibility check (R5)

Objective: confirm nothing else broke and that the code is 3.9-compatible.
Prerequisites: Tasks 1–2.

- [ ] Run `python3 -m unittest -v` in the project root. Expect both
      `test_inventory` tests and all `test_csv_import` tests to pass (the
      current baseline is 2 tests, `OK`).
- [ ] Check that `csv_import.py` imports only stdlib modules (`grep -n
      "^import\|^from" csv_import.py`).
- [ ] 3.9 compatibility: avoid `match` statements, `X | Y` type unions in
      runtime annotations, `zip(strict=…)`, `dataclass(slots=…, kw_only=…)`
      and other features added after 3.9. If a 3.9 interpreter is available
      (for example `python3.9 -m unittest -v`, or a `python:3.9` container),
      run the suite on it. If not, report this check as **not run**.

Acceptance: the full suite passes on the available interpreter, and the 3.9 run
either passes or is clearly reported as not run.

## Requirement → task → check

| Req | Task | Check |
|-----|------|-------|
| R1 | 1 | `ParseCsvTest` line-number cases (plain, blank line, multi-line, CRLF) |
| R2 | 2 | bad row in the middle, later rows still added; duplicates do not stop the import |
| R3 | 2 | assertions on `added` count and `RowError(line, reason)` equality and order |
| R4 | 2 | quantity edge-case matrix; duplicates in the paste and against existing items |
| R5 | 1, 3 | stdlib import check; 3.9 interpreter run, or reported as not run |

## Risks and open items

- **K1 No Python 3.9 interpreter locally.** The workspace has only Python
  3.15.0. Mitigation: Task 3 lists the features to avoid, and the 3.9 run must
  be reported honestly.
- **K2 `csv.Error` mid-stream.** The plan stops the import at that point (see
  Task 2). This goes against the wording "one bad row must not stop the
  remaining rows" only for text that is not valid CSV structure. **Open
  decision** for the requirements owner: accept this stopping behaviour, or
  reject the whole paste up front.
- **K3 Policy defaults D2–D7.** Header strictness, trimming, leading zeros,
  rejecting blank SKU or name, and first-occurrence-wins for duplicates are
  assumptions. Each one has a test, so a change is a one-line policy edit plus
  its test.
- **K4 No rollback (D8).** This follows directly from R2. Callers must use the
  report, not exceptions, to learn the result. Header failures are the only case
  that leaves the inventory untouched.
- **K5 Case-sensitive SKUs.** `A-1` and `a-1` are treated as different SKUs,
  matching the existing `Inventory`. If they should be the same, that change
  belongs in `Inventory`, not in the importer.
