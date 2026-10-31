import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
from quality.cycle1058.real_writer_focus import PALETTES
from quality.cycle1062.real_calc_sample import (
    render_frame, stage, START, COUNT, TABLE_RECT,
    PROTECTED_TABLE, SOURCE_CROP, compose, sha256)

class CalcSampleTests(unittest.TestCase):
    def setUp(self):
        self.shot=Image.new('RGB',(1600,900),'white')
        d=ImageDraw.Draw(self.shot)
        for y in range(295,450,20):
            d.line((80,y,500,y),fill='#223344',width=2)

    def test_ten_genres_and_dimensions(self):
        self.assertEqual(len(PALETTES),10)
        for genre in PALETTES:
            self.assertEqual(render_frame(0,self.shot,genre).size,(1080,1270))

    def test_protected_table_exact_for_three_stages(self):
        original=self.shot.crop(SOURCE_CROP).resize(
            (TABLE_RECT[2]-TABLE_RECT[0],TABLE_RECT[3]-TABLE_RECT[1]),Image.Resampling.LANCZOS)
        x0,y0,x1,y1=PROTECTED_TABLE
        expected=original.crop((x0-TABLE_RECT[0],y0-TABLE_RECT[1],
                                x1-TABLE_RECT[0],y1-TABLE_RECT[1])).tobytes()
        for i in (0,27,28,55,56,81):
            self.assertEqual(render_frame(i,self.shot).crop(PROTECTED_TABLE).tobytes(),expected)

    def test_three_stages(self):
        self.assertEqual([stage(i) for i in (0,27,28,55,56,81)],[0,0,1,1,2,2])

    def test_caption_safe(self):
        self.assertEqual((START,COUNT),(174,82))
        self.assertEqual(render_frame(0,self.shot).height,1270)

    def test_distinct_frames(self):
        self.assertNotEqual(render_frame(0,self.shot).tobytes(),render_frame(80,self.shot).tobytes())

    def test_fail_closed(self):
        with self.assertRaises(ValueError):render_frame(0,self.shot,'unknown')
        with self.assertRaises(ValueError):render_frame(0,Image.new('RGB',(500,500)))
        with self.assertRaises(ValueError):render_frame(82,self.shot)

    def test_input_sha_gate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'src.mp4').write_bytes(b'fake')
            (p/'shot.png').write_bytes(b'fake')
            with self.assertRaises(ValueError):
                compose(p/'src.mp4',p/'shot.png',p/'out.mp4',p,'0'*64,'0'*64)
            self.assertEqual(len(sha256(p/'src.mp4')),64)

if __name__=='__main__':
    unittest.main()
