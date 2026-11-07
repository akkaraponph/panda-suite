import unittest
from after import cancel

class CancelTest(unittest.TestCase):
    def test_owner_can_cancel_and_input_is_unchanged(self):
        order = {"id": 3, "owner_id": 1, "status": "pending"}
        result = cancel(order, 1)
        self.assertEqual(result, {**order, "status": "cancelled"})
        self.assertEqual(order["status"], "pending")

    def test_shipped_order_is_rejected(self):
        order = {"id": 3, "owner_id": 1, "status": "shipped"}
        with self.assertRaises(ValueError):
            cancel(order, 1)
        self.assertEqual(order["status"], "shipped")

    def test_non_owner_is_rejected(self):
        order = {"id": 3, "owner_id": 1, "status": "pending"}
        with self.assertRaises(PermissionError):
            cancel(order, 2)
        self.assertEqual(order["status"], "pending")

if __name__ == "__main__":
    unittest.main()
