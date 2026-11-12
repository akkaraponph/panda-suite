"""Bulk CSV import built on Inventory.add_item."""

import csv
import io
import re
from dataclasses import dataclass
from typing import Tuple

from inventory import Inventory, Item

HEADER = ("sku", "name", "quantity")
HEADER_REASON = "missing or invalid header: expected sku,name,quantity"


@dataclass(frozen=True)
class Rejection:
    line: int
    reason: str


@dataclass(frozen=True)
class CsvRow:
    line: int
    fields: Tuple[str, ...]


@dataclass(frozen=True)
class ParsedCsv:
    rows: Tuple[CsvRow, ...]
    rejected: Tuple[Rejection, ...]


def parse_csv(text: str) -> ParsedCsv:
    reader = csv.reader(io.StringIO(text), strict=True)
    rows = []
    header_seen = False
    while True:
        start = reader.line_num + 1
        try:
            record = next(reader)
        except StopIteration:
            break
        except csv.Error as err:
            return ParsedCsv((), (Rejection(start, "malformed CSV: " + str(err)),))
        if not record:
            continue
        fields = tuple(f.strip() for f in record)
        if not header_seen:
            if fields != HEADER:
                return ParsedCsv((), (Rejection(start, HEADER_REASON),))
            header_seen = True
            continue
        rows.append(CsvRow(start, fields))
    if not header_seen:
        return ParsedCsv((), (Rejection(1, HEADER_REASON),))
    return ParsedCsv(tuple(rows), ())


class RowError(ValueError):
    pass


def row_to_item(row: CsvRow) -> Item:
    fields = row.fields
    if len(fields) != 3:
        raise RowError(f"expected 3 fields, got {len(fields)}")
    sku, name, value = fields
    if not sku:
        raise RowError("sku is required")
    if not name:
        raise RowError("name is required")
    if not re.fullmatch(r"[0-9]+", value) or int(value) <= 0:
        raise RowError(f"quantity must be a positive whole number, got {value!r}")
    return Item(sku, name, int(value))


@dataclass(frozen=True)
class ImportReport:
    added: int
    rejected: Tuple[Rejection, ...]


def import_csv(inventory: Inventory, text: str) -> ImportReport:
    parsed = parse_csv(text)
    rejected = list(parsed.rejected)
    added = 0
    for row in parsed.rows:
        try:
            item = row_to_item(row)
        except RowError as err:
            rejected.append(Rejection(row.line, str(err)))
            continue
        try:
            inventory.add_item(item)
        except KeyError:
            rejected.append(Rejection(row.line, f"duplicate sku: {item.sku}"))
            continue
        added += 1
    return ImportReport(added, tuple(sorted(rejected, key=lambda r: r.line)))
