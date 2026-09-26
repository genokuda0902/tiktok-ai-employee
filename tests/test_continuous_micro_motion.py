import unittest

from video_engine.continuous_micro_motion import micro_motion_filter, safety_contract


class ContinuousMicroMotionTests(unittest.TestCase):
    def test_filter_uses_overscan_and_dynamic_crop(self):
        f = micro_motion_filter()
        self.assertIn("flags=lanczos", f)
        self.assertIn("sin(2*PI*t/", f)
        self.assertIn("cos(2*PI*t/", f)
        self.assertIn("crop=1080:1920", f)

    def test_effect_is_bounded(self):
        with self.assertRaises(ValueError):
            micro_motion_filter(720, 1280)
        with self.assertRaises(ValueError):
            micro_motion_filter(overscan=1.03)
        with self.assertRaises(ValueError):
            micro_motion_filter(period=1.0)

    def test_release_policy_stays_manual(self):
        c = safety_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["preserve_caption_copy"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
