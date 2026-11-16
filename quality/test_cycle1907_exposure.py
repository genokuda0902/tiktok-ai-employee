import unittest
from cycle1907_exposure import render
class TestExposure(unittest.TestCase):
    def test_low_gamma_rejected(self):
        with self.assertRaises(ValueError): render("a","b",0.9)
    def test_high_gamma_rejected(self):
        with self.assertRaises(ValueError): render("a","b",1.2)
if __name__ == "__main__": unittest.main()
