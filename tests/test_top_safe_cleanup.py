import unittest

from video_engine.top_safe_cleanup import ffmpeg_filter, release_contract


class TopSafeCleanupTests(unittest.TestCase):
    def test_filter_masks_only_bounded_top_strip(self):
        f = ffmpeg_filter()
        self.assertEqual(f, "drawbox=x=0:y=0:w=iw:h=105:color=white:t=fill")

    def test_wrong_geometry_or_excessive_mask_fails_closed(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(720, 1280)
        with self.assertRaises(ValueError):
            ffmpeg_filter(strip_height=200)

    def test_release_policy_remains_manual(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["preserve_caption_copy"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
