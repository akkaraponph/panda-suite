# Bulk CSV inventory import implementation plan

Goal: operations staff can import pasted CSV text, retain valid additions when other rows fail, and receive added counts and line-specific rejection reasons.

Scope: parsing, validation, import orchestration and their unit tests. Source: `requirements.md` (requirements R1–R5 in listed order), `inventory.py`, and `test_inventory.py`. File upload, HTTP endpoints and persistence remain excluded. Use Python 3.9 standard library only; no dependencies. Do not change the existing `Item`, `Inventory.add_item(item: Item) -> None`, or `Inventory.get(sku: str) -> Item` contracts.

Current evidence: `Inventory.add_item` owns uniqueness, raises `KeyError` on duplicates and `ValueError` on nonpositive quantities, and mutates only after those checks. It does not enforce runtime integer types. The importer must validate quantities before calling it. Existing two tests cover successful add/get and duplicate rejection only. `python3 -m unittest discover -v` passed both baseline tests; this is not evidence for the proposed feature. This directory is not a Git repository (`git rev-parse --show-toplevel` failed), so no ignore-file change or Git ignore verification applies.

## Decisions and contracts

The following are proposed implementation choices that make unspecified input policy concrete; no unresolved decision blocks implementation:

- Add `inventory_csv.py` with public entry point `import_csv(inventory: Inventory, text: str) -> ImportReport`. The inventory remains the source of truth; the import retains each successful addition immediately. A later rejected row does not roll back earlier additions. Reimporting text rejects existing SKUs rather than updating items.
- Input is line-oriented pasted CSV: one physical line per record. Quoted commas and escaped quotes are supported using `csv.reader(..., strict=True)` on each physical line. Embedded newlines inside quoted fields are unsupported and rejected as malformed CSV. This deliberate record boundary permits recovery after an unmatched quote without losing later physical rows. Document this boundary in the module/API documentation and tests.
- Use `text.splitlines()` for physical lines, numbered from 1; LF and CRLF have identical numbering. The first physical line must parse to exactly `('sku', 'name', 'quantity')`, with no BOM, whitespace normalization, reordering or extra fields. Missing/empty input or an invalid header causes one rejection at line 1, zero additions and no data processing. A valid header alone yields zero additions and no rejections. Blank data lines are rejected, not silently skipped. A terminal newline does not create an extra row.
- Preserve SKU and name strings exactly, including whitespace and case. Do not invent blank SKU/name rejection: the current inventory accepts them and requirements impose no new constraint. Each data row must have exactly three fields. Quantity accepts only a nonempty sequence of ASCII digits with numeric value greater than zero (leading zeros allowed); reject whitespace, signs, decimal notation, exponents, non-ASCII numerals, zero and negatives. Convert with `int` and treat conversion failure as a row rejection, including interpreter limits on extremely long integers.
- `text` must be `str` and `inventory` must be an `Inventory`; programming errors outside this declared input contract are not row failures. Do not broadly catch unexpected exceptions. Catch only parsing errors, the validator's `ValueError`, and the existing `add_item` `KeyError`/`ValueError` outcomes.
- Reject duplicates against existing inventory and earlier accepted rows through `add_item`, without bypassing it or inspecting `_items`. A rejected row does not reserve its SKU. Reasons must be nonempty human-readable strings; required stable reason values are specified below.

Proposed types, all defined in `inventory_csv.py` (Python 3.9 `typing` forms, no `X | Y`):

```python
@dataclass(frozen=True)
class CsvRow:
    line_number: int
    values: Tuple[str, ...]
    error: Optional[str] = None

@dataclass(frozen=True)
class RowRejection:
    line_number: int
    reason: str

@dataclass(frozen=True)
class ImportReport:
    added_count: int
    rejected_rows: List[RowRejection]

def parse_csv(text: str) -> List[CsvRow]: ...
def row_to_item(row: CsvRow) -> Item: ...
def import_csv(inventory: Inventory, text: str) -> ImportReport: ...
```

`parse_csv` returns one `CsvRow` for each data physical line. Valid parsing produces tuple values and `error=None`, including wrong field counts for the validator to reject. Malformed CSV produces `values=()` and `error='malformed CSV'`. Header failure returns exactly one `CsvRow(1, (), 'expected header sku,name,quantity')`, so downstream logic has the same failure transport. Empty input has this same outcome. Parser results preserve source order. `row_to_item` raises `ValueError(row.error)` when error is set, `ValueError('expected 3 columns')` for an incorrect field count, and `ValueError('quantity must be a positive whole number')` for invalid quantity; otherwise it constructs `Item(sku, name, quantity)` with a real `int`. It performs no mutation. `import_csv` reports these messages unchanged; duplicates produce `duplicate sku: <sku>` (avoid the extra quotes from `str(KeyError)`), and an `add_item` `ValueError` supplies its message. Report rejections remain in source order and include each rejected data row once; header failure is the sole rejection when applicable. `added_count` counts only successful `add_item` calls.

## File responsibilities

| File | Responsibility |
| --- | --- |
| `inventory.py` | Existing inventory and Item; unchanged behavior and implementation |
| `inventory_csv.py` (new) | CSV types, parsing, pure validation and import orchestration; imports `Inventory`/`Item` from inventory; inventory never imports this module |
| `test_inventory_csv.py` (new) | Parser, validator and integration/report tests using standard-library unittest and unittest.mock |
| `test_inventory.py` | Existing regression assertions retained |

## Ordered implementation tasks

- [ ] **T1 — Parse physical records and retain source locations** (R1, R3, R5)

  Outcome: implement proposed `CsvRow` and `parse_csv(text: str) -> List[CsvRow]` in `inventory_csv.py`; add parser tests in `test_inventory_csv.py` and document the record/header policy. Prerequisites: none. Consumes pasted string input and the exact header contract above; produces ordered `CsvRow` values/errors for T2/T3. No inventory mutations.

  Acceptance/check **C1**: assert exact row line numbers and values for header plus quoted commas, escaped quotes, LF/CRLF, a blank data line and a terminal newline. Assert wrong header, empty input, whitespace/reordered/extra header fields return the sole line-1 header error; header-only input returns an empty list. Assert malformed quoted line is an error and the next valid physical line is still parsed. Explicitly test unsupported embedded-newline records. This rejects `DictReader` defaults that silently skip blank lines, missing source positions, permissive headers and a parser that consumes subsequent rows after an unmatched quote.

  Verification: `python3 -m unittest test_inventory_csv -v` (proposed module exists after this task); expected evidence is passing C1 assertions, not merely successful import of the new module.

- [ ] **T2 — Convert parsed rows to validated items** (R2, R4, R5)

  Outcome: implement proposed `row_to_item(row: CsvRow) -> Item` in `inventory_csv.py` and its pure validation tests. Prerequisite: T1; consumes the exact `CsvRow` type and error sentinel above, produces existing `Item` or `ValueError` with the prescribed reason. No inventory access or mutation.

  Acceptance/check **C2**: assert valid `1` and `001` become integer 1 while SKU/name remain byte-for-byte equal as Python strings, including empty/whitespace fields. Assert field counts 0, 2 and 4 fail with `expected 3 columns`. Assert quantities empty, whitespace, `0`, `00`, `-1`, `+1`, `1.0`, `1e2`, ` 1`, `1 ` and non-ASCII digits fail with the exact quantity reason. Assert a parser error is propagated before field/quantity validation. Simulate an integer-conversion failure if needed to cover runtime length limits without a Python-version-specific assumption. This rejects `int`-only acceptance of signs/whitespace and accidentally passing strings or floats to inventory.

  Verification: `python3 -m unittest test_inventory_csv -v`; expected evidence is C1 and C2 assertions passing under Python 3.9-compatible code.

- [ ] **T3 — Import independently and return complete rejection reports** (R2, R3, R4, R5)

  Outcome: implement proposed `RowRejection`, `ImportReport` and `import_csv(inventory: Inventory, text: str) -> ImportReport` in `inventory_csv.py`; add integration/report tests and entry-point documentation in that module. Prerequisites: T1 and T2. Consumes `parse_csv`'s ordered `List[CsvRow]`, `row_to_item`'s existing `Item`/prescribed `ValueError`, and `Inventory.add_item(item: Item) -> None` with current `KeyError`/`ValueError`; produces exactly the report type above while retaining successful mutations.

  Acceptance/check **C3**: start with SKU `EXIST`; import lines including a valid new SKU, invalid quantity, existing SKU, repeated newly added SKU, malformed CSV, wrong column count and a final valid row. Assert exact `added_count`, rejection line numbers/reasons/order, and inventory contents including the final row. Confirm first accepted value wins for duplicates. Use a spy wrapping `add_item` to establish every successfully validated row goes through it, including duplicate attempts; invalid rows never call it. Add invalid-then-valid rows sharing a SKU to prove rejection does not reserve the SKU. Repeat an import to prove duplicate reporting and preservation of existing data.

  Acceptance/check **C4**: invalid header returns one line-1 rejection and makes no `add_item` calls; header-only succeeds empty. With an `Inventory` subclass or mock wrapping the declared boundary, make one `add_item` call raise `ValueError('quantity must be positive')`, then succeed; assert that error is reported and the later row is attempted. An unexpected `RuntimeError` must propagate rather than being hidden as a row failure. Assert counts only increase after successful adds. Preserve both existing `test_inventory.py` tests. These checks reject fail-fast imports, direct `_items` writes, pre-validation mutation, hidden programming failures, misleading counts and all-or-nothing rollback.

  Verification: `python3 -m unittest discover -v` (confirmed repository command). Run the same command with a Python 3.9 interpreter where available and inspect imports/syntax for standard-library-only compatibility. Python 3.9 execution remains an evidence gap if that interpreter is unavailable; record interpreter version with future results. Expected evidence: C1–C4 and both original regressions pass on the implementation revision.

## Review focus

| Easily missed input/failure | Expected behavior | Owning check |
| --- | --- | --- |
| Unclosed quote followed by a valid physical row | Reject malformed line, still add later row | T1 C1 / T3 C3 |
| Header absent versus header only versus blank data line | Header rejection versus empty success versus row rejection | T1 C1 / T3 C4 |
| Signed/whitespace/non-ASCII quantity | Reject despite integer conversion accepting some forms | T2 C2 |
| Duplicate after an accepted row versus SKU after rejected row | First accepted value retained; rejected row reserves nothing | T3 C3 |
| Expected add failure versus unexpected failure | Report expected failure and continue; propagate unexpected bug | T3 C4 |

## Requirement coverage and compatibility gate

| Requirement | Tasks | Check and expected evidence |
| --- | --- | --- |
| R1 parse and source locations | T1 | C1 exact line/value assertions |
| R2 valid rows through add_item, continue on failure | T2, T3 | C2 validation; C3 spy and contents; C4 expected failure continuation |
| R3 count and per-row line/reason report | T1, T3 | C1 header errors; C3/C4 exact report assertions |
| R4 positive whole quantity, unique SKU | T2, T3 | C2 invalid input matrix; C3 duplicate scenarios |
| R5 Python 3.9 stdlib only | T1–T3 | Source/import review and C1–C4 under Python 3.9, evidence pending |

Gate G1 is **defined; evidence pending**, blocking compatibility acceptance: on the final implementation revision, C1–C4 and the existing regressions must pass, and Python 3.9/stdlib compatibility must be checked as above. This is a new additive API; callers of the original inventory must keep existing successful results and exception behavior. No migration, persistence or deployment work is required. Rollback removes the new module/API; already added in-memory items remain for that inventory instance, as with ordinary `add_item` use. The report provides operational visibility for rejected input; no logging infrastructure is required.

## Readiness and handoff

**EXECUTION-READY.** First unblocked task: T1. T2 depends on T1; T3 depends on both. All mandatory requirements map to checks. No feature checks have run because implementation is outside this request; Python 3.9 runtime verification is a future evidence requirement. The baseline two-test run establishes only current behavior.

Review this plan before a later implementation request. For a future execution handoff: `Use panda-execute (native) to implement .panda-suite/plans/2026-11-14-bulk-csv-import.md`. Native execution is proportionate for these three tightly coupled tasks in a small in-memory module. This planning request does not authorize implementation.
