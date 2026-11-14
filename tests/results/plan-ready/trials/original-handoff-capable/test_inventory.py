import unittest

from inventory import Inventory, Item


class InventoryTest(unittest.TestCase):
    def test_add_and_get(self):
        inv = Inventory()
        inv.add_item(Item("A-1", "Bolt", 3))
        self.assertEqual(3, inv.get("A-1").quantity)

    def test_duplicate_sku_rejected(self):
        inv = Inventory()
        inv.add_item(Item("A-1", "Bolt", 3))
        with self.assertRaises(KeyError):
            inv.add_item(Item("A-1", "Nut", 1))


if __name__ == "__main__":
    unittest.main()
