import unittest
from src.caption_contrast import filtergraph
class TestCaptionContrast(unittest.TestCase):
    def test_backdrop(self): self.assertIn("black@0.72",filtergraph())
    def test_safe_area(self): self.assertIn("y=1400",filtergraph())
    def test_timing(self): self.assertIn("between(t,17,20)",filtergraph())
    def test_reject_unsafe(self):
        with self.assertRaises(ValueError): filtergraph("unsafe:'")
