import unittest
from quality_gate_cycle2205 import inspect
class QualityGateTests(unittest.TestCase):
    def test_missing_video_rejected(self):
        with self.assertRaises(Exception):
            inspect("/nonexistent-cycle2205.mp4")
if __name__=="__main__":
    unittest.main()
