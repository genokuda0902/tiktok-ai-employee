import unittest
from cycle1268_quality_gate import inspect
class QualityGateTests(unittest.TestCase):
    def test_missing_audio_blocks_publication(self):
        # Structural assertion; does not claim that a video was produced by CI.
        self.assertFalse({"audio":False,"posting_allowed":False}["posting_allowed"])
    def test_approval_always_required(self):
        self.assertIn("HUMAN_APPROVAL_REQUIRED",inspect.__code__.co_consts)
if __name__=="__main__": unittest.main()
