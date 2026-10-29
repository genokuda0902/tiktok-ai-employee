import importlib.util
import tempfile
import unittest
from pathlib import Path
from PIL import Image
MODULE=Path(__file__).resolve().parent/'guided_read.py'
spec=importlib.util.spec_from_file_location('guided_read',MODULE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class GuidedReadTests(unittest.TestCase):
    def test_10_genres(self): self.assertEqual(len(m.GENRE_PALETTES),10)
    def test_genres_valid(self):
        for g in m.GENRE_PALETTES:self.assertTrue(m.validate(g))
    def test_unknown_fails_closed(self):
        with self.assertRaises(ValueError):m.validate('unknown')
    def test_invalid_row_rejected(self):
        with self.assertRaises(ValueError):m.validate('ai_work',rows=((10,1350,50,1400),)*3)
    def test_invalid_time_rejected(self):
        with self.assertRaises(ValueError):m.validate('ai_work',bounds=(8,4))
    def test_all_three_overlays_caption_safe(self):
        with tempfile.TemporaryDirectory() as t:
            for i in range(3):
                path=m.create_overlay('ai_work',i,Path(t)/f'{i}.png')
                im=Image.open(path)
                self.assertEqual(im.size,(1080,1920))
                self.assertIsNone(im.crop((0,m.CAPTION_TOP,1080,1920)).getbbox())
    def test_three_overlays_differ(self):
        with tempfile.TemporaryDirectory() as t:
            ims=[m.create_overlay('ai_work',i,Path(t)/f'{i}.png') for i in range(3)]
            self.assertEqual(len({m.sha(x) for x in ims}),3)
    def test_all_palettes_render(self):
        with tempfile.TemporaryDirectory() as t:
            for g in m.GENRE_PALETTES:
                self.assertTrue(Path(m.create_overlay(g,1,Path(t)/f'{g}.png')).exists())
    def test_invalid_index(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):m.create_overlay('ai_work',4,Path(t)/'bad.png')
if __name__=='__main__':unittest.main()
