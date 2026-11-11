import unittest
from quality.cycle1374_gate import publication_ready

class GateTests(unittest.TestCase):
    def test_missing_is_rejected(self):
        self.assertFalse(publication_ready({}))
    def test_effect_only_audio_rejected(self):
        self.assertFalse(publication_ready({"narration_verified": False, "captions_synced": True, "approved": True}))
    def test_unapproved_rejected(self):
        self.assertFalse(publication_ready({"narration_verified": True, "captions_synced": True, "approved": False}))
    def test_all_verified(self):
        self.assertTrue(publication_ready({"narration_verified": True, "captions_synced": True, "approved": True}))
if __name__ == "__main__":
    unittest.main()
