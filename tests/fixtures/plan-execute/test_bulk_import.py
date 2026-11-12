import unittest

from bulk_import import HEADER_REASON, CsvRow, Rejection, parse_csv


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


if __name__ == "__main__":
    unittest.main()
