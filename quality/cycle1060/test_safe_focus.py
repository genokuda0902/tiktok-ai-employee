import unittest
from PIL import Image
from quality.cycle1058.real_writer_focus import PALETTES, COUNT, START
from quality.cycle1060.safe_focus import render_frame, RAIL_X, PROTECTED_TEXT

class TestSafeFocus(unittest.TestCase):
    def setUp(self):
        self.shot=Image.new('RGB',(1600,900),'white')
        # Synthetic text-like lines; no real user data.
        for y in (360,410,460):
            for x in range(420,1050):
                self.shot.putpixel((x,y),(0,0,0))
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES),10)
        for genre in PALETTES:
            self.assertEqual(render_frame(30,self.shot,genre).size,(1080,1270))
    def test_source_text_pixels_unchanged_for_all_three_stages(self):
        expected=self.shot.crop((352,276,1200,665)).resize((920,500))
        x0,y0,x1,y1=PROTECTED_TEXT
        region=expected.crop((x0-80,y0-404,x1-80,y1-404)).tobytes()
        for i in (0,27,28,58,59,88):
            frame=render_frame(i,self.shot)
            self.assertEqual(frame.crop(PROTECTED_TEXT).tobytes(),region)
    def test_marker_is_outside_text_region(self):
        self.assertLess(RAIL_X[1],PROTECTED_TEXT[0])
    def test_stage_visuals_differ(self):
        self.assertNotEqual(render_frame(0,self.shot).tobytes(),render_frame(88,self.shot).tobytes())
    def test_fail_closed_unknown_genre(self):
        with self.assertRaises(ValueError):render_frame(10,self.shot,'secret')
    def test_fail_closed_small_image(self):
        with self.assertRaises(ValueError):render_frame(10,Image.new('RGB',(1000,500)))
    def test_frame_and_timing(self):
        self.assertEqual((START,COUNT),(520,89))
        with self.assertRaises(ValueError):render_frame(COUNT,self.shot)
if __name__=='__main__':unittest.main()
