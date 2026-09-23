import unittest

from video_engine.micro_parallax import MicroParallaxProfile, require_human_approval


class MicroParallaxTests(unittest.TestCase):
    def test_default_profile_is_vertical_full_hd(self):
        p = MicroParallaxProfile()
        p.validate()
        self.assertEqual((p.width, p.height), (1080, 1920))

    def test_filter_uses_lanczos_and_crop(self):
        f = MicroParallaxProfile().ffmpeg_filter()
        self.assertIn("flags=lanczos", f)
        self.assertIn("crop=1080:1920", f)

    def test_excess_motion_fails_closed(self):
        with self.assertRaises(ValueError):
            MicroParallaxProfile(x_amplitude_px=20).validate()

    def test_human_approval_required(self):
        with self.assertRaises(PermissionError):
            require_human_approval(False)


if __name__ == "__main__":
    unittest.main()
