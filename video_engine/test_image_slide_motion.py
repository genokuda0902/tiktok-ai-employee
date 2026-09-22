import unittest

from image_slide_motion import (
    MOTION_PROFILES,
    interaction_filter,
    interactive_motion_filter,
    motion_filter,
)


class ImageSlideMotionTests(unittest.TestCase):
    def test_profiles_are_reusable(self):
        self.assertGreaterEqual(len(MOTION_PROFILES), 4)
        for i in range(12):
            value = motion_filter(i)
            self.assertIn("crop=1080:1920", value)
            self.assertIn("scale=", value)

    def test_interaction_filter_has_cursor_and_click_pulse(self):
        value = interaction_filter()
        self.assertIn("drawbox=", value)
        self.assertIn("enable=", value)
        self.assertIn("mod(t,2.5)", value)

    def test_combined_filter_keeps_camera_and_interaction_motion(self):
        value = interactive_motion_filter(2)
        self.assertIn("crop=1080:1920", value)
        self.assertGreaterEqual(value.count("drawbox="), 2)

    def test_fail_closed_for_non_portrait_target(self):
        with self.assertRaises(ValueError):
            motion_filter(0, 720, 1280)
        with self.assertRaises(ValueError):
            interaction_filter(720, 1280)
        with self.assertRaises(ValueError):
            interactive_motion_filter(0, 720, 1280)


if __name__ == "__main__":
    unittest.main()
