import unittest
from quality_gate import approve

class GateTests(unittest.TestCase):
    def test_empty_is_blocked(self):
        self.assertFalse(approve({}))
    def test_audio_alone_is_not_enough(self):
        self.assertFalse(approve({"japanese_narration_verified": True}))
    def test_all_checks_required(self):
        keys = ("japanese_narration_verified", "spoken_caption_sync_verified",
                "assets_rights_approved", "privacy_review_approved",
                "employee_approved", "manual_post_only")
        self.assertTrue(approve({k: True for k in keys}))
        for missing in keys:
            data = {k: True for k in keys}
            data[missing] = False
            self.assertFalse(approve(data))
if __name__ == "__main__":
    unittest.main()
