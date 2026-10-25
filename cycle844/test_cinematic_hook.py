import hashlib
import tempfile
import unittest
from pathlib import Path
import cv2
import numpy as np
from cycle844.cinematic_hook import (
    GENRES, COPY, REQUIRED, START, END, PANEL_X, PANEL_Y, PANEL_W, PANEL_H,
    validate, make_panel, smoothstep)

class TestCinematicHook(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.source=Path(self.temp.name)/'fictional.mp4'
        self.source.write_bytes(b'fictional local media')
        self.output=Path(self.temp.name)/'output.mp4'
        self.manifest={**REQUIRED,'source_sha256':hashlib.sha256(self.source.read_bytes()).hexdigest()}
        self.photo=np.full((PANEL_H,PANEL_W,3), (80,95,120),dtype=np.uint8)
    def tearDown(self):self.temp.cleanup()
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(set(COPY),set(GENRES))
        for g in GENRES:validate(self.manifest,g,self.source,self.output)
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):validate(self.manifest,'unsupported',self.source,self.output)
    def test_fail_closed_each_rights_gate(self):
        for k in REQUIRED:
            m=self.manifest.copy();m.pop(k)
            with self.subTest(k=k),self.assertRaises(ValueError):validate(m,'ai_work',self.source,self.output)
    def test_reject_modified_source(self):
        m=self.manifest.copy();m['source_sha256']='f'*64
        with self.assertRaises(ValueError):validate(m,'ai_work',self.source,self.output)
    def test_reject_same_path(self):
        with self.assertRaises(ValueError):validate(self.manifest,'ai_work',self.source,self.source)
    def test_protected_region(self):
        self.assertEqual((START,END),(0,96))
        self.assertGreaterEqual(PANEL_X,45)
        self.assertGreaterEqual(PANEL_Y,330)
        self.assertLessEqual(PANEL_X+PANEL_W,1005)
        self.assertLessEqual(PANEL_Y+PANEL_H,1130)
    def test_frame_shape_and_motion(self):
        a=make_panel(self.photo,4);b=make_panel(self.photo,40)
        self.assertEqual(a.shape,self.photo.shape)
        self.assertGreater(np.mean(np.abs(a.astype(int)-b.astype(int))),1.0)
    def test_readable_hook_after_half_second(self):
        p=make_panel(self.photo,18)
        # Yellow/white title pixels in lower part of panel.
        roi=p[440:640,40:800]
        bright=(roi[:,:,1]>180)&(roi[:,:,2]>170)
        self.assertGreater(int(bright.sum()),1000)
    def test_reject_bad_frame_and_index(self):
        with self.assertRaises(ValueError):make_panel(np.zeros((200,200,3),np.uint8),0)
        with self.assertRaises(ValueError):make_panel(self.photo,END)
    def test_smoothstep_bounds(self):
        self.assertEqual(smoothstep(-1),0)
        self.assertEqual(smoothstep(2),1)
        self.assertAlmostEqual(smoothstep(.5),.5)
    def test_all_genre_titles_fit(self):
        from PIL import ImageFont
        from cycle844.cinematic_hook import FONT
        for genre,(title,sub) in COPY.items():
            f=ImageFont.truetype(FONT,78 if len(title)<=9 else 61)
            with self.subTest(genre=genre):
                self.assertLess(f.getlength(title),PANEL_W-70)
    def test_review_copy_no_quantified_claims(self):
        for a,b in COPY.values():
            self.assertNotIn('%',a+b)
            self.assertNotIn('100倍',a+b)
if __name__=='__main__':unittest.main()
