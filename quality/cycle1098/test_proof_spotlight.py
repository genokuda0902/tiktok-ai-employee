import unittest
from proof_spotlight import PALETTES, RECTS, COUNT, START, make_overlay, validate, smooth

BASE={'genre':'ai_work','synthetic_scenario':True,'review_only':True,
      'rights_status':'unverified','contains_private_data':False}
class SpotlightTests(unittest.TestCase):
    def test_ten_genres(self):
        for genre in PALETTES: self.assertTrue(validate({**BASE,'genre':genre}))
    def test_fail_closed(self):
        for k,v in [('review_only',False),('synthetic_scenario',False),('rights_status','approved'),('contains_private_data',True)]:
            with self.assertRaises(ValueError): validate({**BASE,k:v})
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError): validate({**BASE,'genre':'other'})
    def test_safe_timeline(self): self.assertLess(START+COUNT,609)
    def test_safe_geometry(self):
        for x0,y0,x1,y1 in RECTS:
            self.assertLess(x0,x1);self.assertLess(y0,y1);self.assertLess(y1,1490)
    def test_transparent_at_start(self): self.assertEqual(make_overlay(0,'ai_work').getbbox(),None)
    def test_visible_mid_stage(self):
        for t in (12,36,60): self.assertIsNotNone(make_overlay(t,'ai_work').getbbox())
    def test_reject_bad_frame(self):
        for t in (-1,COUNT):
            with self.assertRaises(ValueError): make_overlay(t,'ai_work')
    def test_smooth_bounded(self):
        self.assertEqual(smooth(-1),0);self.assertEqual(smooth(2),1)
    def test_dimensions(self): self.assertEqual(make_overlay(15,'travel').size,(1080,920))
if __name__=='__main__': unittest.main()
