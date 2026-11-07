import unittest

from slug import slugify


class SlugTest(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual("hello-world", slugify("Hello, World!"))

    def test_accents(self):
        self.assertEqual("cafe-deja-vu", slugify("Café déjà vu"))

    def test_empty(self):
        self.assertEqual("", slugify(" --- "))

    def test_separators(self):
        self.assertEqual("a-b-c", slugify(" A___B   C "))

    def test_unicode_non_alphanumeric_separates_words(self):
        self.assertEqual("a-b", slugify("a💰b"))
        self.assertEqual("a-b", slugify("a—b"))
