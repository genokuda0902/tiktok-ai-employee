import unittest

from video_engine.caption_panel_compactor import compact_caption_filter, release_policy


class CaptionPanelCompactorTests(unittest.TestCase):
    def test_default_reduces_panel_and_uses_lanczos(self):
        f = compact_caption_filter()
        self.assertIn("crop=1080:180:0:1480", f)
        self.assertIn("scale=1080:140:flags=lanczos", f)
        self.assertIn("overlay=0:1500", f)

    def test_wrong_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            compact_caption_filter(720, 1280)

    def test_oversized_or_non_compacting_panel_fails_closed(self):
        with self.assertRaises(ValueError):
            compact_caption_filter(target_h=180)
        with self.assertRaises(ValueError):
            compact_caption_filter(target_h=200)

    def test_release_remains_manual_and_zero_cost(self):
        c = release_policy()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["preserve_caption_copy"])
        self.assertTrue(c["human_approval_required"])
        self.assertTrue(c["manual_post_only"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
