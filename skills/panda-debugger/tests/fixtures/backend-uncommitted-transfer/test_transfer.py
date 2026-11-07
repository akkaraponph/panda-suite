import sqlite3
import tempfile
import unittest
from pathlib import Path

from transfer import transfer


class TransferTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.db_path = Path(self.directory.name) / "accounts.sqlite"
        with sqlite3.connect(self.db_path) as connection:
            connection.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER)")
            connection.executemany(
                "INSERT INTO accounts (id, balance) VALUES (?, ?)",
                [(1, 100), (2, 20)],
            )

    def balances(self):
        with sqlite3.connect(self.db_path) as connection:
            return [
                row[0]
                for row in connection.execute("SELECT balance FROM accounts ORDER BY id")
            ]

    def test_success_persists_both_balances(self):
        self.assertIsNone(transfer(self.db_path, 1, 2, 25))
        self.assertEqual([75, 45], self.balances())

    def test_invalid_amount_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "amount must be positive"):
            transfer(self.db_path, 1, 2, 0)
        self.assertEqual([100, 20], self.balances())


if __name__ == "__main__":
    unittest.main()
