import unittest
from pathlib import Path
from footer_readability import render

class FooterTest(unittest.TestCase):
    def test_reusable_function(self):
        self.assertTrue(callable(render))
    def test_source_independent(self):
        self.assertEqual(render.__code__.co_argcount, 3)
if __name__ == "__main__": unittest.main()
