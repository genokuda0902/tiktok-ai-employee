import unittest
from visual_core import *
class CoreTest(unittest.TestCase):
    def test_storyboard(self): self.assertTrue(validate_storyboard(SCENES,CUTS,'ai_productivity'))
    def test_genres(self):
        self.assertEqual(len(GENRE_COLORS),10)
        for g in GENRE_COLORS: self.assertTrue(validate_storyboard(SCENES,CUTS,g))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError): validate_storyboard(SCENES,CUTS,'no')
    def test_invalid_duration(self):
        with self.assertRaises(ValueError): validate_storyboard(SCENES,[0,1,2,3,4,5,6,7,8],'ai_productivity')
    def test_repeated_slide(self):
        with self.assertRaises(ValueError): validate_storyboard([SCENES[0]]*8,CUTS,'ai_productivity')
    def test_pct(self): self.assertEqual(pct(3,4),75)
    def test_pct_zero(self): self.assertEqual(pct(0,4),0)
    def test_pct_all(self): self.assertEqual(pct(4,4),100)
    def test_pct_invalid(self):
        for d,t in [(-1,4),(5,4),(0,0)]:
            with self.assertRaises(ValueError): pct(d,t)
    def test_safe_caption(self):
        x1,y1,x2,y2=SUBTITLE_BOX
        self.assertLess(y2,BOTTOM_CONTENT)
        self.assertGreater(y1,TOP_SAFE)
    def test_native_resolution(self): self.assertEqual((W,H),(1080,1920))
    def test_8_scenes(self): self.assertEqual(len(SCENES),8)
if __name__=='__main__': unittest.main()
