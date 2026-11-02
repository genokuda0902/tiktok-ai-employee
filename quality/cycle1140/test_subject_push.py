import importlib.util
import sys
import unittest
from pathlib import Path
import numpy as np
from PIL import Image
spec=importlib.util.spec_from_file_location('subject_push',Path(__file__).with_name('subject_push.py'))
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
class PushTests(unittest.TestCase):
    def setUp(self):
        self.m={'policy':m.POLICY,'asset_approval':'private_review_only','source_sha256':'abc','genre':'ai',
                'roi':{'x':110,'y':475,'width':670,'height':500},'start_frame':3,'motion_frames':56,
                'max_zoom':1.08,'feather_px':32,'title_guard_px':90}
        self.spec={'frames':691,'duration':23.033}
    def test_all_ten_genres(self):
        self.assertEqual(len(m.GENRES),10)
        for g in m.GENRES:
            self.m['genre']=g;self.assertEqual(m.validate(self.m,'abc',self.spec)[-1],56)
    def test_hash_fail_closed(self):
        with self.assertRaises(ValueError):m.validate(self.m,'bad',self.spec)
    def test_approval_fail_closed(self):
        self.m['asset_approval']='public'
        with self.assertRaises(ValueError):m.validate(self.m,'abc',self.spec)
    def test_header_protected(self):
        self.m['roi']['y']=250
        with self.assertRaises(ValueError):m.validate(self.m,'abc',self.spec)
    def test_caption_protected(self):
        self.m['roi']['y']=1200
        with self.assertRaises(ValueError):m.validate(self.m,'abc',self.spec)
    def test_zoom_limit(self):
        self.m['max_zoom']=1.5
        with self.assertRaises(ValueError):m.validate(self.m,'abc',self.spec)
    def test_frame_bounds(self):
        self.m['motion_frames']=200
        with self.assertRaises(ValueError):m.validate(self.m,'abc',self.spec)
    def test_reject_unknown_manifest(self):
        self.m['auto_post']=True
        with self.assertRaises(ValueError):m.validate(self.m,'abc',self.spec)
    def test_motion_identity_at_boundaries(self):
        self.assertAlmostEqual(m.eased_zoom(0,1.08),1)
        self.assertAlmostEqual(m.eased_zoom(1,1.08),1)
        self.assertAlmostEqual(m.eased_zoom(.5,1.08),1.08)
    def test_overlay_feather(self):
        img=Image.new('RGB',(800,900),(80,90,100))
        out=np.array(m.local_frame(img,(110,475,670,400),1.08,32,90))
        self.assertEqual(out.shape,(400,670,4));self.assertEqual(out[0,0,3],0)
        self.assertEqual(out[200,335,3],255);self.assertEqual(out[70,335,3],0)
    def test_missing_title_guard(self):
        self.m.pop('title_guard_px')
        with self.assertRaises(ValueError):m.validate(self.m,'abc',self.spec)
    def test_bad_feather(self):
        self.m['feather_px']=0
        with self.assertRaises(ValueError):m.validate(self.m,'abc',self.spec)
if __name__=='__main__':unittest.main()
