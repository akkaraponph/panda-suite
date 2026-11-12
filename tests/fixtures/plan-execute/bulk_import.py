"""Bulk CSV import built on Inventory.add_item."""

import csv
import io
from dataclasses import dataclass
from typing import Tuple

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
