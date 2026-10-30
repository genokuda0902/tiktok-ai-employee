import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'/'quality'))
from cycle1001_staged_reveal import ACCENTS,SIZE,AFTER,make_mask,render

class TestReveal(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(ACCENTS),10)
    def test_all_genres_render(self):
        for genre in ACCENTS:
            with self.subTest(genre=genre): self.assertEqual(make_mask(genre).size,SIZE)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): make_mask('unknown')
    def test_outside_after_transparent(self):
        im=make_mask()
        for xy in [(10,10),(540,850),(540,1460),(1000,1600)]:
            self.assertEqual(im.getpixel(xy)[3],0)
    def test_after_opaque(self):
        self.assertEqual(make_mask().getpixel((540,1100))[3],255)
    def test_safe_area(self):
        self.assertLess(AFTER[3],1390)
        self.assertGreater(AFTER[1],900)
    def test_bad_timing(self):
        with self.assertRaises(ValueError): render(Path(__file__),Path('/tmp/no.mp4'),start=-1)
    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError): render(Path('/nonexistent/file.mp4'),Path('/tmp/no.mp4'))

if __name__=='__main__': unittest.main()
