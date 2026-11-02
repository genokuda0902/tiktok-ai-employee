import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from chapter_progress import *

CHAPTERS=[{'start_time':str(i),'end_time':str(i+1)} for i in range(8)]
class ChapterProgressTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRE_COLORS),10)
    def test_frame_dimensions(self): self.assertEqual(draw_progress(0,0).size,(OVERLAY_W,OVERLAY_H))
    def test_all_genres(self):
        for g in GENRE_COLORS: self.assertEqual(draw_progress(7,.6,g).mode,'RGBA')
    def test_first_chapter(self): self.assertEqual(chapter_fraction(.5,CHAPTERS),(0,.5))
    def test_boundary(self): self.assertEqual(chapter_fraction(1,CHAPTERS),(1,0.))
    def test_last(self): self.assertEqual(chapter_fraction(7.5,CHAPTERS),(7,.5))
    def test_end_clamp(self): self.assertEqual(chapter_fraction(9,CHAPTERS),(7,1.))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError): draw_progress(0,.5,'bad')
    def test_invalid_index(self):
        with self.assertRaises(ValueError): draw_progress(8,.5)
    def test_invalid_fraction(self):
        with self.assertRaises(ValueError): draw_progress(0,1.1)
    def test_active_only(self):
        im=draw_progress(3,.5)
        self.assertEqual(im.getpixel((2,2))[3],0)
        self.assertEqual(im.getpixel((2+3*BAR_STEP,2))[3],255)
    def test_progress_increases(self):
        x=2+3*BAR_STEP
        a=draw_progress(3,.2)
        b=draw_progress(3,.8)
        self.assertNotEqual(a.getpixel((x+55,3)),b.getpixel((x+55,3)))
if __name__=='__main__': unittest.main()
