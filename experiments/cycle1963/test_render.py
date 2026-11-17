import unittest
from render import render
class FadeTests(unittest.TestCase):
    def test_zero(self):
        with self.assertRaises(ValueError): render("x","y",1,0)
    def test_too_long(self):
        with self.assertRaises(ValueError): render("x","y",1,2)
