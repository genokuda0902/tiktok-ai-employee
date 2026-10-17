"""Zero-dependency tests: python -m unittest discover -s video_engine/genre_v1 -p 'test_review_asset_gate.py'"""
import unittest
from review_asset_gate import GENRES, Asset, review_gate

class GateTests(unittest.TestCase):
    def test_ten_genres_share_gate(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            result = review_gate(genre, (Asset("storyboard", "user_library"),),
                                 {"japanese_narration": False})
            self.assertEqual(result["publication"], "NOT_APPROVED")
            self.assertEqual(result["posting_mode"], "MANUAL_ONLY")
    def test_rights_unknown_fail_closed(self):
        result = review_gate(GENRES[0], (Asset("ref-01", "user_storyboard"),),
                             {"japanese_narration": True,
                              "voice_caption_sync_verified": True, "human_approved": True})
        self.assertFalse(result["rights_approved"])
        self.assertEqual(result["publication"], "NOT_APPROVED")
    def test_missing_voice_blocks_even_with_rights(self):
        a = Asset("original", "local_original", True, True)
        result = review_gate(GENRES[0], (a,), {"japanese_narration": False,
                              "voice_caption_sync_verified": False, "human_approved": True})
        self.assertEqual(result["publication"], "NOT_APPROVED")
    def test_human_review_required(self):
        a = Asset("original", "local_original", True, True)
        result = review_gate(GENRES[0], (a,), {"japanese_narration": True,
                              "voice_caption_sync_verified": True})
        self.assertEqual(result["publication"], "NOT_APPROVED")
    def test_manual_only_even_when_approved(self):
        a = Asset("original", "local_original", True, True)
        result = review_gate(GENRES[0], (a,), {"japanese_narration": True,
                              "voice_caption_sync_verified": True, "human_approved": True})
        self.assertEqual(result["posting_mode"], "MANUAL_ONLY")
    def test_bad_assets_rejected(self):
        with self.assertRaises(ValueError):
            review_gate(GENRES[0], (), {})
        with self.assertRaises(ValueError):
            review_gate(GENRES[0], (Asset("a", ""),), {})
        with self.assertRaises(ValueError):
            review_gate(GENRES[0], (Asset("a", "local"), Asset("a", "local")), {})
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):
            review_gate("other", (Asset("a", "local"),), {})

if __name__ == "__main__":
    unittest.main()
