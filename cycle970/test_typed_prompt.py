import unittest
import numpy as np
from typed_prompt import LINES, GENRES, check_genre, visible_text, scene, CAPTION_TOP

class TestTypedPrompt(unittest.TestCase):
    def test_start_blank(self): self.assertEqual(visible_text(0),['','',''])
    def test_end_full(self): self.assertEqual(visible_text(0.84),list(LINES))
    def test_monotonic(self):
        lens=[sum(map(len,visible_text(i/100))) for i in range(101)]
        self.assertEqual(lens,sorted(lens))
    def test_typing_has_motion(self): self.assertFalse(np.array_equal(scene(.1),scene(.7)))
    def test_geometry(self): self.assertEqual(scene(.5).shape,(CAPTION_TOP,1080,3))
    def test_valid_palette_count(self): self.assertEqual(len(GENRES),10)
    def test_other_genres_fail_closed(self):
        for genre in GENRES.keys()-{'ai_work'}:
            with self.assertRaises(PermissionError): check_genre(genre)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): check_genre('unknown')
    def test_negative_phase(self): self.assertEqual(visible_text(-1),['','',''])
    def test_late_phase(self): self.assertEqual(visible_text(2),list(LINES))

if __name__=='__main__':unittest.main()
