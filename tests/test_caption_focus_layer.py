import unittest
from video_engine.caption_focus_layer import caption_focus_filter, release_contract

class CaptionFocusLayerTests(unittest.TestCase):
    def test_default_filter_is_subtle_and_portrait(self):
        f = caption_focus_filter()
        self.assertIn("1080", f)
        self.assertIn("black@0.18", f)

    def test_wrong_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            caption_focus_filter(720, 1280)

    def test_aggressive_opacity_fails_closed(self):
        with self.assertRaises(ValueError):
            caption_focus_filter(opacity=0.30)

    def test_release_stays_manual_zero_cost(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["human_approval_required"])
        self.assertTrue(c["manual_post_only"])
        self.assertFalse(c["auto_post"])

if __name__ == "__main__":
    unittest.main()
