import unittest

class UnrelatedTest(unittest.TestCase):
    def test_deployment_setting(self):
        self.assertEqual("legacy", "new", "known unrelated environment mismatch")
