import unittest

from video_engine.mobile_sharpness_finish import ffmpeg_filter, release_contract


class MobileSharpnessFinishTests(unittest.TestCase):
    def test_default_is_subtle_unsharp_only(self):
        self.assertEqual(ffmpeg_filter(), "unsharp=5:5:0.35:3:3:0.0")

    def test_wrong_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(720, 1280)

    def test_aggressive_sharpening_fails_closed(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(amount=0.8)

    def test_release_remains_manual_and_zero_cost(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["preserve_caption_copy"])
        self.assertTrue(c["human_approval_required"])
        self.assertTrue(c["manual_post_only"])
        self.assertFalse(c["auto_post"])
        self.assertFalse(c["reference_quality_claim_allowed_without_review"])


if __name__ == "__main__":
    unittest.main()
