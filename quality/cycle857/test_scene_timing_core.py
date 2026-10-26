import unittest,sys,json,tempfile
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent))
from scene_timing_core import *

class TestNativeScene(unittest.TestCase):
    def test_eight_scenes(self):self.assertEqual(len(frame_counts()),8)
    def test_exact_frames(self):self.assertEqual(sum(frame_counts()),691)
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_native_crop(self):self.assertLessEqual(native_crop_scale((941,1672)),1)
    def test_reject_upscale(self):
        with self.assertRaises(ValueError):native_crop_scale((640,640))
    def test_invalid_boundaries(self):
        with self.assertRaises(ValueError):frame_counts((0,1,1,2,3,4,5,6,691))
    def test_validate_beat_grouping(self):
        beats=json.loads((Path(__file__).parent.parent/'assets/caption_beats.json').read_text())
        self.assertTrue(validate_beats(beats))
    def test_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'p.png';Image.new('RGB',(1024,1536)).save(p)
            with self.assertRaises(ValueError):audit_sources([p]*8)
    def test_small_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'p.png';Image.new('RGB',(640,900)).save(p)
            with self.assertRaises(ValueError):audit_sources([p]*8)
if __name__=='__main__':unittest.main()
