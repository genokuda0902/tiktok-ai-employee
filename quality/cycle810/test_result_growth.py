import unittest
from pathlib import Path
import result_growth as m

class TestResultGrowth(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(m.EXAMPLES),10)
    def test_each_genre_safe(self):
        for genre in m.EXAMPLES: self.assertEqual(len(m.check(genre)),5)
    def test_reject_unknown(self):
        with self.assertRaises(ValueError):m.check('unknown')
    def test_frame_range(self):
        with self.assertRaises(ValueError):m.frame(-1)
        with self.assertRaises(ValueError):m.frame(90)
    def test_frame_is_vertical_rgba(self):self.assertEqual(m.frame(0).size,(1080,1920))
    def test_early_late_different(self):self.assertNotEqual(m.frame(2).tobytes(),m.frame(83).tobytes())
    def test_caption_safe_region(self):
        im=m.frame(89)
        self.assertEqual(im.getpixel((500,1400))[3],0)
        self.assertEqual(im.getpixel((500,450))[3],0)
    def test_fictional_badge_visible(self):self.assertGreater(m.frame(5).getpixel((800,735))[3],0)
    def test_numeric_consistency(self):
        for k,(metric,old,new,unit,color) in m.EXAMPLES.items():
            self.assertEqual(round((new/old-1)*100),150)
    def test_no_publication(self):
        src=Path(m.__file__).read_text(encoding='utf-8')
        self.assertIn("'posting_allowed':False",src)
        self.assertIn("'auto_post':False",src)
    def test_finite_animation(self):
        for t in [-10,0,.5,1,10]:self.assertTrue(0<=m.ease(t)<=1)

if __name__=='__main__':unittest.main()
