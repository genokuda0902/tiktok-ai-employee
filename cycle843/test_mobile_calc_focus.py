import hashlib
import tempfile
import unittest
from pathlib import Path
import cv2
import numpy as np
from cycle843.mobile_calc_focus import (
    GENRES, REQUIRED, CROPS, START, END, PANEL_X, PANEL_Y, PANEL_W, PANEL_H,
    ZOOM, frame_panel, validate)

class TestMobileFocus(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.source=Path(self.t.name)/'dummy.mp4'
        self.source.write_bytes(b'fictional dummy video')
        self.output=Path(self.t.name)/'out.mp4'
        self.manifest={**REQUIRED,'source_sha256':hashlib.sha256(self.source.read_bytes()).hexdigest()}

    def tearDown(self): self.t.cleanup()

    def test_all_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES: validate(self.manifest,g,self.source,self.output)

    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError): validate(self.manifest,'unknown',self.source,self.output)

    def test_fail_closed_rights(self):
        for k in REQUIRED:
            m=self.manifest.copy();m.pop(k)
            with self.assertRaises(ValueError):validate(m,'ai_work',self.source,self.output)

    def test_reject_bad_hash(self):
        m=self.manifest.copy();m['source_sha256']='0'*64
        with self.assertRaises(ValueError):validate(m,'ai_work',self.source,self.output)

    def test_reject_same_path(self):
        with self.assertRaises(ValueError):validate(self.manifest,'ai_work',self.source,self.source)

    def test_geometry_is_inside_safe_image_region(self):
        self.assertEqual((START,END),(170,249))
        self.assertGreaterEqual(PANEL_X,45)
        self.assertGreaterEqual(PANEL_Y,370)
        self.assertLessEqual(PANEL_X+PANEL_W,1005)
        self.assertLessEqual(PANEL_Y+PANEL_H,1130)
        self.assertGreater(min(ZOOM),1.9)
        for x,y,w,h in CROPS:
            self.assertGreaterEqual(min(x,y),0)
            self.assertLessEqual(x+w,1080)
            self.assertLessEqual(y+h,1920)

    def test_panel_from_synthetic_frame(self):
        frame=np.zeros((1920,1080,3),dtype=np.uint8)
        frame[680:890,90:560]=(20,100,220)
        frame[680:890,460:930]=(80,220,60)
        a=frame_panel(frame,0)
        b=frame_panel(frame,78)
        self.assertEqual(a.shape,(470,930,3))
        self.assertGreater(np.abs(a.astype(int)-b.astype(int)).sum(),100000)

    def test_reject_bad_frame(self):
        with self.assertRaises(ValueError):frame_panel(np.zeros((100,100,3),dtype=np.uint8),0)
        with self.assertRaises(ValueError):frame_panel(np.zeros((1920,1080,3),dtype=np.uint8),79)

if __name__=='__main__':unittest.main()
