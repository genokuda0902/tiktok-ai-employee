"""Cycle1161 synthetic overlay regression tests. No private media required."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import repetition_focus as m

class FocusTests(unittest.TestCase):
    def test_safe_geometry(self):
        self.assertTrue(m.validate())
        self.assertLess(m.Y+m.H,1330)
    def test_10_genres(self):
        self.assertEqual(len(m.GENRES),10)
        for genre in m.GENRES:
            self.assertEqual(m.draw_frame(15,genre).size,(m.W,m.H))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):m.draw_frame(0,'unknown')
    def test_invalid_frame(self):
        with self.assertRaises(ValueError):m.draw_frame(m.FRAME_COUNT)
    def test_transparent_safe_area(self):
        for idx in (0,10,20,30,40,48):
            im=m.draw_frame(idx)
            self.assertEqual(im.getpixel((0,0))[3],0)
            self.assertEqual(im.getpixel((900,560))[3],0)
    def test_distinct_three_row_foci(self):
        for k in range(3):
            im=m.draw_frame(k*12+6)
            x0,y0,_,_=m.ROWS[k]
            self.assertGreater(im.getpixel((x0,y0+35))[3],0)
    def test_final_connector_visible(self):
        self.assertIsNotNone(m.draw_frame(45).getbbox())
    def test_frame_is_rgba(self):
        self.assertEqual(m.draw_frame(5).mode,'RGBA')

if __name__=='__main__':unittest.main()
