import tempfile, unittest
from pathlib import Path
from chart_story import (DATA,GENRES,POLICY,ROI,FRAMES,START,COLORS,draw_frame,
                         totals,frames_to_disk,ease,validate)

class ChartTests(unittest.TestCase):
    def test_source_data_totals(self): self.assertEqual(totals(),(46,29))
    def test_no_fabricated_data(self):
        with self.assertRaises(ValueError): totals({'months':['4月'],'A':[12],'B':[8,9]})
    def test_reject_negative(self):
        with self.assertRaises(ValueError): totals({'months':['4月','5月'],'A':[-1,2],'B':[2,3]})
    def test_ten_genres(self):self.assertEqual(len(GENRES),len(COLORS))
    def test_reject_unknown(self):
        with self.assertRaises(ValueError):draw_frame(0,'unknown')
    def test_frame_range(self):
        with self.assertRaises(ValueError):draw_frame(FRAMES)
    def test_native_picture_size(self):self.assertEqual(draw_frame(40).size,ROI[2:])
    def test_caption_safe_geometry(self):
        x,y,w,h=ROI;self.assertGreaterEqual(x,80);self.assertGreaterEqual(y,450)
        self.assertLessEqual(x+w,1000);self.assertLessEqual(y+h,1240)
    def test_animation_changes(self):
        self.assertNotEqual(draw_frame(0).tobytes(),draw_frame(40).tobytes())
        self.assertNotEqual(draw_frame(40).tobytes(),draw_frame(80).tobytes())
    def test_ease_bounds(self):self.assertEqual((ease(-1),ease(2)),(0,1))
    def test_private_only(self):
        self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['automatic_posting'])
    def test_missing_source_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                validate(Path(d)/'missing.mp4',Path(d)/'out.mp4',POLICY,'ai_work')
    def test_frame_generator(self):
        with tempfile.TemporaryDirectory() as d:
            frames_to_disk(d)
            self.assertEqual(len(list(Path(d).glob('chart_*.png'))),FRAMES)
            with self.assertRaises(ValueError):frames_to_disk(d)
    def test_source_segment(self):self.assertEqual((START,START+FRAMES-1),(170,250))
if __name__=='__main__':unittest.main()