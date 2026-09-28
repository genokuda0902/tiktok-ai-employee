import unittest

from video_engine.hook_focus import hook_focus_filter, release_contract


class HookFocusTests(unittest.TestCase):
    def test_default_is_bounded_to_opening(self):
        f = hook_focus_filter()
        self.assertIn("between(t,0,1.20)", f)
        self.assertIn("contrast=1.040", f)

    def test_aggressive_settings_fail_closed(self):
        with self.assertRaises(ValueError):
            hook_focus_filter(duration=2.0)
        with self.assertRaises(ValueError):
            hook_focus_filter(contrast=1.2)

    def test_portrait_manual_release_only(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["human_approval_required"])
        self.assertTrue(c["manual_post_only"])
        self.assertFalse(c["auto_post"])
        with self.assertRaises(ValueError):
            release_contract(720, 1280)


if __name__ == "__main__":
    unittest.main()
