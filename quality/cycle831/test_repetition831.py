import importlib.util,unittest
from pathlib import Path
from PIL import ImageChops
s=importlib.util.spec_from_file_location('repetition831',Path(__file__).with_name('repetition831.py'))
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Tests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(m.GENRES),10)
    def test_palettes(self):self.assertEqual(set(m.GENRES),set(m.PALETTES))
    def test_safe_region(self):self.assertTrue(all(m.validate(g) for g in m.GENRES))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):m.validate('invalid')
    def test_frames(self):self.assertEqual(m.LAST-m.FIRST+1,97)
    def test_no_publication(self):self.assertIn('NOT_APPROVED',m.REVIEW)
    def test_image_animation(self):self.assertIsNotNone(ImageChops.difference(m.frame(.1),m.frame(.9)).getbbox())
    def test_palette_image(self):self.assertIsNotNone(ImageChops.difference(m.frame(.8,'ai_work'),m.frame(.8,'beauty')).getbbox())
    def test_repeatable(self):self.assertIsNone(ImageChops.difference(m.frame(.7),m.frame(.7)).getbbox())
if __name__=='__main__':unittest.main()
