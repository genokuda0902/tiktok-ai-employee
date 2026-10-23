import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from hook_motion import (validate, synthetic_source, render_frame, WIDTH, HEIGHT,
                         LEFT_CARD, RIGHT_CARD, PHOTO_ROI, SHEET_ROI, NFRAMES)
CFG=json.loads((Path(__file__).parent/'config.json').read_text())

class HookTests(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(CFG))
    def test_ten_genres(self):self.assertEqual(len(set(CFG['genres'])),10)
    def test_fail_closed(self):
        for key in ('rights_reviewed','employee_approved','publication_approved'):
            x=copy.deepcopy(CFG);x[key]=True
            with self.assertRaises(ValueError):validate(x)
    def test_mode(self):
        x=copy.deepcopy(CFG);x['mode']='publish'
        with self.assertRaises(ValueError):validate(x)
    def test_fps(self):
        x=copy.deepcopy(CFG);x['fps']=29
        with self.assertRaises(ValueError):validate(x)
    def test_margin(self):
        x=copy.deepcopy(CFG);x['safe_margin_px']=30
        with self.assertRaises(ValueError):validate(x)
    def test_frame_count(self):
        x=copy.deepcopy(CFG);x['frame_count']=95
        with self.assertRaises(ValueError):validate(x)
    def test_size(self):self.assertEqual(synthetic_source().size,(WIDTH,HEIGHT))
    def test_frame_bounds(self):
        for index in (-1,NFRAMES):
            with self.assertRaises(ValueError):render_frame(synthetic_source(),index)
    def test_motion_changes_pixels(self):
        src=synthetic_source()
        before=render_frame(src,0)
        active=render_frame(src,32)
        self.assertNotEqual(before.tobytes(),active.tobytes())
    def test_no_outside_changes(self):
        src=synthetic_source()
        out=render_frame(src,32)
        # Header and disclosure/CTA lanes must remain pixel-identical.
        for box in [(0,0,WIDTH,450),(0,1100,WIDTH,HEIGHT)]:
            self.assertEqual(src.crop(box).tobytes(),out.crop(box).tobytes())
    def test_roi_inside_cards(self):
        for roi,card in [(PHOTO_ROI,LEFT_CARD),(SHEET_ROI,RIGHT_CARD)]:
            self.assertTrue(card[0]<roi[0]<roi[2]<card[2])
            self.assertTrue(card[1]<roi[1]<roi[3]<card[3])

if __name__=='__main__':unittest.main()
