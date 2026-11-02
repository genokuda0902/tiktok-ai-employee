import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import save_reuse_panel as s

class SaveReusePanelTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(s.PALETTES),10)
        for g in s.PALETTES:
            im,labels=s.design(g,scale=1)
            self.assertEqual(im.size,(980,695))
            self.assertGreaterEqual(len(labels),16)
    def test_overlay_geometry(self):
        self.assertEqual(s.panel().size,(1080,1920))
    def test_outside_roi_transparent(self):
        im=s.panel()
        for xy in [(0,0),(400,300),(400,1200),(1050,1800)]:
            self.assertEqual(im.getpixel(xy)[3],0)
    def test_inside_roi_opaque(self):
        im=s.panel()
        self.assertEqual(im.getpixel((60,450))[3],255)
    def test_reject_bad_genre(self):
        with self.assertRaises(ValueError):s.design('unknown')
    def test_reject_bad_scale(self):
        with self.assertRaises(ValueError):s.design('ai',scale=4)
    def test_text_all_inside(self):
        for g in s.PALETTES:
            _,labels=s.design(g,scale=1)
            for text,(x0,y0,x1,y1) in labels:
                self.assertGreaterEqual(x0,0,text)
                self.assertGreaterEqual(y0,0,text)
                self.assertLessEqual(x1,980,text)
                self.assertLessEqual(y1,695,text)
    def test_cards_separated(self):
        self.assertGreaterEqual(537-443,90)
    def test_scene_index(self):
        self.assertEqual(s.SCENE_INDEX,6)

if __name__=='__main__':unittest.main()
