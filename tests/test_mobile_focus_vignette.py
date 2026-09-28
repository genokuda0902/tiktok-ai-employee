import unittest

from video_engine.mobile_focus_vignette import ffmpeg_filter, safety_contract


class MobileFocusVignetteTests(unittest.TestCase):
    def test_filter_is_subtle_and_deterministic(self):
        value = ffmpeg_filter()
        self.assertIn("vignette=", value)
        self.assertIn("eval=frame", value)

    def test_strength_is_bounded(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(strength=0.13)
        with self.assertRaises(ValueError):
            ffmpeg_filter(strength=0.03)

    def test_portrait_geometry_is_required(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(720, 1280)

    def test_release_policy_stays_manual(self):
        c = safety_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["preserve_caption_copy"])
        self.assertTrue(c["preserve_timing"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
