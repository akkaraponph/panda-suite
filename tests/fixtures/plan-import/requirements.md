# Bulk CSV import

Operations staff paste CSV text with the header `sku,name,quantity` to add many
items at once.

1. Parse the CSV text into rows that keep their source line numbers.
2. Import every valid row through the existing `Inventory.add_item`; one bad row
   must not stop the remaining rows.
3. Return a report listing how many rows were added and, for each rejected row,
   its line number and a human-readable reason.
4. Quantity must be a positive whole number. SKUs stay unique.
5. Python 3.9 standard library only; no new dependencies.

Out of scope: file upload, HTTP endpoints, persistence.
