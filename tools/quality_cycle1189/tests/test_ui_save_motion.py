import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from ui_save_motion import Plan,GENRES,COLORS,check_plan,ease,position,generate_frames,render

class UIMotionTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_color_for_every_genre(self):self.assertEqual(set(GENRES),set(COLORS))
    def test_unique_colors(self):self.assertEqual(len(set(COLORS.values())),10)
    def test_ease_ends(self):self.assertEqual((ease(-1),ease(0),ease(1),ease(3)),(0,0,1,1))
    def test_ease_monotonic(self):self.assertEqual(sorted(ease(i/100) for i in range(101)),[ease(i/100) for i in range(101)])
    def test_motion_ends(self):
        p=Plan();self.assertEqual(position(.26,p),p.source_xy);self.assertEqual(position(1.34,p),p.target_xy)
    def test_safe_area(self):self.assertTrue(check_plan(Plan()))
    def test_reject_overlay_on_captions(self):
        with self.assertRaises(ValueError):check_plan(Plan(box_y=1200))
    def test_reject_cursor_clipping(self):
        with self.assertRaises(ValueError):check_plan(Plan(target_xy=(1070,800)))
    def test_reject_invalid_timing(self):
        with self.assertRaises(ValueError):check_plan(Plan(duration=5))
    def test_unknown_genre(self):
        with TemporaryDirectory() as d:
            with self.assertRaises(ValueError):generate_frames(Path(d),'unknown')
    def test_no_overwrite(self):
        with self.assertRaises(ValueError):render('a.mp4','a.mp4')
    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError):render('missing.mp4','new.mp4')
    def test_frames_rgba_and_safe_bounds(self):
        with TemporaryDirectory() as d:
            p=Plan(duration=.8)
            count=generate_frames(Path(d),'ai',p)
            self.assertEqual(count,24)
            for f in sorted(Path(d).glob('*.png')):
                with Image.open(f) as im:
                    self.assertEqual(im.size,(p.box_w,p.box_h));self.assertEqual(im.mode,'RGBA')
    def test_no_existing_frames(self):
        with TemporaryDirectory() as d:
            Path(d,'exists').write_text('x')
            with self.assertRaises(ValueError):generate_frames(Path(d))

if __name__=='__main__':unittest.main()
