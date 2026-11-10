import unittest

from service import normalize_labels


class NormalizeLabelsTest(unittest.TestCase):
    def test_trim_and_lowercase(self):
        self.assertEqual(["alpha", "beta"], normalize_labels([" Alpha ", "BETA"]))

    def test_blank_labels(self):
        self.assertEqual([], normalize_labels(["", "  "]))

    def test_input_unchanged(self):
        values = [" B ", "A"]
        self.assertEqual(["b", "a"], normalize_labels(values))
        self.assertEqual([" B ", "A"], values)


if __name__ == "__main__":
    unittest.main()
