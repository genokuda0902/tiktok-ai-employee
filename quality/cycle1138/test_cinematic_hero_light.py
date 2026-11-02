import importlib.util
import json
import sys
import unittest
from pathlib import Path
import numpy as np

spec=importlib.util.spec_from_file_location('cinematic_hero_light',Path(__file__).with_name('cinematic_hero_light.py'))
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)

class HeroLightTests(unittest.TestCase):
    def setUp(self):
        self.manifest={'policy':m.POLICY,'asset_approval':'private_review_only','source_sha256':'abc',
                       'genre':'ai','roi':{'x':110,'y':475,'width':670,'height':500},
                       'start_frame':4,'sweep_frames':29,'color_rgb':[105,220,245],'max_alpha':0.16}
        self.media={'frames':691,'duration':23.033}
    def test_all_ten_genres(self):
        self.assertEqual(len(m.GENRES),10)
        for g in m.GENRES:
            self.manifest['genre']=g
            self.assertEqual(m.validate(self.manifest,'abc',self.media)[-1],29)
    def test_hash_fail_closed(self):
        with self.assertRaises(ValueError):m.validate(self.manifest,'not-approved',self.media)
    def test_rights_fail_closed(self):
        self.manifest['asset_approval']='public';
        with self.assertRaises(ValueError):m.validate(self.manifest,'abc',self.media)
    def test_caption_region_protected(self):
        self.manifest['roi']['y']=1150
        with self.assertRaises(ValueError):m.validate(self.manifest,'abc',self.media)
    def test_header_region_protected(self):
        self.manifest['roi']['y']=300
        with self.assertRaises(ValueError):m.validate(self.manifest,'abc',self.media)
    def test_bad_color_rejected(self):
        self.manifest['color_rgb']=[255,999,0]
        with self.assertRaises(ValueError):m.validate(self.manifest,'abc',self.media)
    def test_bad_alpha_rejected(self):
        self.manifest['max_alpha']=0.6
        with self.assertRaises(ValueError):m.validate(self.manifest,'abc',self.media)
    def test_frame_bounds(self):
        self.manifest['sweep_frames']=80
        with self.assertRaises(ValueError):m.validate(self.manifest,'abc',self.media)
    def test_light_has_soft_peak(self):
        a=np.array(m.light_rgba(320,240,0.5,(105,220,245),0.16))
        self.assertEqual(a.shape,(240,320,4));self.assertLessEqual(a[:,:,3].max(),41)
        self.assertGreater(a[:,:,3].max(),15)
    def test_light_zero_at_endpoints(self):
        for p in (0,1):self.assertEqual(np.array(m.light_rgba(160,120,p,(105,220,245),0.16))[:,:,3].max(),0)
    def test_reject_unknown_field(self):
        self.manifest['publish']=True
        with self.assertRaises(ValueError):m.validate(self.manifest,'abc',self.media)

if __name__=='__main__':unittest.main()
