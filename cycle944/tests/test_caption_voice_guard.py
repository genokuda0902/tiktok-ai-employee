import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from caption_voice_guard import (GENRE_PRESETS,groups,scene_for_frame,select_repairs,patch_frame,text_visibility)
import numpy as np

class CaptionGuardTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_PRESETS),10)
        self.assertEqual(len(set(GENRE_PRESETS)),10)
    def test_groups(self):self.assertEqual(groups([1,2,5,7,8]),[[1,2],[5],[7,8]])
    def test_scene_cut(self):
        self.assertEqual(scene_for_frame(86),0)
        self.assertEqual(scene_for_frame(87),1)
    def test_dim_voice_gap(self):
        vis=[.06,.06,.001,.001,.06,.06];db=[-15]*6
        self.assertEqual(select_repairs(vis,db,cuts=(0,6)),{2:1,3:4})
    def test_silence_not_filled(self):
        vis=[.06,.001,.001,.06];db=[-15,-65,-65,-15]
        self.assertEqual(select_repairs(vis,db,cuts=(0,4)),{})
    def test_long_gap_not_filled(self):
        vis=[.06]+[.001]*6+[.06];db=[-15]*8
        self.assertEqual(select_repairs(vis,db,cuts=(0,8)),{})
    def test_cut_not_crossed(self):
        vis=[.06,.001,.001,.06];db=[-15]*4
        self.assertEqual(select_repairs(vis,db,cuts=(0,2,4)),{})
    def test_no_reference(self):
        vis=[.001]*5;db=[-15]*5
        self.assertEqual(select_repairs(vis,db,cuts=(0,5)),{})
    def test_10_genres_repair(self):
        vis=[.06,.002,.002,.06];db=[-15]*4
        for th in GENRE_PRESETS.values():
            self.assertEqual(select_repairs(vis,db,threshold=th,cuts=(0,4)),{1:0,2:3})
    def test_patch_outside_unchanged(self):
        frame=np.zeros((1920,1080,3),dtype=np.uint8)
        ref=np.full_like(frame,255)
        out=patch_frame(frame,ref)
        self.assertEqual(int(out[100,100,0]),0)
        self.assertEqual(int(out[1700,500,0]),0)
        self.assertGreater(int(out[1500,500,0]),220)
    def test_visibility(self):
        f=np.zeros((1920,1080,3),dtype=np.uint8)
        self.assertEqual(text_visibility(f),0)
        f[1490:1625,250:820]=255
        self.assertAlmostEqual(text_visibility(f),1.)

if __name__=='__main__':unittest.main()
