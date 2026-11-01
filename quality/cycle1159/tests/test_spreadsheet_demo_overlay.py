"""Cycle1159 synthetic-only tests; no publication or speech certification."""
import importlib.util
import unittest
from pathlib import Path

p=Path(__file__).parents[1]/"spreadsheet_demo_overlay.py"
spec=importlib.util.spec_from_file_location("spreadsheet_demo",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class SpreadsheetDemoTests(unittest.TestCase):
    def test_correct_independent_calculation(self):
        self.assertEqual(m.stats(),{"total":54,"done":44,"remaining":10,"rate":81.5})

    def test_bad_data_rejected(self):
        with self.assertRaises(ValueError):m.stats(((1,2,3),))

    def test_protected_narration_and_title(self):
        self.assertTrue(m.safe())
        with self.assertRaises(ValueError):m.safe(y=1350)
        with self.assertRaises(ValueError):m.safe(y=300)

    def test_ten_genres(self):
        self.assertEqual(len(m.PALETTES),10)
        for genre in m.PALETTES:
            self.assertEqual(m.frame(20,genre).size,(920,630))

    def test_timing_is_chapter_three_only(self):
        self.assertEqual((m.START_FRAME,m.FRAMES),(168,82))
        self.assertEqual(m.frame(81).size,(920,630))
        with self.assertRaises(ValueError):m.frame(82)

    def test_review_only_and_fictional_label(self):
        source=p.read_text(encoding="utf-8")
        self.assertIn("架空データ",source)
        self.assertIn("publication_approved",source)
        self.assertIn("NOT a genuine",source)

if __name__=="__main__":unittest.main()
