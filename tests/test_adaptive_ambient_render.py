import unittest

from video_engine.adaptive_ambient_render import ffmpeg_filter, release_contract


class AdaptiveAmbientRenderTests(unittest.TestCase):
    def test_filter_ducks_synthesized_bed_under_narration(self):
        f = ffmpeg_filter(12.7)
        self.assertIn("highpass=f=180", f)
        self.assertIn("lowpass=f=1800", f)
        self.assertIn("sidechaincompress", f)
        self.assertIn("loudnorm=I=-16:TP=-1.5:LRA=7", f)

    def test_wrong_geometry_and_duration_fail_closed(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(12.7, 720, 1280)
        with self.assertRaises(ValueError):
            ffmpeg_filter(0)

    def test_release_remains_manual_and_zero_cost(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["synthesized_bed_only"])
        self.assertTrue(c["preserve_video_and_burned_captions"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertEqual((c["audio_rate"], c["audio_channels"]), (48000, 2))


if __name__ == "__main__":
    unittest.main()
