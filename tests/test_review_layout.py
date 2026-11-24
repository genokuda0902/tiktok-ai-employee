import unittest
from src.review_layout import validate_layout, validate_timeline
class ReviewLayoutTest(unittest.TestCase):
    def test_valid(self):
        validate_layout([(80,140,900,200)])
        validate_timeline([0,1,2],2)
    def test_overflow(self):
        with self.assertRaises(ValueError): validate_layout([(80,140,950,200)])
    def test_timeline(self):
        with self.assertRaises(ValueError): validate_timeline([0,1,1],2)
