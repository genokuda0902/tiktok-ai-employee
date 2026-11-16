import unittest
from deband import render
class TestDeband(unittest.TestCase):
    def test_reject_high(self):
        with self.assertRaises(ValueError): render("x","y",0.1)
    def test_reject_low(self):
        with self.assertRaises(ValueError): render("x","y",0)
    def test_missing_input(self):
        with self.assertRaises(Exception): render("/not-found.mp4","/tmp/out.mp4")
if __name__=="__main__": unittest.main()
