import unittest

from video_engine.hook_visual_emphasis import hook_visual_contract, hook_visual_filter


class HookVisualEmphasisTests(unittest.TestCase):
    def test_filter_is_first_second_dynamic_eq(self):
        f = hook_visual_filter(0.9)
        self.assertIn("lt(t,0.900)", f)
        self.assertIn("brightness=", f)
        self.assertIn("saturation=", f)
        self.assertIn("eval=frame", f)

    def test_duration_is_bounded(self):
        with self.assertRaises(ValueError):
            hook_visual_filter(0.2)
        with self.assertRaises(ValueError):
            hook_visual_filter(2.0)

    def test_release_policy_is_preserved(self):
        c = hook_visual_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["first_second_only"])
        self.assertFalse(c["changes_caption_copy"])
        self.assertFalse(c["changes_audio"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])

    def test_wrong_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            hook_visual_contract(720, 1280)


if __name__ == "__main__":
    unittest.main()
