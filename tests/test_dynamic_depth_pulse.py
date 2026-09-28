import unittest
from video_engine.dynamic_depth_pulse import ffmpeg_filter


class DynamicDepthPulseTests(unittest.TestCase):
    def test_default_filter_is_time_varying_eq(self):
        value = ffmpeg_filter()
        self.assertIn("eq=", value)
        self.assertIn("sin(2*PI*t", value)

    def test_rejects_excessive_contrast(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(contrast_amount=0.051)

    def test_rejects_excessive_brightness(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(brightness_amount=0.016)


if __name__ == "__main__":
    unittest.main()
