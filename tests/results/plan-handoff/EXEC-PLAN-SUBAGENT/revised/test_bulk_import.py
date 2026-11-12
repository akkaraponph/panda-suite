import unittest

from bulk_import import HEADER_REASON, CsvRow, Rejection, RowError, import_csv, parse_csv, row_to_item
from inventory import Inventory, Item


class ParseCsvTest(unittest.TestCase):
    def test_rows_keep_line_numbers(self):
        parsed = parse_csv("sku,name,quantity\nA-1,Bolt,3\n\nB-2,Nut,5\n")
        self.assertEqual((CsvRow(2, ("A-1", "Bolt", "3")), CsvRow(4, ("B-2", "Nut", "5"))), parsed.rows)
        self.assertEqual((), parsed.rejected)

    def test_wrong_header(self):
        self.assertEqual((Rejection(1, HEADER_REASON),), parse_csv("sku,qty,name\nA-1,3,Bolt\n").rejected)

    def test_malformed_csv_rejects_whole_paste(self):
        parsed = parse_csv('sku,name,quantity\nA-1,Bolt,3\nB-2,"Nut,5\n')
        self.assertEqual((), parsed.rows)
        self.assertTrue(parsed.rejected[0].reason.startswith("malformed CSV: "))


class RowToItemTest(unittest.TestCase):
    def assertReason(self, fields, reason):
        with self.assertRaises(RowError) as ctx:
            row_to_item(CsvRow(2, fields))
        self.assertEqual(reason, str(ctx.exception))

    def test_valid_row(self):
        self.assertEqual(Item("A-1", "Bolt", 7), row_to_item(CsvRow(2, ("A-1", "Bolt", "007"))))

    def test_wrong_field_count(self):
        self.assertReason(("A-1", "Bolt"), "expected 3 fields, got 2")

    def test_empty_sku(self):
        self.assertReason(("", "Bolt", "3"), "sku is required")

    def test_empty_name(self):
        self.assertReason(("A-1", "", "3"), "name is required")

    def test_quantity_rejections(self):
        for value in ("0", "-1", "+5", "2.0", "", "\u0663"):
            with self.subTest(value=value):
                self.assertReason(("A-1", "Bolt", value), f"quantity must be a positive whole number, got {value!r}")


class ImportCsvTest(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()

    def test_all_valid(self):
        report = import_csv(self.inventory, "sku,name,quantity\nA-1,Bolt,3\nB-2,Nut,5\n")
        self.assertEqual(2, report.added)
        self.assertEqual((), report.rejected)
        self.assertEqual(Item("A-1", "Bolt", 3), self.inventory.get("A-1"))
        self.assertEqual(Item("B-2", "Nut", 5), self.inventory.get("B-2"))

    def test_bad_row_does_not_stop_later_rows(self):
        report = import_csv(self.inventory, "sku,name,quantity\nA-1,Bolt,3\nB-2,Nut,0\nC-3,Washer,4\n")
        self.assertEqual(2, report.added)
        self.assertEqual(1, len(report.rejected))
        self.assertEqual(3, report.rejected[0].line)
        self.assertEqual(Item("C-3", "Washer", 4), self.inventory.get("C-3"))

    def test_duplicate_within_paste(self):
        report = import_csv(self.inventory, "sku,name,quantity\nA-1,Bolt,3\nA-1,Other,9\n")
        self.assertEqual(1, report.added)
        self.assertEqual((Rejection(3, "duplicate sku: A-1"),), report.rejected)
        self.assertEqual(Item("A-1", "Bolt", 3), self.inventory.get("A-1"))

    def test_duplicate_of_existing_item(self):
        self.inventory.add_item(Item("A-1", "Bolt", 3))
        report = import_csv(self.inventory, "sku,name,quantity\nA-1,Other,9\nB-2,Nut,5\n")
        self.assertEqual(1, report.added)
        self.assertEqual((Rejection(2, "duplicate sku: A-1"),), report.rejected)
        self.assertEqual(Item("A-1", "Bolt", 3), self.inventory.get("A-1"))

    def test_bad_header_imports_nothing(self):
        report = import_csv(self.inventory, "sku,qty,name\nA-1,3,Bolt\n")
        self.assertEqual(0, report.added)
        self.assertEqual((Rejection(1, HEADER_REASON),), report.rejected)
        with self.assertRaises(KeyError):
            self.inventory.get("A-1")


if __name__ == "__main__":
    unittest.main()
