import copy
import json
import sys
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from copy_paste_story import FRAMES, FPS, W, H, geometry, make_frame, validate

CONFIG = json.loads((Path(__file__).parent/'config.json').read_text())

class CopyPasteStoryTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(set(CONFIG['genres'])), 10)
    def test_sum(self):
        self.assertTrue(validate(CONFIG))
        self.assertEqual(sum(r['value'] for r in CONFIG['rows']),650000)
    def test_bad_total_fails(self):
        c=copy.deepcopy(CONFIG);c['total']=1
        with self.assertRaises(ValueError): validate(c)
    def test_rights_fail_closed(self):
        for flag in ('rights_reviewed','employee_approved','publication_approved'):
            c=copy.deepcopy(CONFIG);c[flag]=True
            with self.assertRaises(ValueError):validate(c)
    def test_publication_mode_rejected(self):
        c=copy.deepcopy(CONFIG);c['mode']='publish'
        with self.assertRaises(ValueError):validate(c)
    def test_empty_rows_rejected(self):
        c=copy.deepcopy(CONFIG);c['rows']=[]
        with self.assertRaises(ValueError):validate(c)
    def test_safe_rectangles(self):
        for box in geometry().values():
            x0,y0,x1,y1=box
            self.assertGreaterEqual(x0,60)
            self.assertLessEqual(x1,1010)
            self.assertGreaterEqual(y0,230)
            self.assertLessEqual(y1,1660)
    def test_exact_duration(self):
        self.assertEqual(FRAMES,72)
        self.assertEqual(FPS,30)
    def test_frame_dimensions(self):
        frame=make_frame(35,CONFIG)
        self.assertEqual(frame.size,(W,H))
        self.assertEqual(frame.mode,'RGB')
    def test_frames_change(self):
        bg=Image.new('RGB',(W,H),'#081222')
        a=make_frame(10,CONFIG,bg)
        b=make_frame(63,CONFIG,bg)
        self.assertNotEqual(a.tobytes(),b.tobytes())
    def test_frame_range(self):
        with self.assertRaises(ValueError):make_frame(72,CONFIG)

if __name__=='__main__':unittest.main()
