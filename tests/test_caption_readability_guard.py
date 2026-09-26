import unittest
from video_engine.caption_readability_guard import CaptionGuard, posting_policy

class CaptionReadabilityGuardTest(unittest.TestCase):
    def test_default_is_subtle_and_inside_frame(self):
        guard = CaptionGuard()
        guard.validate()
        self.assertLessEqual(guard.opacity, 0.14)
        self.assertLessEqual(guard.y + guard.height, 1920)
        self.assertIn("drawbox", guard.ffmpeg_filter())

    def test_rejects_overdark_guard(self):
        with self.assertRaises(ValueError):
            CaptionGuard(opacity=0.20).validate()

    def test_manual_posting_only(self):
        policy = posting_policy()
        self.assertTrue(policy["human_approval_required"])
        self.assertFalse(policy["auto_post"])
        self.assertTrue(policy["zero_cost"])

if __name__ == "__main__":
    unittest.main()
