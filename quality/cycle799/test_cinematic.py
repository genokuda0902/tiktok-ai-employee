import unittest
import numpy as np
from cinematic import GENRES,SCENES,PANEL,SOURCE_VISUAL,scene_at,make_overlay,reframe
class CinematicTests(unittest.TestCase):
    def test_genres(self): self.assertEqual(len(GENRES),10)
    def test_timeline(self): self.assertEqual(sum(SCENES),429)
    def test_scene_boundaries(self):
        self.assertEqual(scene_at(0),0);self.assertEqual(scene_at(57),1)
        self.assertEqual(scene_at(428),7)
        with self.assertRaises(ValueError):scene_at(429)
    def test_subtitle_safety(self):
        self.assertLessEqual(PANEL[1]+PANEL[3],1530)
    def test_crop_bounds(self):
        x,y,x2,y2=SOURCE_VISUAL
        self.assertTrue(0<=x<x2<=PANEL[2] and 0<=y<y2<=PANEL[3])
    def test_overlay_alpha(self):
        o=make_overlay(0,'science');self.assertEqual(o.shape,(1050,1010,4))
        self.assertTrue(np.max(o[:,:,3])>0)
    def test_reframe(self):
        o=make_overlay(0,'science');p=np.zeros((1050,1010,3),dtype=np.uint8)
        a=reframe(p,0,0,'science',o)
        self.assertEqual(a.shape,p.shape)
        self.assertGreater(int(a.sum()),0)
    def test_unknown_genre(self):
        with self.assertRaises(KeyError):make_overlay(0,'invalid')
if __name__=='__main__':unittest.main()
