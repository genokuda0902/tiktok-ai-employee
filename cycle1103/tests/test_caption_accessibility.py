import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from caption_accessibility import render_plate,CAPTIONS,GENRE_PALETTES

class TestCaption(unittest.TestCase):
    def test_eight_scenes(self):self.assertEqual(len(CAPTIONS),8)
    def test_ten_genres(self):self.assertEqual(len(GENRE_PALETTES),10)
    def test_render_every_genre(self):
        for genre in GENRE_PALETTES:self.assertEqual(render_plate(0,genre).size,(1080,1920))
    def test_caption_safe_area(self):
        im=render_plate(4)
        self.assertEqual(im.getpixel((540,1630))[3],0)
        self.assertEqual(im.getpixel((540,1400))[3],255)
    def test_outside_unchanged(self):
        im=render_plate(2)
        for p in [(10,10),(1000,1700),(500,1000),(500,1800)]:
            self.assertEqual(im.getpixel(p)[3],0)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):render_plate(0,'unlicensed')
    def test_invalid_scene(self):
        with self.assertRaises(ValueError):render_plate(8)
    def test_all_lines_fit(self):
        for i in range(8):self.assertEqual(render_plate(i).size,(1080,1920))
if __name__=='__main__':unittest.main()
