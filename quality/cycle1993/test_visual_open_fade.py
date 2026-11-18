import unittest
from visual_open_fade import render
class TestFade(unittest.TestCase):
    def test_reject_too_long(self):
        with self.assertRaises(ValueError): render("a","b",1.0)
    def test_reject_negative(self):
        with self.assertRaises(ValueError): render("a","b",-0.1)
if __name__ == "__main__": unittest.main()
