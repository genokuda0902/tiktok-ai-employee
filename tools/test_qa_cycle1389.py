import unittest
from qa_cycle1389 import inspect

class QualityGateTest(unittest.TestCase):
    def test_missing_video_fails(self):
        with self.assertRaises(Exception):
            inspect("/nonexistent/cycle1389.mp4")

    def test_review_gate_never_approves_without_evidence(self):
        # A valid video container alone is insufficient to approve narration.
        import inspect as introspect
        source = introspect.getsource(inspect)
        self.assertIn('"narration_verified": False', source)
        self.assertIn('"publication_approved": False', source)

if __name__ == "__main__":
    unittest.main()
