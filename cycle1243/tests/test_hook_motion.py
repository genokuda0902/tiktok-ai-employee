"""Unit checks for 10-genre opening hook, geometry, and safe timing."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from hook_motion import GENRE_ACCENTS, filter_graph, validate, OPEN_START, OPEN_END, X_START, X_END

class HookMotionTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRE_ACCENTS),10)
    def test_genres_unique(self): self.assertEqual(len(set(GENRE_ACCENTS)),10)
    def test_palettes(self):
        for genre,color in GENRE_ACCENTS.items():
            self.assertRegex(color,r'^[0-9a-f]{6}$')
            self.assertIn(color,filter_graph(genre))
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError): validate('unknown')
    def test_wrong_resolution_rejected(self):
        with self.assertRaises(ValueError): validate('ai',720,1280)
    def test_font_required(self):
        with self.assertRaises(FileNotFoundError): validate('ai',font='/does/not/exist.ttf')
    def test_ends_before_first_cut(self):
        self.assertGreater(OPEN_START,0)
        self.assertLess(OPEN_END,1.4)
        self.assertIn('enable=',filter_graph())
    def test_subtitle_region_untouched(self):
        self.assertLess(X_END,610)
        self.assertLess(X_START,X_END)
        self.assertNotIn('drawbox',filter_graph())
    def test_two_layer_cue(self): self.assertEqual(filter_graph().count('drawtext='),2)
    def test_no_remote_assets(self):
        self.assertNotIn('http',filter_graph())
        self.assertNotIn('movie=',filter_graph())
    def test_no_frame_rate_change(self): self.assertNotIn('fps=',filter_graph())
    def test_ease_out(self): self.assertIn('pow(',filter_graph())

if __name__=='__main__': unittest.main()
