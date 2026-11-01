import importlib.util
from pathlib import Path
import tempfile
import unittest
from PIL import Image

CODE=Path(__file__).resolve().parents[1]/'code'/'scene_transition_sweep.py'
spec=importlib.util.spec_from_file_location('sweep',CODE)
sweep=importlib.util.module_from_spec(spec)
spec.loader.exec_module(sweep)

class SweepTests(unittest.TestCase):
    def test_valid_timing(self): self.assertTrue(sweep.validate_timing())
    def test_ten_genres(self): self.assertEqual(len(sweep.GENRES),10)
    def test_no_overlapping_cuts(self):
        with self.assertRaises(AssertionError): sweep.validate_timing((42,45),675)
    def test_reject_out_of_bounds(self):
        with self.assertRaises(AssertionError): sweep.validate_timing((670,),675)
    def test_empty_at_start(self):
        a=sweep.make_frame(0,sweep.GENRES['ai-work']);self.assertEqual(a.getchannel('A').getbbox(),None)
    def test_empty_at_end(self):
        a=sweep.make_frame(1,sweep.GENRES['ai-work']);self.assertEqual(a.getchannel('A').getbbox(),None)
    def test_nonempty_midpoint(self):
        a=sweep.make_frame(.5,sweep.GENRES['ai-work']);self.assertIsNotNone(a.getchannel('A').getbbox())
    def test_overlay_size(self): self.assertEqual(sweep.make_frame(.5,(73,228,211)).size,(820,28))
    def test_presets_are_distinct(self): self.assertNotEqual(sweep.GENRES['ai-work'],sweep.GENRES['finance'])
    def test_sequence_is_frame_exact(self):
        with tempfile.TemporaryDirectory() as td:
            frames=sweep.generate_overlay_sequence(Path(td),(4,30),50)
            self.assertEqual(len(frames),26)
            self.assertEqual(len(list(Path(td).glob('overlay_*.png'))),50)
            self.assertEqual(Image.open(Path(td)/'overlay_00017.png').getchannel('A').getbbox(),None)
            self.assertIsNotNone(Image.open(Path(td)/'overlay_00009.png').getchannel('A').getbbox())
    def test_caption_safe_roi(self):
        x,y,w,h=sweep.ROI;self.assertLess(y+h,500);self.assertLessEqual(x+w,1080)
    def test_scene_cuts_from_actual_frames(self):
        self.assertEqual(sweep.CUTS,(42,94,168,250,330,412,499))

if __name__=='__main__': unittest.main()
