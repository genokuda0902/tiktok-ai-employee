import unittest

from video_engine.delivery_master import delivery_contract, ffmpeg_args


class DeliveryMasterTests(unittest.TestCase):
    def test_portrait_contract_and_safety(self):
        c = delivery_contract()
        self.assertEqual((c["width"], c["height"], c["fps"]), (1080, 1920, 30))
        self.assertEqual(c["video_codec"], "libx264")
        self.assertEqual(c["crf"], 15)
        self.assertEqual(c["pixel_format"], "yuv420p")
        self.assertEqual(c["audio_rate"], 48000)
        self.assertEqual(c["audio_channels"], 2)
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertFalse(c["changes_audio_copy"])
        self.assertFalse(c["changes_caption_copy"])

    def test_fail_closed_for_wrong_geometry_or_fps(self):
        with self.assertRaises(ValueError):
            delivery_contract(720, 1280)
        with self.assertRaises(ValueError):
            delivery_contract(fps=24)

    def test_faststart_and_high_profile_are_explicit(self):
        args = ffmpeg_args()
        self.assertIn("+faststart", args)
        self.assertIn("high", args)
        self.assertIn("192k", args)


if __name__ == "__main__":
    unittest.main()
