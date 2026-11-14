# Bulk CSV import implementation plan

## Goal, scope, sources and constraints

Add an in-memory CSV import function that imports valid items through `Inventory.add_item` and reports rejected rows without stopping later valid rows.

Source of requirements: `requirements.md`, numbered requirements R1–R5. Current implementation: `inventory.py:6–25`; current assertions: `test_inventory.py:7–16`.

- R1: parse CSV and retain source line numbers.
- R2: send every valid row through the existing `Inventory.add_item`; isolate bad rows.
- R3: report the added count and each rejected row's line number and human-readable reason.
- R4: positive whole-number quantities and unique SKUs.
- R5: Python **3.9**, standard library only, **no new dependencies**.
- Exclusions: file upload, HTTP endpoints, persistence, changes to existing direct `add_item` or `get` behavior. No application implementation is authorized by this plan.

Confirmed: `add_item(item: Item) -> None` raises `KeyError` for an existing SKU before checking quantity, raises `ValueError` for nonpositive quantity, and only then mutates `_items`. It does not itself enforce integer types. Existing tests cover successful addition and an existing duplicate only; they do not prove import behavior or quantity validation.

## Proposed decisions and contracts

The following are concrete implementation choices for review, with no unresolved implementation decision. Add `csv_import.py`, importing `Item` and `Inventory`; `inventory.py` does not depend on the importer.

Use frozen dataclasses and Python 3.9-compatible typing:

```python
@dataclass(frozen=True)
class CsvRow:
    line_number: int
    sku: str
    name: str
    quantity_text: str

@dataclass(frozen=True)
class RejectedRow:
    line_number: int
    reason: str

@dataclass(frozen=True)
class ParsedCsv:
    rows: Tuple[CsvRow, ...]
    rejected: Tuple[RejectedRow, ...]

@dataclass(frozen=True)
class ImportReport:
    added_count: int
    rejected: Tuple[RejectedRow, ...]

def parse_csv(text: str) -> ParsedCsv: ...
def import_csv(inventory: Inventory, text: str) -> ImportReport: ...
```

- Input is CSV text, not a filename. Omission of required Python arguments raises the ordinary `TypeError`; explicit `None` or other non-string `text` raises `TypeError("text must be a string")` before inventory mutation.
- Require the first CSV record to be exactly the three fields `sku,name,quantity` in that order, case sensitive, without trimming header fields. Empty text, missing header, wrong columns/order/case, or syntactically malformed header raises `ValueError("expected header: sku,name,quantity")`; nothing imports. Header-only input returns zero additions and no rejections. No BOM normalization is proposed.
- Use standard-library `csv.reader` with comma delimiter, double-quote quoting, and `strict=True`. Retain physical newline information, including LF and CRLF. A record's line number is its one-based starting physical line; a quoted field may span lines. Ignore truly blank physical lines between records, but count them for numbering. A whitespace-only line or a record with empty fields is not blank.
- Data records need exactly three fields. Wrong field count yields `RejectedRow(start_line, "expected 3 fields")`; continue afterward. Preserve SKU and name text verbatim, including whitespace and empty strings, matching the existing inventory's lack of additional field restrictions. SKU equality remains exact and case sensitive.
- Malformed data CSV yields `RejectedRow(start_line, "invalid CSV syntax")`. To prevent an unterminated quote from swallowing later valid rows, after a `csv.Error` retry parsing from the physical line immediately after the failed record's starting line, including lines consumed by the failed reader. On a successful record advance past all its consumed physical lines. This recovery is a proposed deterministic best-effort policy: following fragments can themselves become rejected records; never promise to reconstruct the intended boundaries of malformed quoted input. Use a progress check so every attempt advances at least one physical line. Keep tests for quoted multiline success and unclosed-quote recovery. No alternative CSV engine or bespoke CSV tokenizer is needed.
- Validate quantity before constructing an `Item`: strip surrounding quantity whitespace; require one or more ASCII digits `0`–`9`, convert with base 10, and require value greater than zero. Leading zeros are allowed. Empty, omitted field, sign, fractional/exponent notation, Unicode digits, zero, and negative input cannot import. Missing fields fail the field-count check; all other invalid quantities report `"quantity must be a positive whole number"`. Catch conversion `ValueError` too, including interpreter integer-string limits where present.
- Only quantity-valid parsed rows call `inventory.add_item(Item(...))`, once each, in source order. Do not inspect or write `_items`. Successful calls increment the count. Catch `KeyError` and `ValueError` from `add_item` per row; turn `KeyError` into `"duplicate sku: {sku}"` without Python exception quotation decoration and use `str(error)` for `ValueError`. Unexpected exception types propagate; this is a programming/dependency failure, not a rejected input row, and previously successful additions remain.
- First successfully added occurrence of a SKU wins, including duplicates within one CSV. An invalid earlier occurrence does not reserve the SKU. Return all parse and inventory rejections sorted by source line. Import is additive, with no transaction rollback, retry deduplication mechanism, logging infrastructure, or persistence. Retrying the same text reports already-added SKUs as duplicates.

## Files and responsibilities

| File | Responsibility |
| --- | --- |
| `csv_import.py` (new) | Public result models, CSV parsing/recovery, import orchestration and quantity validation |
| `test_csv_import.py` (new) | `unittest` coverage for the new public boundary, state and failure behavior |
| `inventory.py` | Reused unchanged as authoritative storage and uniqueness enforcement |
| `test_inventory.py` | Preserve and rerun both existing regression assertions |

## Ordered tasks

- [ ] **T1 — Parse CSV with source locations and recoverable row errors.**
  - Requirements: R1, parsing portion of R3, R5. Prerequisites: none.
  - Affected files: new `csv_import.py` and `test_csv_import.py`.
  - Consumes: `text: str` with the header and dialect above. Produces the exact proposed `CsvRow`, `RejectedRow`, `ParsedCsv`, and `parse_csv(text: str) -> ParsedCsv` contracts. Preserve field text, return rows in source order, and implement the stated document errors, blank-line rules and syntax recovery. Add these API contracts to module docstrings.
  - Acceptance/checks: unit tests assert concrete field values and starting line numbers for LF/CRLF, quoted commas, escaped quotes, a multiline quoted name, and blank lines. Assert a valid record after a wrong-width row remains in `rows` and that rejection is attributed to the failed row. For an unclosed quote on line 2 followed by a valid physical row on line 3, expect a syntax rejection at 2 and the valid row at 3. Assert no duplicate emission while recovering. Assert header-only gives empty tuples; empty text, bad header, malformed header, and `None` raise the specified errors. Assert a whitespace-only line is rejected for field count and an empty SKU/name survives parsing. These checks reject line numbering based on row count, naive comma splitting, and stopping after malformed input.
  - Verification: `python3 -m unittest -v test_csv_import` and `python3 -m unittest -v` from the workspace root. Expected evidence: parser tests and both inventory regressions pass; no source changes to `inventory.py`.

- [ ] **T2 — Import valid rows and return an accurate rejection report.**
  - Requirements: R2, R3, R4, R5. Prerequisite: T1.
  - Affected files: `csv_import.py`, `test_csv_import.py`; preserve existing files.
  - Consumes: T1's `ParsedCsv.rows: Tuple[CsvRow, ...]`, `ParsedCsv.rejected: Tuple[RejectedRow, ...]`, exact parser error semantics, and established `Inventory.add_item(item: Item) -> None`/`Inventory.get(sku: str) -> Item`. Produces proposed `ImportReport` and `import_csv(inventory: Inventory, text: str) -> ImportReport` with the signatures and behavior above. Document additive behavior, header failure, and report ordering in its docstring.
  - Acceptance/checks: integration tests import a mixture of successful, quantity-invalid, malformed-width, and duplicate rows into a seeded `Inventory`, assert exact count/reason/line tuples and retrieved `Item` values, and verify seed state survives. A later valid row after each rejection must exist. A recording `Inventory` subclass verifies each quantity-valid parsed row reaches `add_item` once in input order; invalid quantities never reach it. Include accepted `1`, `001`, and whitespace-surrounded digits; rejected empty quantity, `0`, `-1`, `+1`, `1.0`, `1e2`, nonnumeric and Unicode digits. Test duplicate against existing inventory and within the text, case-sensitive distinct SKUs, and invalid-first/valid-second same SKU. Preserve empty SKU/name behavior. Header error on a seeded inventory leaves it unchanged. Test a controlled `ValueError` from an `Inventory` subclass yields one rejection and allows the next row; controlled `RuntimeError` propagates with prior successes retained. Check report ordering where parse rejection occurs after an earlier duplicate. Retry a successful import and assert duplicate reports with zero added count. These tests reject bypassing `add_item`, broad exception swallowing, counting attempts, truthiness-based quantity validation, and last-duplicate-wins behavior.
  - Verification: `python3 -m unittest -v` from the workspace root; inspect imports and syntax for Python 3.9 compatibility. Run the same suite with a Python 3.9 interpreter when available. Expected evidence: all new tests and existing regression assertions pass, no dependency additions, and no out-of-scope interfaces or state changes.

## Review focus

| Likely omission | Expected behavior | Owning check |
| --- | --- | --- |
| Multiline names and blank lines | Source starting physical line remains accurate | T1 multiline/blank fixtures |
| Unterminated quoted row consumes later input | Deterministic recovery imports later valid physical row | T1 unclosed quote fixture |
| Numeric-looking invalid values | Only positive ASCII whole-number quantity accepted | T2 quantity table |
| Duplicate or invalid-first repeated SKU | First successful item wins; invalid row reserves nothing | T2 duplicate fixtures and final state |
| Parser errors mixed with inventory failures | Every rejection returned in source order; additions count only success | T2 mixed integration and subclass fixtures |

## Traceability and expected evidence

| Requirement | Task | Check | Expected evidence |
| --- | --- | --- | --- |
| R1 parse with line numbers | T1 | Quoting, multiline, newline and blank-line assertions | Exact `CsvRow` values and starting lines |
| R2 valid rows through existing method; continue | T2 | Recording subclass, mixed valid/invalid, recovery integration | Ordered calls and later items present |
| R3 added count and per-row reasons | T1, T2 | Exact parser rejection tuples and mixed report | Count equals actual additions; ordered line/reason tuples |
| R4 positive integer and unique SKU | T2 | Quantity table; seeded/intra-input/invalid-first duplicates | Invalid rows absent; original items preserved |
| R5 Python 3.9 stdlib only | T1, T2 | Imports/syntax inspection and Python 3.9 suite | No external imports; compatible syntax; suite results on target runtime |

## Readiness and execution handoff

**EXECUTION-READY.** T1 is the first unblocked task; T2 follows T1 and consumes its specified interfaces. There are no unresolved implementation blockers. Proposed parsing and recovery policies above are part of the plan for user review before execution. Both tasks remain unchecked until implementation acceptance checks produce evidence.

Planning observation: `python3 -m unittest -v` passed both existing tests. That does not validate future importer behavior. Python 3.9 execution and all new tests remain evidence gaps; the observed default interpreter was not established as Python 3.9. No release or deployment boundary was requested, so no release gates are defined. This workspace is not a Git repository (`git rev-parse --show-toplevel` failed); repository ignore/index requirements do not apply here.

User selected sequential subagent execution in advance: retain that choice. After the user reviews this plan, the intended handoff is a fresh implementing subagent and fresh reviewer for T1, then the same pattern for T2, followed by whole-change review. This fits two tasks with one shared parsing contract and catches reporting/state mistakes before moving on. Do not start implementation merely because this plan is saved.

Review request: Please review the plan. When approved, use: “Use panda-execute (subagent-driven, one task at a time) to implement `.panda-suite/plans/2026-11-14-bulk-csv-import.md`.”
