import unittest
from render import render
class TestRender(unittest.TestCase):
    def test_bad_window(self):
        with self.assertRaises(ValueError):render('x',['a'],'o',[(2,1)])
    def test_overlap(self):
        with self.assertRaises(ValueError):render('x',['a','b'],'o',[(1,2),(1.5,3)])
    def test_count(self):
        with self.assertRaises(ValueError):render('x',['a'],'o',[(1,2),(2,3)])
if __name__=='__main__':unittest.main()
