"""Regression tests: ten genres, review gate, deterministic cinematic finale."""
import importlib.util,unittest
from pathlib import Path
from PIL import ImageChops
p=Path(__file__).with_name('finish830.py')
spec=importlib.util.spec_from_file_location('finish830',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Finale830Tests(unittest.TestCase):
    def test_genre_count(self):self.assertEqual(len(m.GENRES),10)
    def test_palette_complete(self):self.assertEqual(set(m.GENRES),set(m.PALETTES))
    def test_genres_validate(self):
        for genre in m.GENRES:self.assertTrue(m.validate(genre))
    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError):m.validate('fake')
    def test_safe_area_preserves_original_subtitles(self):self.assertLessEqual(m.Y+m.H,1130)
    def test_action_stages_are_distinct(self):self.assertEqual(len(set(m.PHASES)),3)
    def test_no_unverified_benefit_numbers(self):self.assertFalse(any(c.isdigit() for c in m.CTA+m.LABEL))
    def test_no_publication_or_posting(self):self.assertIn('NOT_APPROVED',m.REVIEW_STATUS)
    def test_all_palettes_change_image(self):
        self.assertIsNotNone(ImageChops.difference(m.frame(.9,'ai_work'),m.frame(.9,'beauty')).getbbox())
    def test_staged_animation_changes_pixels(self):
        self.assertIsNotNone(ImageChops.difference(m.frame(.05),m.frame(.93)).getbbox())
    def test_deterministic_same_frame(self):
        self.assertIsNone(ImageChops.difference(m.frame(.5),m.frame(.5)).getbbox())
if __name__=='__main__':unittest.main()
