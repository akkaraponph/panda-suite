import unittest
from consumer import welcome

class GreetingTest(unittest.TestCase):
    def test_admin(self):
        self.assertEqual("Hello, Ada", welcome({"role": "admin"}, "Ada"))
    def test_denied(self):
        with self.assertRaisesRegex(PermissionError, "admin required"):
            welcome({"role": "member"}, "Ada")
