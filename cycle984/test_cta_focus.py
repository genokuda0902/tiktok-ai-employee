import unittest
from cta_focus import GENRES,SAFE_Y,CARDS,focus_step,overlay_frame,validate
class CTATests(unittest.TestCase):
    def test_frame_range(self):
        self.assertEqual([focus_step(x,82) for x in (0,26,27,53,54,81)],[0,0,0,1,1,2])
        for i in (-1,82):
            with self.assertRaises(ValueError):focus_step(i,82)
    def test_step_progression(self):
        self.assertEqual([focus_step(x,82) for x in range(82)].count(2),27)
    def test_safe_area(self):
        for i in (0,30,60,81):
            im=overlay_frame(i,82)
            self.assertEqual(im.size,(1080,SAFE_Y))
            self.assertEqual(im.mode,'RGBA')
    def test_focus_changes(self):
        self.assertNotEqual(overlay_frame(0,82).tobytes(),overlay_frame(81,82).tobytes())
    def test_transparent_outside_artwork(self):
        for i in (0,40,81):
            self.assertEqual(overlay_frame(i,82).getpixel((1000,1300))[3],0)
    def test_card_bounds(self):
        self.assertTrue(all(0<x0<x1<1080 and 0<y0<y1<SAFE_Y for x0,y0,x1,y1 in CARDS))
    def test_fail_closed_other_genres(self):
        for genre in GENRES[1:]:
            with self.assertRaises(ValueError):validate(genre)
    def test_synthetic_other_genres(self):
        for genre in GENRES:validate(genre,True)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):validate('unknown')
if __name__=='__main__':unittest.main()
