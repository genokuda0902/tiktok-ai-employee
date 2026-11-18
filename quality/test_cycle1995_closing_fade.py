import unittest
from cycle1995_closing_fade import render
class TestFade(unittest.TestCase):
 def test_invalid_fade(self):
  with self.assertRaises(ValueError): render('a','b',0)
 def test_excessive_fade(self):
  with self.assertRaises(ValueError): render('a','b',0.6)
