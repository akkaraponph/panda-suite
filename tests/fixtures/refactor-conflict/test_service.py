import unittest
from service import normalize_labels

class LabelTest(unittest.TestCase):
    def test_unique(self):
        self.assertEqual(["a", "b"], normalize_labels([" A ", "", "B"]))
