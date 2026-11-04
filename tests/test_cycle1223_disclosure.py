import unittest
from quality.cycle1223_disclosure import filtergraph

class DisclosureTests(unittest.TestCase):
    def test_timing(self):
        self.assertIn("between(t,6.0,14.0)", filtergraph())
    def test_message(self):
        self.assertIn("実際の操作映像ではありません", filtergraph())
    def test_invalid_window(self):
        with self.assertRaises(ValueError):
            filtergraph(14, 6)
