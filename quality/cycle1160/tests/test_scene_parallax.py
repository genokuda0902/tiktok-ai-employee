import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from scene_parallax import GENRES,POLICY,ROIS,SCENES,active_scene,feather_mask,transform_frame,validate

class ParallaxTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_approved_policies_only(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'s';p.write_bytes(b'video')
            import scene_parallax
            m={'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,'source_sha256':scene_parallax.sha256(p),'genre':'ai','layout_id':'eight_scene_v1'}
            self.assertEqual(len(validate(m,p,23.033333)),3)
            for g in GENRES:
                m['genre']=g;self.assertEqual(len(validate(m,p,23.033333)),3)
            for key,value in [('policy','PUBLIC'),('manual_post_only',False),('source_sha256','wrong'),('layout_id','unknown'),('asset_approval','approved')]:
                mm=dict(m);mm[key]=value
                with self.assertRaises(ValueError):validate(mm,p,23.033333)
    def test_scene_windows_disjoint_and_safe(self):
        self.assertEqual(len(SCENES),3)
        for a,b in zip(SCENES,SCENES[1:]):self.assertLess(a[2],b[1])
        for x,y,w,h in ROIS.values():
            self.assertLess(y+h,1000)
            self.assertLess(x+w,940)
    def test_mask_no_visible_rectangle_seam(self):
        m=feather_mask(840,836)
        self.assertEqual(float(m[0,100,0]),0)
        self.assertEqual(float(m[100,0,0]),0)
        self.assertAlmostEqual(float(m[400,400,0]),1)
    def test_only_active_window(self):
        self.assertIsNone(active_scene(6.2,SCENES))
        self.assertEqual(active_scene(4.0,SCENES)[0],'problem')
    def test_caption_protected_and_outside_unchanged(self):
        frame=np.zeros((1100,960,3),dtype=np.uint8)
        yy,xx=np.indices((836,840))
        frame[132:968,54:894,0]=(xx%255).astype(np.uint8)
        frame[132:968,54:894,1]=(yy%255).astype(np.uint8)
        frame[1000:]=99
        out,flag=transform_frame(frame,4.2,SCENES)
        self.assertTrue(flag)
        self.assertTrue(np.array_equal(out[1000:],frame[1000:]))
        self.assertTrue(np.array_equal(out[:132],frame[:132]))
        self.assertTrue(np.array_equal(out[:, :54],frame[:, :54]))
        self.assertGreater(float(np.abs(out.astype('float32')-frame).mean()),0.1)
    def test_no_modification_outside_window(self):
        frame=np.ones((1100,960,3),dtype=np.uint8)
        out,flag=transform_frame(frame,10.0,SCENES)
        self.assertFalse(flag)
        self.assertIs(out,frame)
    def test_ends_fade_cleanly(self):
        frame=np.random.default_rng(0).integers(0,255,(1100,960,3),dtype=np.uint8)
        out,flag=transform_frame(frame,SCENES[0][1],SCENES)
        self.assertFalse(flag)
        self.assertTrue(np.array_equal(out,frame))

if __name__=='__main__':unittest.main()
