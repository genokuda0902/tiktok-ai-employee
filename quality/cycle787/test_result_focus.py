import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from result_focus import validate,easing,render_overlay_frame
CFG=json.loads((Path(__file__).parent/'config.json').read_text())

class ResultFocusTests(unittest.TestCase):
    def test_valid(self): self.assertTrue(validate(CFG))
    def test_bad_safe_area(self):
        c=copy.deepcopy(CFG);c['bbox']=[900,1090,1050,1222]
        with self.assertRaises(AssertionError):validate(c)
    def test_bad_duration(self):
        c=copy.deepcopy(CFG);c['end']=100
        with self.assertRaises(AssertionError):validate(c)
    def test_text_border_protection(self):
        c=copy.deepcopy(CFG);c['bbox']=[520,1120,760,1180]
        with self.assertRaises(AssertionError):validate(c)
    def test_no_approval_escalation(self):
        c=copy.deepcopy(CFG);c['publication_approved']=True
        with self.assertRaises(AssertionError):validate(c)
    def test_easing_monotonic(self):
        xs=[easing(i/100) for i in range(101)]
        self.assertEqual(xs,sorted(xs))
    def test_outside_time_transparent(self):
        im=render_overlay_frame(CFG,CFG['start']-.1)
        self.assertIsNone(im.getbbox())
    def test_active_pixels_only_inside_focus(self):
        im=render_overlay_frame(CFG,16.0)
        self.assertIsNotNone(im.getbbox())
        self.assertEqual(im.getpixel((500,600))[3],0)
        self.assertEqual(im.getpixel((700,1360))[3],0)

if __name__=='__main__':unittest.main()
