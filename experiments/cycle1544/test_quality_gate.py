import unittest
from quality_gate import approved
class QualityGateTests(unittest.TestCase):
    def test_missing_narration_rejected(self):
        self.assertFalse(approved({"video": True, "audio": True, "japanese_narration_verified": False}))
    def test_missing_human_approval_rejected(self):
        self.assertFalse(approved({"video": True, "audio": True, "japanese_narration_verified": True, "caption_sync_verified": True, "asset_rights_verified": True}))
    def test_complete_evidence(self):
        self.assertTrue(approved({"video": True, "audio": True, "japanese_narration_verified": True, "caption_sync_verified": True, "asset_rights_verified": True, "human_approved": True}))
if __name__ == "__main__": unittest.main()
