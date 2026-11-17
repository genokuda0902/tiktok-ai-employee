import unittest
from tools.soft_visual_intro import render
class TestIntro(unittest.TestCase):
    def test_zero_rejected(self):
        with self.assertRaises(ValueError): render('x','y',0)
    def test_long_rejected(self):
        with self.assertRaises(ValueError): render('x','y',2)
