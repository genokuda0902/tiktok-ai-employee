"""Tests for cycle861 common 10-genre evidence montage; synthetic-only fixtures."""
import tempfile, unittest
from pathlib import Path
from PIL import Image
from evidence_montage import (GENRES,ACCENTS,POLICY,ROI,N,START,TOTAL,CLIPS,
                              ease,draw_scene,validate_policy,digest)

class MontageTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRES),10);self.assertEqual(set(GENRES),set(ACCENTS))
    def test_timing(self):self.assertEqual((START,N,START+N-1,TOTAL),(89,81,169,691))
    def test_safe_roi(self):
        x,y,w,h=ROI;self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,315)
        self.assertLessEqual(x+w,1080);self.assertLessEqual(y+h,1490)
    def test_two_real_sources(self):self.assertEqual(len(CLIPS),2);self.assertNotEqual(CLIPS[0]['start'],CLIPS[1]['start'])
    def test_policy(self):
        self.assertTrue(POLICY['review_only']);self.assertFalse(POLICY['publication_approved'])
        self.assertFalse(POLICY['automatic_posting']);self.assertFalse(POLICY['external_upload'])
    def test_ease(self):
        self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1)
        self.assertAlmostEqual(ease(.5),.5)
    def test_fail_closed_hash(self):
        with tempfile.TemporaryDirectory() as td:
            s=Path(td)/'input.mp4';s.write_bytes(b'synthetic')
            o=Path(td)/'out.mp4'
            with self.assertRaises(ValueError):validate_policy({},s,o,'ai_work')
            with self.assertRaises(ValueError):validate_policy({**POLICY,'source_sha256':'bad'},s,o,'ai_work')
            self.assertEqual(validate_policy({**POLICY,'source_sha256':digest(s)},s,o,'ai_work'),(s,o))
            o.write_bytes(b'x')
            with self.assertRaises(ValueError):validate_policy({**POLICY,'source_sha256':digest(s)},s,o,'ai_work')
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):draw_scene(0,[[],[]],'other')
    def test_invalid_frame(self):
        with self.assertRaises(ValueError):draw_scene(-1,[[],[]])
        with self.assertRaises(ValueError):draw_scene(N,[[],[]])
    def test_all_genres_synthetic_frame(self):
        with tempfile.TemporaryDirectory() as td:
            paths=[]
            for i in range(2):
                p=Path(td)/f'synthetic_{i}.png'
                Image.new('RGB',(760,510),('steelblue' if i==0 else 'seagreen')).save(p)
                paths.append([p]*44)
            for genre in GENRES:
                im=draw_scene(0,paths,genre)
                self.assertEqual(im.size,ROI[2:])
                self.assertEqual(im.mode,'RGB')
            for i in (0,38,39,41,44,45,80):
                self.assertEqual(draw_scene(i,paths).size,ROI[2:])

if __name__=='__main__':unittest.main()