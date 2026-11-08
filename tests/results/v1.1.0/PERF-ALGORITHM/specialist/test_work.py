import unittest
import work


class Contracts(unittest.TestCase):
    def test_ids(self):
        for values, expected in [([], []), ([3, 1, 3, -1, 1], [3, 1, -1]), ([0, 0], [0])]:
            self.assertEqual(expected, work.unique_ids(values))

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
