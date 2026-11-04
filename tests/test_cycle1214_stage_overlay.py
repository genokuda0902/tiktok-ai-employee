import unittest
from src.cycle1214_stage_overlay import stage_filter
class StageOverlayTest(unittest.TestCase):
    def test_labels(self):
        for label in ["01 目的","02 条件","03 確認"]:
            self.assertIn(label,stage_filter())
    def test_intervals(self):
        self.assertEqual(stage_filter().count("between(t"),6)
    def test_safe_position(self):
        self.assertIn("y=1260",stage_filter())
if __name__=="__main__": unittest.main()
