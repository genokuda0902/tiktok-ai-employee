import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from repair_transition import validate_plan,GENRES,CAPTION_SAFE_Y,DEFAULT_START,DEFAULT_END,DEFAULT_ANCHOR

class TestTransitionRepair(unittest.TestCase):
    def test_ten_genres_declared(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_ai_work_reviewed(self):
        validate_plan('ai_work',False,522,530,532,691)
    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError): validate_plan('unknown',True,10,18,20,60)
    def test_other_genre_fails_closed_for_real_media(self):
        for g in GENRES[1:]:
            with self.subTest(genre=g), self.assertRaises(ValueError):
                validate_plan(g,False,10,18,20,60)
    def test_other_genre_synthetic_only(self):
        for g in GENRES:
            validate_plan(g,True,10,18,20,60)
    def test_anchor_must_be_clean_later(self):
        for s,e,a in [(10,18,18),(10,18,17),(10,18,25)]:
            with self.subTest(anchor=a),self.assertRaises(ValueError):
                validate_plan('ai_work',True,s,e,a,60)
    def test_no_long_overlay(self):
        with self.assertRaises(ValueError):validate_plan('ai_work',True,1,17,19,60)
    def test_caption_safe_area(self):
        self.assertEqual(CAPTION_SAFE_Y,1440)
        self.assertGreaterEqual(1920-CAPTION_SAFE_Y,480)
    def test_defaults_contiguous_with_scene_boundary(self):
        self.assertEqual((DEFAULT_START,DEFAULT_END,DEFAULT_ANCHOR),(522,530,532))

if __name__=='__main__':unittest.main()
