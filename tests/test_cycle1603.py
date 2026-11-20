import unittest
from quality.cycle1603_scene_contract import SCENES, Scene, validate, publication_allowed

class TestCycle1603(unittest.TestCase):
    def test_scene_timeline(self): self.assertTrue(validate())
    def test_gap_rejected(self):
        broken = (SCENES[0], Scene(2.6, 5, "x", "y"), *SCENES[2:])
        with self.assertRaises(ValueError): validate(broken)
    def test_review_video_not_publishable(self):
        self.assertFalse(publication_allowed())
        self.assertFalse(publication_allowed(japanese_narration_verified=True))
    def test_all_approvals_required(self):
        self.assertTrue(publication_allowed(japanese_narration_verified=True,
            speech_caption_sync_verified=True, asset_rights_approved=True,
            privacy_approved=True, employee_approved=True))

if __name__ == "__main__": unittest.main()
