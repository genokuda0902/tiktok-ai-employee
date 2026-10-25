import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import cv2
from three_beat_capture import GENRES,POLICY,SHOTS,shot_index,crop_focus,make_badge,composite,validate

class TestThreeBeat(unittest.TestCase):
    def test_genres(self):self.assertEqual(len(GENRES),10)
    def test_no_publication(self):self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['automatic_posting'])
    def test_rights_fail_closed(self):self.assertFalse(POLICY['source_rights_reviewed'])
    def test_shot0(self):self.assertEqual(shot_index(0,86),0)
    def test_shot1(self):self.assertEqual(shot_index(29,86),1)
    def test_shot2(self):self.assertEqual(shot_index(58,86),2)
    def test_last(self):self.assertEqual(shot_index(85,86),2)
    def test_out_of_range(self):
        with self.assertRaises(ValueError):shot_index(86,86)
    def test_crops(self):
        im=np.zeros((900,1440,3),np.uint8)
        for _,z,pt in SHOTS:self.assertEqual(crop_focus(im,z,pt,(908,758)).shape,(758,908,3))
    def test_badges(self):
        for i,(txt,_,_) in enumerate(SHOTS):self.assertEqual(make_badge(txt,i+1,888).shape,(86,888,4))
    def test_protect_header_and_caption(self):
        base=np.full((1920,1080,3),17,np.uint8);cap=np.full((900,1440,3),255,np.uint8)
        badges=[make_badge(s[0],i+1,888) for i,s in enumerate(SHOTS)]
        out=composite(base,cap,40,86,badges)
        self.assertTrue(np.array_equal(out[:475],base[:475]))
        self.assertTrue(np.array_equal(out[1235:],base[1235:]))
    def test_missing_files_rejected(self):
        with self.assertRaises(FileNotFoundError):validate('/bad/source','/bad/capture','/tmp/out',{},'ai_work',(0,1))
    def test_bad_genre_rejected(self):
        with self.assertRaises(ValueError):validate('/bad/source','/bad/capture','/tmp/out',{},'bad',(0,1))

if __name__=='__main__':unittest.main()