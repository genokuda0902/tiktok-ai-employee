import unittest
from src.review_progress import progress_filter
class TestReviewProgress(unittest.TestCase):
    def test_bounded(self): self.assertIn("min(", progress_filter(12))
    def test_invalid_duration(self):
        with self.assertRaises(ValueError): progress_filter(0)
    def test_invalid_size(self):
        with self.assertRaises(ValueError): progress_filter(12,100,200)
if __name__=="__main__": unittest.main()
