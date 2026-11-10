import unittest
from service import label

class LabelTest(unittest.TestCase):
    def test_label(self):
        self.assertEqual("7: ready", label({"id": 7, "status": "ready"}))
