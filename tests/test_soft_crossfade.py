import unittest

from video_engine.soft_crossfade import crossfade_contract, xfade_filter


class SoftCrossfadeTests(unittest.TestCase):
    def test_default_is_short_and_portrait(self):
        c = crossfade_contract()
        self.assertEqual((c["width"], c["height"]), (1080, 1920))
        self.assertEqual(c["transition"], "fade")
        self.assertLessEqual(c["duration_seconds"], 0.18)

    def test_aggressive_transition_fails_closed(self):
        with self.assertRaises(ValueError):
            crossfade_contract(duration=0.30)
        with self.assertRaises(ValueError):
            crossfade_contract(720, 1280)

    def test_filter_is_deterministic(self):
        self.assertEqual(
            xfade_filter(1.08),
            "xfade=transition=fade:duration=0.120:offset=1.080",
        )

    def test_release_policy_stays_manual(self):
        c = crossfade_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_narration"])
        self.assertTrue(c["preserve_caption_copy"])
        self.assertTrue(c["human_approval_required"])
        self.assertTrue(c["manual_post_only"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
