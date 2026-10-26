import unittest
from mobile_layout_core import (
    PALETTES, MobileLayout, palette_for,
    completed_progress, report_text, browser_area_growth_percent,
)

class MobileReadabilityTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES), 10)

    def test_all_palettes(self):
        for genre, color in PALETTES.items():
            with self.subTest(genre=genre):
                self.assertEqual(palette_for(genre), color)
                self.assertTrue(color.startswith("#"))

    def test_unknown_genre(self):
        with self.assertRaises(ValueError):
            palette_for("unknown")

    def test_portrait(self):
        layout = MobileLayout()
        self.assertEqual((layout.video_width, layout.video_height), (1080, 1920))

    def test_caption_safe_zone(self):
        self.assertTrue(MobileLayout().validate())

    def test_caption_overlap_rejected(self):
        with self.assertRaises(AssertionError):
            MobileLayout(caption_top=1200).validate()

    def test_screen_overflow_rejected(self):
        with self.assertRaises(AssertionError):
            MobileLayout(browser_y=1000).validate()

    def test_area_increase(self):
        self.assertEqual(browser_area_growth_percent(), 113.3)

    def test_invalid_previous_height(self):
        with self.assertRaises(ValueError):
            browser_area_growth_percent(0)

    def test_progress_75(self):
        self.assertEqual(completed_progress([True, True, True, False])["percent"], 75)

    def test_progress_0_and_100(self):
        self.assertEqual(completed_progress([False] * 4)["percent"], 0)
        self.assertEqual(completed_progress([True] * 4)["percent"], 100)

    def test_invalid_task_list(self):
        for states in ([True], [1, 0, 1, 0]):
            with self.assertRaises(ValueError):
                completed_progress(states)

    def test_report_reordering(self):
        p = completed_progress([True, True, True, False])
        self.assertTrue(report_text(p, conclusion_first=True).startswith("今週の進捗は"))
        self.assertTrue(report_text(p, conclusion_first=False).startswith("未完了1件"))

if __name__ == "__main__":
    unittest.main()
