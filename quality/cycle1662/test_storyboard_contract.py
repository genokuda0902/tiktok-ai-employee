import unittest
from storyboard_contract import Scene, DEMO, validate_storyboard

class StoryboardTest(unittest.TestCase):
    def test_review_video_blocked(self):
        self.assertFalse(validate_storyboard(DEMO)["publication_approved"])
    def test_long_caption_blocked(self):
        self.assertIn("scene_0_text_overflow", validate_storyboard([Scene("a"*25,"x",4)])["issues"])
    def test_invalid_duration_blocked(self):
        self.assertIn("scene_0_duration", validate_storyboard([Scene("ok","x",9)])["issues"])
    def test_complete_contract(self):
        self.assertTrue(validate_storyboard(DEMO,narration_verified=True,rights_approved=True,employee_approved=True)["publication_approved"])

if __name__ == "__main__":
    unittest.main()
