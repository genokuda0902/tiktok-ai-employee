import unittest
from src.review_checkpoint_rail import checkpoint_filter

class CheckpointTests(unittest.TestCase):
    def test_filter_has_timing_and_label(self):
        s=checkpoint_filter("/tmp/font.ttc")
        self.assertIn("between(t,1,5)",s)
        self.assertIn("目的 → 条件 → 確認",s)
    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            checkpoint_filter("/tmp/font.ttc",5,1)
    def test_unsafe_font(self):
        with self.assertRaises(ValueError):
            checkpoint_filter("/tmp/a'b.ttf")
if __name__=="__main__": unittest.main()
