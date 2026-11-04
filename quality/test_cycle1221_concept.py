import unittest
from cycle1221_concept import build_filter
class TestConcept(unittest.TestCase):
    def test_review_label(self):
        self.assertIn("実操作映像ではありません",build_filter())
    def test_time_window(self):
        self.assertIn("between(t,6,14)",build_filter())
    def test_before_after(self):
        self.assertIn("BEFORE",build_filter())
        self.assertIn("AFTER",build_filter())
if __name__=="__main__":
    unittest.main()
