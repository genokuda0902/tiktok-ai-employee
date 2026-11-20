import unittest
from quality_gate import REQUIRED, evaluate
class QualityGateTests(unittest.TestCase):
    def test_all_required(self):
        self.assertTrue(evaluate({k: True for k in REQUIRED})["publication_ready"])
        for k in REQUIRED:
            evidence = {x: True for x in REQUIRED}
            evidence[k] = False
            self.assertFalse(evaluate(evidence)["publication_ready"])
    def test_missing_evidence_fails(self):
        self.assertFalse(evaluate({})["publication_ready"])
    def test_audio_track_alone_not_speech(self):
        e = {k: True for k in REQUIRED}
        e["japanese_speech_verified"] = False
        self.assertIn("japanese_speech_verified", evaluate(e)["missing"])
if __name__ == "__main__": unittest.main()
