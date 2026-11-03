import unittest
from render_upper_detail import filtergraph

class TestUpperDetail(unittest.TestCase):
    def test_preserves_bottom_570_pixels(self):
        graph = filtergraph()
        self.assertIn("crop=1080:570:0:1350",graph)
        self.assertIn("vstack=inputs=2",graph)
    def test_no_negative_region(self):
        with self.assertRaises(ValueError): filtergraph(safe_bottom=1920)
    def test_no_excess_sharpen(self):
        with self.assertRaises(ValueError): filtergraph(amount=2)

if __name__ == "__main__": unittest.main()
