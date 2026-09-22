import unittest

from image_slide_motion import MOTION_PROFILES, motion_filter


class ImageSlideMotionTests(unittest.TestCase):
    def test_profiles_are_reusable(self):
        self.assertGreaterEqual(len(MOTION_PROFILES), 4)
        for i in range(12):
            value = motion_filter(i)
            self.assertIn("crop=1080:1920", value)
            self.assertIn("scale=", value)

    def test_fail_closed_for_non_portrait_target(self):
        with self.assertRaises(ValueError):
            motion_filter(0, 720, 1280)


if __name__ == "__main__":
    unittest.main()
