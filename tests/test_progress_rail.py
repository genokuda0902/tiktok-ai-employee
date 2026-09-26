import unittest

from video_engine.progress_rail import progress_rail_filter, release_contract


class ProgressRailTests(unittest.TestCase):
    def test_filter_is_time_driven_and_safe_area_bounded(self):
        f = progress_rail_filter(10.816)
        self.assertIn("y=1760", f)
        self.assertIn("940*min(t/10.816,1)", f)

    def test_invalid_duration_or_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            progress_rail_filter(0)
        with self.assertRaises(ValueError):
            progress_rail_filter(10, 720, 1280)

    def test_release_policy_is_preserved(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["preserve_burned_captions"])
        self.assertTrue(c["manual_post_only"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
