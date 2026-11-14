# Bulk CSV import implementation plan

Goal: operations staff paste `sku,name,quantity` CSV and receive an added count and line-numbered rejection reasons while valid rows enter the existing inventory.

Status: **PARTIALLY READY**. T2 can start once implementation is separately authorized. T1 and T3 require the CSV record/recovery decision below. No implementation is authorized by this plan. Checkboxes remain open; no implementation checks have run.

## Sources, scope, and constraints

- `requirements.md` R1: parse CSV and retain source line numbers; R2: add every valid row through `Inventory.add_item`, continuing past bad rows; R3: return count and each rejection's line/reason; R4: positive whole-number quantity and unique SKUs; R5: Python **3.9**, **standard library only**, **no new dependencies**.
- `inventory.py`: frozen `Item(sku: str, name: str, quantity: int)`; `Inventory.add_item(self, item: Item) -> None` rejects duplicates with `KeyError` and nonpositive quantities with `ValueError`, stores successes immediately. `get(self, sku: str) -> Item` retrieves stored items. Preserve these APIs and semantics.
- `test_inventory.py`: `unittest` asserts add/get and duplicate rejection only. These tests do not establish CSV behavior or integer validation.
- In scope: in-memory CSV parsing, validation, sequential insertion and report. Excluded: file uploads, HTTP, persistence, dependencies and changes to existing direct callers' validation behavior.
- Workspace is not a Git repository (`git rev-parse --show-toplevel` failed). No ignore change or `git check-ignore` applies here. Saving this plan creates no application behavior.

## Decisions and unresolved policy

**D1, blocking T1/T3:** does each physical line represent one record (so malformed quoting is rejected on that line and processing resumes on the next), or must quoted fields support embedded newlines? Under multiline CSV, an unmatched quote can consume subsequent lines, and there is no unambiguous way to identify the intended next record. The latter choice requires an explicit recovery rule or narrowed continuation guarantee. Do not silently choose either behavior.

Proposed nonblocking choices, adopted for the planned API:

- Require exact header values and order `sku,name,quantity`; no BOM, trimming or case folding. Header-only input returns zero added and no errors. Empty input or any other header raises `ValueError("expected header: sku,name,quantity")` before mutation. This is an input-wide error, distinct from row rejections.
- Preserve SKU/name values exactly; no new blank-field restrictions. Empty SKU and name are allowed because requirements add no such restriction and `Inventory.add_item` permits them. Whitespace and case remain significant for uniqueness.
- Quantity syntax is one or more ASCII digits and integer value greater than zero. Reject empty, whitespace, signs, decimal/exponent notation, non-ASCII numerals, zero and negatives. Leading zeroes are accepted. Convert only after syntax validation; conversion failures, including runtime digit limits where applicable, become row rejections.
- Every non-header record, including blank records, must contain exactly three fields. Reject shorter/longer records; missing trailing quantity and explicit empty quantity both fail quantity validation once field count is three. CSV has no separate null value; literal `null` is text and is invalid as a quantity.
- Source line numbers are 1-based physical lines, counting the header as line 1. For any allowed multiline record use its starting line. Report rejected records in source order.
- Insert in source order; first successful occurrence of an exact SKU wins. Existing inventory entries also win. Rejected rows do not reserve SKUs. No whole-import rollback; successful rows persist. Report only expected input/duplicate failures; unexpected internal failures propagate instead of masquerading as row errors. Concurrent imports are outside this scope.

## Files and proposed contracts

- `inventory.py`: unchanged source of truth and owner of uniqueness/storage.
- New `csv_import.py`: parsing, pure row validation and import orchestration; imports `Item` and `Inventory`, with no reverse import.
- New `test_csv_import.py`: standard-library `unittest` tests and inline CSV fixtures.
- `test_inventory.py`: retained regression coverage, no required changes.

New interfaces are **proposed**, not existing source:

```python
@dataclass(frozen=True)
class ImportError:
    line_number: int
    reason: str

@dataclass(frozen=True)
class ImportReport:
    added_count: int
    errors: List[ImportError]

def _item_from_fields(fields: List[str]) -> Item: ...
def import_csv(inventory: Inventory, text: str) -> ImportReport: ...
```

Use `typing.List` for Python 3.9-compatible annotations. `_item_from_fields` raises `ValueError` with exactly `expected 3 fields` or `quantity must be a positive whole number`. Orchestration converts duplicate `KeyError` into `duplicate sku: <sku>` without the quotes added by `str(KeyError)`. Parsing errors use `invalid CSV: <parser detail>`; assert the stable prefix rather than interpreter-specific detail. Import report lists contain only rejected data records, never successful ones. Non-string `text` raises `TypeError`; it is not part of the pasted-text contract.

## Ordered implementation tasks

- [ ] **T1 — Establish CSV record framing and parsing (R1, R2, R3, R5).** Prerequisite: D1 answered. Consume pasted `text: str` and the header policy above. Produce private parser results carrying either `(line_number: int, fields: List[str])` or `ImportError`, in source order. Exact private parser signature and malformed-quote recovery outcomes must be written into this task after D1, before implementation. Use `csv` and `io` where suitable; verify chosen framing actually supports the promised recovery. Files: `csv_import.py`, `test_csv_import.py`. Acceptance: quoted commas and escaped quotes decode correctly; valid records retain starting line numbers; bad field counts and blank lines cannot disappear; invalid header fails before insertion. Verification: inline fixtures for quoted commas, escaped quotes, empty/header-only input, reordered/extra header columns, LF and CRLF, malformed quote followed by a valid record, and a quoted multiline field. Expected results for the last two remain an explicit D1 evidence gap. Reject a parser that uses naive comma splitting, numbers records instead of physical lines, silently skips blanks, or consumes later valid records contrary to the agreed policy.

- [ ] **T2 — Validate rows into inventory items (R4, R5).** No task prerequisite; first unblocked task. Consume the exact `_item_from_fields(fields: List[str]) -> Item` contract above; produce `Item` or the specified `ValueError`. Files: `csv_import.py`, `test_csv_import.py`. Acceptance: `['A','Bolt','003']` becomes `Item('A','Bolt',3)`; SKU/name are unchanged, including blank and whitespace values. Exactly three fields are required; an empty quantity is rejected separately from missing fields. Verification: table-driven unit tests accept `1`, `003`; reject `0`, `-1`, `+1`, `1.0`, `1e2`, spaces, empty, `null`, Unicode digits and wrong field counts. Assert error messages and output types/values. These tests reject permissive `float` conversion, truncation, accidental normalization and treating integer-looking Unicode text as ASCII quantities.

- [ ] **T3 — Integrate sequential import and report (R1–R5).** Prerequisites: T1 and T2, including D1 resolution. Consume T1's agreed parser results, `_item_from_fields` and the established `Inventory.add_item(self, item: Item) -> None`; produce `import_csv(inventory: Inventory, text: str) -> ImportReport` with the dataclasses above. Files: `csv_import.py`, `test_csv_import.py`. Acceptance: each valid row calls `add_item`; expected validation and duplicate failures append one error and allow subsequent valid rows; added count increases only after successful insertion. Verification: integration fixture with existing SKU `OLD`, valid `A`, invalid quantity, duplicate `A`, duplicate `OLD`, then valid `B`; expect 2 additions, exact error lines/reasons, preserved `OLD`, first `A` value and stored `B`. Add an invalid `X` followed by valid `X` to prove rejects do not reserve a SKU. Use a recording `Inventory` subclass to prove calls go through `add_item`; inject unexpected `RuntimeError` and assert propagation. Assert empty report for header-only input, header failure leaves inventory untouched, and all existing inventory tests still pass. These checks reject direct `_items` writes, pre-reserving SKUs, premature success counts, overwrites, early stop and broad exception swallowing. Include a module docstring with the final header/quantity/framing/report contract and example usage in this task.

## Verification and review focus

Planned command, derived from the existing `unittest` test module and standard discovery: `python3 -m unittest discover -v`. Run it with Python 3.9; first confirm `python3 --version`. No project-specific test runner configuration exists in the inspected fixture. Python 3.9 availability has not been checked. Future implementation evidence must include the interpreter version, command and result; none is claimed here.

| Requirement | Tasks | Check and expected evidence |
| --- | --- | --- |
| R1 parse and source lines | T1, T3 | Quoted CSV + LF/CRLF fixtures; exact physical line assertions; D1 cases pending |
| R2 insert all valid rows, continue | T1, T3 | Mixed-error fixture stores A/B, recording subclass sees valid insertion attempts; malformed syntax continuation pending D1 |
| R3 added count/rejections | T3 | Exact count 2, ordered line/reason list, no success entries |
| R4 quantity and uniqueness | T2, T3 | Syntax matrix and duplicate/preexisting/retry fixtures with unchanged original items |
| R5 Python 3.9 stdlib | T1–T3 | Python 3.9 test pass plus import/dependency diff inspection |

Review focus (owning checks): unmatched quote recovery and multiline framing (T1, blocked); blank/missing/empty fields (T1/T2); physical line versus record numbering (T1); a rejected SKU subsequently accepted (T3); swallowed internal exceptions (T3). These are not established by the existing green tests.

Dependencies are acyclic: D1 → T1; T1 + T2 → T3. No release or deployment is requested, so no release gates are defined. Existing direct callers remain compatible because `Inventory` is unchanged. Rollback of the code addition removes the new module; already imported in-memory items are not transactionally undone. Counts/errors supply caller-visible diagnostics; no new logging infrastructure is needed.

## Handoff

Resolve D1 and update T1's parser contract and exact expected outcomes before declaring the whole plan execution-ready. Then review the plan before requesting `panda-execute` implementation. Implementation was explicitly deferred; no execution mode is being selected and no application code has been changed.
