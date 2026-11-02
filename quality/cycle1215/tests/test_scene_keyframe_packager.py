import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from scene_keyframe_packager import GENRES,validate,verify_keyframes

class TestScenePackaging(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES: self.assertTrue(validate((30,60),90,genre))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError): validate((30,),90,'unknown')
    def test_reject_duplicate_boundary(self):
        with self.assertRaises(ValueError): validate((30,30),90,'ai')
    def test_reject_unsorted_boundary(self):
        with self.assertRaises(ValueError): validate((60,30),90,'ai')
    def test_reject_negative_boundary(self):
        with self.assertRaises(ValueError): validate((-1,30),90,'ai')
    def test_reject_end_boundary(self):
        with self.assertRaises(ValueError): validate((30,89),90,'ai')
    def test_reject_short_video(self):
        with self.assertRaises(ValueError): validate((15,),30,'ai')
    def test_reject_empty_boundaries(self):
        with self.assertRaises(ValueError): validate((),90,'ai')
    def test_reject_non_integer(self):
        with self.assertRaises(ValueError): validate((30.0,),90,'ai')
    def test_keyframe_alignment(self):
        self.assertTrue(verify_keyframes([0,1,2],(30,60)))
    def test_keyframe_tolerance(self):
        self.assertTrue(verify_keyframes([0,1.005,2.01],(30,60)))
    def test_keyframe_missing(self):
        with self.assertRaises(ValueError): verify_keyframes([0,2],(30,60))

if __name__=='__main__': unittest.main()
