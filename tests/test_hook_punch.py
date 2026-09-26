import unittest
from video_engine.hook_punch import hook_punch_filter, safety_contract


class HookPunchTest(unittest.TestCase):
    def test_contract_is_fail_closed_for_delivery(self):
        c = safety_contract()
        self.assertEqual((c["width"], c["height"]), (1080, 1920))
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_audio"])
        self.assertTrue(c["preserve_captions"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])

    def test_filter_is_subtle_and_opening_only(self):
        f = hook_punch_filter()
        self.assertIn("crop=1080:1920", f)
        with self.assertRaises(ValueError):
            hook_punch_filter(start=2.0)
        with self.assertRaises(ValueError):
            hook_punch_filter(duration=0.8)
        with self.assertRaises(ValueError):
            hook_punch_filter(scale=1.2)


if __name__ == "__main__":
    unittest.main()
