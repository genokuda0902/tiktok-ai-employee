import unittest

from video_engine.kinetic_card_motion import kinetic_card_contract, motion_profile, zoompan_filter


class KineticCardMotionTests(unittest.TestCase):
    def test_portrait_manual_zero_cost_contract(self):
        c = kinetic_card_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertTrue(c["preserve_burned_captions"])
        self.assertLessEqual(c["max_zoom_delta"], 0.035)

    def test_wrong_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            kinetic_card_contract(720, 1280)

    def test_profiles_alternate_without_excess_zoom(self):
        a, b = motion_profile(0), motion_profile(1)
        self.assertLess(a.zoom_start, a.zoom_end)
        self.assertGreater(b.zoom_start, b.zoom_end)
        self.assertLessEqual(a.max_zoom_delta, 0.035)
        self.assertLessEqual(b.max_zoom_delta, 0.035)

    def test_filter_keeps_portrait_geometry_and_30fps(self):
        f = zoompan_filter(0)
        self.assertIn("s=1080x1920", f)
        self.assertIn("fps=30", f)
        self.assertIn("flags=lanczos", f)

    def test_invalid_frame_count_fails_closed(self):
        with self.assertRaises(ValueError):
            zoompan_filter(0, 0)


if __name__ == "__main__":
    unittest.main()
