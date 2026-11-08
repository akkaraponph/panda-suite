import unittest
import work


class Contracts(unittest.TestCase):
    def test_ids(self):
        for values, expected in [([], []), ([3, 1, 3, -1, 1], [3, 1, -1]), ([0, 0], [0])]:
            self.assertEqual(expected, work.unique_ids(values))

    def test_ids_match_generic_and_leave_input_unchanged(self):
        import random
        rng = random.Random(42)
        for size in (0, 1, 10, 100, 1000):
            values = [rng.randrange(-100, 101) for _ in range(size)]
            original = values.copy()
            result = work.unique_ids(values)
            self.assertIsInstance(result, list)
            self.assertEqual(work.unique(values), result)
            self.assertEqual(original, values)
            self.assertIsNot(result, values)

    def test_ids_large_integers_and_iterator(self):
        values = [2**200, -2**200, 0, 2**200, -1, -1]
        self.assertEqual(work.unique(values), work.unique_ids(iter(values)))

    def test_generic(self):
        self.assertEqual([[1], [2]], work.unique([[1], [2], [1]]))
        self.assertEqual([{"x": 1}], work.unique([{"x": 1}, {"x": 1}]))

    def test_recent_is_bounded(self):
        work.RECENT.clear()
        for i in range(25):
            work.record_recent(i)
        self.assertEqual(list(range(15, 25)), list(work.RECENT))


if __name__ == "__main__":
    unittest.main()
