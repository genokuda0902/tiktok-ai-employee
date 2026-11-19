import unittest
from readable_takeaways import TAKEAWAYS, render

class TestTakeaways(unittest.TestCase):
    def test_five_parts(self):
        self.assertEqual(len(TAKEAWAYS), 5)
    def test_reject_wrong_count(self):
        with self.assertRaises(ValueError):
            render("source.mp4", "out.mp4", "/font.ttf", ["one"])
    def test_reject_unsafe_text(self):
        with self.assertRaises(ValueError):
            render("source.mp4", "out.mp4", "/font.ttf", ["bad:text"] * 5)
