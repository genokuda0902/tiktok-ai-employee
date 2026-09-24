import unittest

from video_engine.focus_hold_motion import ffmpeg_filter, release_policy


class FocusHoldMotionTests(unittest.TestCase):
    def test_filter_is_bounded_portrait_motion(self):
        f = ffmpeg_filter()
        self.assertIn("scale=1092:1941:flags=lanczos", f)
        self.assertIn("crop=1080:1920", f)
        self.assertIn("sin(2*PI*t/4.2)", f)
        self.assertIn("cos(2*PI*t/5.1)", f)

    def test_wrong_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(720, 1280)

    def test_release_stays_manual_and_zero_cost(self):
        p = release_policy()
        self.assertTrue(p["zero_cost"])
        self.assertTrue(p["preserve_audio"])
        self.assertTrue(p["preserve_caption_copy"])
        self.assertTrue(p["human_approval_required"])
        self.assertTrue(p["manual_post_only"])
        self.assertFalse(p["auto_post"])


if __name__ == "__main__":
    unittest.main()
