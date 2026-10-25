import unittest
import numpy as np
from PIL import Image
from scene2_workflow_focus import (GENRES,POLICY,PANEL,WINDOW,beat,ease,make_panel,composite,validate)

class TestWorkflowFocus(unittest.TestCase):
    def setUp(self):
        self.photo=Image.new('RGB',(908,758),(83,112,137))
    def test_ten_genres(self):self.assertEqual(len(set(GENRES)),10)
    def test_beat_boundaries(self):
        self.assertEqual([beat(i,81) for i in (0,26,27,53,54,80)],[0,0,1,1,2,2])
    def test_invalid_frames(self):
        for f,t in [(-1,81),(81,81),(0,0),(0,2)]:
            with self.assertRaises(ValueError):beat(f,t)
    def test_motion_bounds(self):
        self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1)
    def test_all_genre_panels(self):
        for genre in GENRES:
            for i in (0,27,54):
                self.assertEqual(make_panel(self.photo,i,81,genre).shape,(758,908,3))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):make_panel(self.photo,0,81,'unknown')
    def test_preserves_heading_and_captions(self):
        src=np.random.default_rng(2).integers(0,256,(1920,1080,3),dtype=np.uint8)
        panel=make_panel(self.photo,40,81,'ai_work')
        out=composite(src,panel)
        x0,y0,x1,y1=PANEL
        np.testing.assert_array_equal(src[:y0],out[:y0])
        np.testing.assert_array_equal(src[y1:],out[y1:])
        np.testing.assert_array_equal(src[y0:y1,:x0],out[y0:y1,:x0])
        np.testing.assert_array_equal(src[y0:y1,x1:],out[y0:y1,x1:])
        self.assertGreater(np.abs(out[y0:y1,x0:x1].astype(int)-src[y0:y1,x0:x1].astype(int)).mean(),10)
    def test_strict_policy(self):
        with self.assertRaises(FileNotFoundError):validate('/missing-source.mp4','/tmp/x.mp4',{},'ai_work',WINDOW,108)
    def test_bad_panel_dimensions(self):
        with self.assertRaises(ValueError):composite(np.zeros((1920,1080,3),dtype=np.uint8),np.zeros((2,2,3),dtype=np.uint8))
    def test_policy_review_only(self):
        self.assertTrue(POLICY['review_only'])
        self.assertFalse(POLICY['publication_approved'])
        self.assertFalse(POLICY['automatic_posting'])
        self.assertFalse(POLICY['external_upload'])
        self.assertFalse(POLICY['source_rights_reviewed'])

if __name__=='__main__':unittest.main()