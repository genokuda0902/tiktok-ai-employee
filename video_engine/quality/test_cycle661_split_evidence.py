"""Cycle661 tests: no user media, network, or posting."""
import unittest
from unittest.mock import patch
from pathlib import Path
from cycle661_split_evidence import GENRES, check

class FakeCapture:
    def get(self, key):
        return 920 if key == 3 else 550
    def release(self): pass

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.m={'genre':GENRES[0],'publication':'NOT_APPROVED',
                'rights':'REVIEW_ONLY_UNVERIFIED','data':'SYNTHETIC',
                'source_sha256':'test','crop':[0,0,450,355],
                'formula_roi':[258,9,110,43],'result_roi':[160,237,168,32]}
    @patch('cycle661_split_evidence.sha',return_value='test')
    @patch('cycle661_split_evidence.cv2.VideoCapture',return_value=FakeCapture())
    def test_ten_genres(self,*_):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            self.assertTrue(check({**self.m,'genre':genre},Path('dummy')))
    @patch('cycle661_split_evidence.sha',return_value='test')
    @patch('cycle661_split_evidence.cv2.VideoCapture',return_value=FakeCapture())
    def test_fail_closed(self,*_):
        for key,bad in [('rights','APPROVED'),('publication','APPROVED'),
                        ('data','REAL'),('source_sha256','bad'),
                        ('genre','other'),('crop',[0,0,999,999]),
                        ('result_roi',[499,300,50,50])]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                check({**self.m,key:bad},Path('dummy'))
if __name__=='__main__': unittest.main()
