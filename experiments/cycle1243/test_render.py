import unittest
from render import validate
class TestTimeline(unittest.TestCase):
    def test_valid(self): validate([(0,4,"a"),(4,10,"b"),(10,15,"c")],15)
    def test_gap(self):
        with self.assertRaises(ValueError): validate([(0,4,"a"),(5,15,"b")],15)
    def test_empty(self):
        with self.assertRaises(ValueError): validate([],15)
    def test_missing_label(self):
        with self.assertRaises(ValueError): validate([(0,15,"")],15)
if __name__=="__main__": unittest.main()
