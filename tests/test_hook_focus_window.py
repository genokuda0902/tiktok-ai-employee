import unittest
from video_engine.hook_focus_window import ffmpeg_filter, output_contract


class HookFocusWindowTests(unittest.TestCase):
    def test_default_is_first_second_only_and_subtle(self):
        f = ffmpeg_filter()
        self.assertIn("between(t,0,1.6)", f)
        self.assertIn("contrast=1.035", f)
        self.assertIn("brightness=0.008", f)

    def test_aggressive_or_long_hook_fails_closed(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(window_s=3.0)
        with self.assertRaises(ValueError):
            ffmpeg_filter(contrast=1.2)

    def test_manual_release_contract(self):
        c = output_contract()
        self.assertEqual((c["width"], c["height"]), (1080, 1920))
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["preserve_caption_copy"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
