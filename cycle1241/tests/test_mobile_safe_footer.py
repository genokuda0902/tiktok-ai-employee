import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from mobile_safe_footer import GENRE_ACCENTS, BADGE, DANGER_Y, validate_geometry, filter_graph

class TestMobileSafeFooter(unittest.TestCase):
    def test_genres_ten(self): self.assertEqual(len(GENRE_ACCENTS), 10)
    def test_palette_unique(self): self.assertEqual(len(set(GENRE_ACCENTS.values())), 10)
    def test_all_hex_colors(self):
        for color in GENRE_ACCENTS.values():
            self.assertEqual(len(color), 6)
            self.assertTrue(all(c in '0123456789abcdef' for c in color))
    def test_geometry(self): self.assertTrue(validate_geometry())
    def test_reject_resolution(self):
        with self.assertRaises(ValueError): validate_geometry(720,1280)
    def test_reject_caption_collision(self):
        with self.assertRaises(ValueError): validate_geometry(badge=(570,1390,460,43))
    def test_reject_badge_overflow(self):
        with self.assertRaises(ValueError): validate_geometry(badge=(900,482,460,43))
    def test_reject_footer_mask_collision(self):
        with self.assertRaises(ValueError): validate_geometry(danger_y=1600)
    def test_graph_has_disclosure(self): self.assertIn('社員承認前',filter_graph())
    def test_graph_has_no_audio_filter(self): self.assertNotIn('loudnorm',filter_graph())
    def test_all_genres_filter(self):
        for genre in GENRE_ACCENTS: self.assertIn(GENRE_ACCENTS[genre],filter_graph(genre))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): filter_graph('other')
    def test_safe_badge_above_subtitles(self): self.assertLess(BADGE[1]+BADGE[3],1170)
    def test_lower_mask_after_subtitles(self): self.assertGreaterEqual(DANGER_Y,1700)

if __name__ == '__main__': unittest.main()
