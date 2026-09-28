import unittest

from video_engine.japanese_hook_font_guard import JapaneseHookFontGuard, release_contract


class JapaneseHookFontGuardTests(unittest.TestCase):
    def test_requires_cjk_font_and_portrait_delivery(self):
        g = JapaneseHookFontGuard()
        g.validate()
        self.assertIn("NotoSansCJK", g.font_path)
        with self.assertRaises(ValueError):
            JapaneseHookFontGuard(width=720, height=1280).validate()

    def test_hook_repair_stays_in_first_three_seconds(self):
        with self.assertRaises(ValueError):
            JapaneseHookFontGuard(end=3.1).validate()

    def test_filter_explicitly_draws_japanese_capable_font(self):
        f = JapaneseHookFontGuard().filters("Excel集計、まだ手作業？", "知らないと損")
        self.assertIn("NotoSansCJK-Bold.ttc", f)
        self.assertIn("drawtext", f)
        self.assertIn("lt(t,1.8)", f)

    def test_release_policy_remains_manual(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["japanese_font_required"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
