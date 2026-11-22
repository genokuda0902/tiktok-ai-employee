import unittest
from src.review_caption_safearea import review_gate

class TestReviewGate(unittest.TestCase):
    def test_silent_video_rejected(self):
        data = dict(width=1080, height=1920, fps=24,
                    caption_safe_area_checked=True, assets_approved=True,
                    employee_approved=True, speech_caption_sync_verified=True)
        self.assertIn("japanese_narration_unverified", review_gate(data)["issues"])
    def test_missing_safe_area_rejected(self):
        self.assertIn("caption_safe_area_unverified", review_gate({})["issues"])
    def test_fully_verified_metadata_only(self):
        data = dict(width=1080, height=1920, fps=24,
                    caption_safe_area_checked=True, assets_approved=True,
                    employee_approved=True, japanese_narration_verified=True,
                    speech_caption_sync_verified=True)
        self.assertTrue(review_gate(data)["publication_approved"])

if __name__ == "__main__":
    unittest.main()
