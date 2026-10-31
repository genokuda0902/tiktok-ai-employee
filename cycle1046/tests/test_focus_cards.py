import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/'source'/'focus_cards.py'
spec=importlib.util.spec_from_file_location('focus_cards',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class FocusCardTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(set(m.GENRES)),10)
    def test_frame_bounds(self): self.assertEqual((m.START,m.END,m.PROTECTED_Y),(87,174,1460))
    def test_progression(self):
        self.assertEqual([m.visible_cards(i) for i in (0,23,24,47,48,86)],[1,1,2,2,3,3])
    def test_bad_frame(self):
        for i in (-1,87):
            with self.assertRaises(ValueError):m.visible_cards(i)
    def test_image_dimensions(self): self.assertEqual(m.make_frame(30).size,(1080,1460))
    def test_ten_genre_frames(self):
        for genre in m.GENRES: self.assertEqual(m.make_frame(50,genre,540,800).size,(540,800))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):m.make_frame(0,'not_approved')
    def test_fail_closed_no_review(self):
        with self.assertRaisesRegex(ValueError,'review-only'):m.validate('missing','bad','ai_work',False)
    def test_fail_closed_no_source(self):
        with self.assertRaisesRegex(ValueError,'approved source'):m.validate('missing','bad','beauty',True)
    def test_fail_closed_bad_sha(self):
        with self.assertRaisesRegex(ValueError,'SHA mismatch'):m.validate('missing','bad','ai_work',True)

if __name__=='__main__': unittest.main()
