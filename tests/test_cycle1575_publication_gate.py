import unittest
from quality.publication_gate import assess

class PublicationGateTests(unittest.TestCase):
    def test_missing_audio_blocks(self):
        result = assess({"video_decodes": True, "resolution_ok": True})
        self.assertFalse(result["posting_allowed"])
        self.assertIn("japanese_speech_verified", result["failed_checks"])

    def test_only_explicit_full_approval_passes(self):
        fields = ("video_decodes", "resolution_ok", "japanese_speech_verified",
                  "captions_synced_verified", "assets_approved",
                  "human_quality_approved")
        self.assertTrue(assess({key: True for key in fields})["posting_allowed"])

    def test_false_cannot_pass(self):
        self.assertFalse(assess({"japanese_speech_verified": False})["posting_allowed"])

if __name__ == "__main__":
    unittest.main()
