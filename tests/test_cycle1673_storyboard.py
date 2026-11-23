import unittest
from src.quality.storyboard_contract import Scene, validate

class TestStoryboard(unittest.TestCase):
    def test_review_fails_closed(self):
        self.assertEqual(validate([Scene(0, 3, "日本語字幕")], 3), ["japanese_narration_unverified", "publication_not_approved"])
    def test_overlapping_scenes_rejected(self):
        self.assertIn("overlap_or_disorder:1", validate([Scene(0,3,"A"),Scene(2,5,"B")],5))
    def test_long_caption_rejected(self):
        self.assertIn("long_caption:0", validate([Scene(0,3,"あ"*36)],3))
    def test_approved_contract_only(self):
        self.assertEqual(validate([Scene(0,3,"短い字幕")],3,japanese_audio_verified=True,human_approved=True), [])

if __name__ == "__main__": unittest.main()
