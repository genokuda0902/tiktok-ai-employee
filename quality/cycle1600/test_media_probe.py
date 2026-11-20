import unittest
from quality.cycle1600.media_probe import publication_allowed

class GateTests(unittest.TestCase):
    def test_empty_rejected(self):
        self.assertFalse(publication_allowed({}))
    def test_audio_presence_does_not_count_as_japanese(self):
        self.assertFalse(publication_allowed({"decode_ok": True, "audio_streams": 1}))
    def test_only_complete_verified_evidence_passes(self):
        keys = ("decode_ok", "japanese_narration_verified", "caption_sync_verified",
                "assets_approved", "privacy_approved", "employee_approved")
        evidence = dict.fromkeys(keys, True)
        self.assertTrue(publication_allowed(evidence))
        for key in keys:
            modified = dict(evidence)
            modified[key] = False
            self.assertFalse(publication_allowed(modified))

if __name__ == "__main__":
    unittest.main()
