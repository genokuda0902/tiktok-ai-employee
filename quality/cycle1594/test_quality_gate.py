import unittest
from quality_gate import evaluate

class GateTest(unittest.TestCase):
    def test_empty_rejected(self):
        self.assertFalse(evaluate({})["approved"])
    def test_silent_video_rejected(self):
        evidence = dict.fromkeys(("video_decodes","caption_sync_verified","assets_licensed","privacy_reviewed","employee_approved"), True)
        self.assertIn("japanese_narration_verified", evaluate(evidence)["missing"])
    def test_all_required(self):
        evidence = dict.fromkeys(("video_decodes","japanese_narration_verified","caption_sync_verified","assets_licensed","privacy_reviewed","employee_approved"), True)
        self.assertTrue(evaluate(evidence)["approved"])
if __name__ == "__main__":
    unittest.main()
