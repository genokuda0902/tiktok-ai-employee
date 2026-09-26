import unittest

from video_engine.audio_master_timeline import audio_master_timeline, ffmpeg_tail_hold_filter


class AudioMasterTimelineTest(unittest.TestCase):
    def test_pads_short_video_to_audio(self):
        result = audio_master_timeline(12.700, 11.867)
        self.assertAlmostEqual(result.pad_duration, 0.833, places=3)
        self.assertAlmostEqual(result.video_duration, 12.700, places=3)
        self.assertAlmostEqual(result.drift, 0.0, places=3)

    def test_does_not_pad_within_tolerance(self):
        result = audio_master_timeline(12.700, 12.680, tolerance=0.04)
        self.assertEqual(result.pad_duration, 0.0)

    def test_rejects_invalid_duration(self):
        with self.assertRaises(ValueError):
            audio_master_timeline(0, 12.0)

    def test_ffmpeg_tail_hold(self):
        self.assertEqual(ffmpeg_tail_hold_filter(0.833), "tpad=stop_mode=clone:stop_duration=0.833")


if __name__ == "__main__":
    unittest.main()
