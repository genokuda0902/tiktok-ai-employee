import sys
import unittest
from pathlib import Path
from PIL import ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build_cycle581 as b

class TestSafeCaptionRenderer(unittest.TestCase):
    def test_timing_no_gaps_or_overlaps(self):
        self.assertEqual(b.CUES[0][0],0)
        self.assertEqual(b.CUES[-1][1],468)
        self.assertTrue(all(a[1]==z[0] for a,z in zip(b.CUES,b.CUES[1:])))
    def test_safe_geometry(self):
        self.assertGreaterEqual(78,b.SAFE['left']-2)
        self.assertLessEqual(882,b.SAFE['right'])
        self.assertLessEqual(1425,b.SAFE['bottom'])
        self.assertEqual((b.WIDTH,b.HEIGHT),(1080,1920))
    def test_ten_genres(self):
        gs=b.genres()
        self.assertEqual(len(gs),10)
        for genre,data in gs.items():
            im=b.caption_image(['保存！'],'保存！',data['theme'],8)
            self.assertEqual(im.size,(1080,b.LAYER_H),genre)
    def test_cues_have_visible_japanese_text(self):
        for start,end,lines,highlight in b.CUES:
            self.assertGreater(end,start)
            self.assertTrue(all(line.strip() for line in lines))
            self.assertTrue(any('\u3040'<=ch<='\u9fff' for line in lines for ch in line))
    def test_caption_fits_width(self):
        for start,end,lines,highlight in b.CUES:
            sz=66 if len(lines)==1 else 58
            font=ImageFont.truetype(b.FONT_PATH,sz*2)
            while max(font.getlength(line) for line in lines)>725*2:
                sz-=2
                font=ImageFont.truetype(b.FONT_PATH,sz*2)
            self.assertGreaterEqual(sz,50)
            self.assertLessEqual(max(font.getlength(line) for line in lines),725*2)
    def test_white_text_contrast(self):
        def lin(x):
            x=x/255
            return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
        def lum(rgb):
            return sum(w*lin(c) for w,c in zip((.2126,.7152,.0722),rgb))
        self.assertGreater((lum((251,253,255))+.05)/(lum((4,20,37))+.05),7)

if __name__=='__main__':
    unittest.main()
