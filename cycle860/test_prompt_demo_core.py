import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prompt_demo_core import (
    WIDTH, HEIGHT, GENRE_ACCENTS, CARD_BOX, CAPTION_Y,
    CARDS, validate_cards, safe_zone, filter_graph
)

class PromptDemoTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_ACCENTS), 10)
        self.assertTrue(all(c.startswith("#") and len(c) == 7 for c in GENRE_ACCENTS.values()))

    def test_portrait_size(self):
        self.assertEqual((WIDTH, HEIGHT), (1080, 1920))

    def test_safe_zone(self):
        self.assertTrue(safe_zone())
        self.assertLess(CARD_BOX[3], CAPTION_Y - 50)

    def test_three_states(self):
        self.assertEqual([c.name for c in CARDS], ["before", "after", "check"])
        self.assertTrue(validate_cards())

    def test_before_after_sequence(self):
        self.assertAlmostEqual(CARDS[0].end, CARDS[1].start)
        self.assertLess(CARDS[1].end, CARDS[2].start)

    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            validate_cards((CARDS[0], replace(CARDS[1], start=9.0)))

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            validate_cards((CARDS[0], replace(CARDS[1], name=CARDS[0].name)))

    def test_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            validate_cards((replace(CARDS[0], end=25.0),))

    def test_fades(self):
        graph = filter_graph()
        self.assertEqual(graph.count("alpha=1"), 6)
        self.assertEqual(graph.count("overlay="), 3)
        self.assertIn("format=yuv420p", graph)

    def test_content_is_actionable(self):
        self.assertIn("150字", CARDS[1].title)
        self.assertIn("日付", CARDS[2].title)

if __name__ == "__main__":
    unittest.main()
