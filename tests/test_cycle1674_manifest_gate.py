import unittest
from quality.cycle1674_manifest_gate import validate

class TestManifestGate(unittest.TestCase):
    def test_missing_fields_block(self):
        self.assertFalse(validate({})["posting_allowed"])
    def test_silent_video_block(self):
        m = dict(publication_approved=True,asset_rights_approved=True,privacy_checked=True,japanese_narration_verified=False,captions_synced=True,video_decode_passed=True,width=1080,height=1920)
        self.assertIn("Japanese narration unverified", validate(m)["errors"])
    def test_all_verified(self):
        m = dict(publication_approved=True,asset_rights_approved=True,privacy_checked=True,japanese_narration_verified=True,captions_synced=True,video_decode_passed=True,width=1080,height=1920)
        self.assertTrue(validate(m)["posting_allowed"])

if __name__ == "__main__":
    unittest.main()
