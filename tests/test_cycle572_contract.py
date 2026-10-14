"""Cycle572 reusable proof contract tests. Run: python -m unittest discover -s tests -p test_cycle572_contract.py -v"""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'quality'/'cycle572'))
from scene_contract import GENRES, proof, gate, scene_config

class Cycle572Tests(unittest.TestCase):
    def test_sum(self): self.assertEqual(proof(),720)
    def test_negative_rejected(self):
        with self.assertRaises(ValueError): proof([120,-1])
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): proof([])
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_each_genre(self):
        for genre in GENRES:
            self.assertEqual(scene_config(genre)['verified_sum'],720)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): scene_config('unknown')
    def test_no_publication(self):
        with self.assertRaises(ValueError): gate({'publication':'APPROVED','auto_post':False,'synthetic':True,'rights_checked':True})
    def test_no_auto_post(self):
        with self.assertRaises(ValueError): gate({'publication':'NOT_APPROVED','auto_post':True,'synthetic':True,'rights_checked':True})
    def test_missing_rights(self):
        with self.assertRaises(ValueError): gate({'publication':'NOT_APPROVED','auto_post':False,'synthetic':True})
    def test_safe_gate(self): self.assertTrue(gate({'publication':'NOT_APPROVED','auto_post':False,'synthetic':True,'rights_checked':True}))

if __name__=='__main__':unittest.main()
