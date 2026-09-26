import unittest
from video_engine.semantic_beat_punch import BeatPunch, ffmpeg_scale_expr, posting_policy


class SemanticBeatPunchTests(unittest.TestCase):
    def test_builds_bounded_expression(self):
        expr = ffmpeg_scale_expr([BeatPunch(0.0), BeatPunch(2.0, scale=1.02)], 12.7)
        self.assertIn("between(t,0.000,0.180)", expr)
        self.assertIn("0.0200", expr)

    def test_rejects_over_scale(self):
        with self.assertRaises(ValueError):
            ffmpeg_scale_expr([BeatPunch(1.0, scale=1.03)], 12.7)

    def test_rejects_unordered(self):
        with self.assertRaises(ValueError):
            ffmpeg_scale_expr([BeatPunch(2.0), BeatPunch(1.0)], 12.7)

    def test_manual_post_only(self):
        policy = posting_policy()
        self.assertTrue(policy["zero_cost"])
        self.assertTrue(policy["human_approval_required"])
        self.assertFalse(policy["auto_post"])


if __name__ == "__main__":
    unittest.main()
