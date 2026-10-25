import unittest
import numpy as np
from PIL import Image
from scene8_evidence_reveal import (GENRES,POLICY,PANEL,WINDOW,EVIDENCE,
                                    stage,render_panel,composite,validate)

class TestScene8EvidenceReveal(unittest.TestCase):
    def setUp(self):
        self.shots=[Image.new('RGB',(864,486),(220,228,238)),Image.new('RGB',(864,486),(235,245,250))]
    def test_ten_genres(self):self.assertEqual(len(set(GENRES)),10)
    def test_beat_bounds(self):
        self.assertEqual([stage(i,103) for i in (0,33,34,68,69,102)],[0,0,0,1,2,2])
    def test_reject_bad_frame(self):
        for f in (-1,103):
            with self.assertRaises(ValueError):stage(f,103)
    def test_all_genre_panels(self):
        for g in GENRES:
            self.assertEqual(render_panel(self.shots,45,103,g).shape,(758,908,3))
    def test_reject_unknown_genre(self):
        with self.assertRaises(KeyError):render_panel(self.shots,0,103,'unknown')
    def test_caption_and_heading_protected(self):
        f=np.zeros((1920,1080,3),np.uint8);f[:430]=17;f[1300:]=29
        o=composite(f,self.shots,15,103,'ai_work')
        self.assertTrue(np.all(o[:430]==17))
        self.assertTrue(np.all(o[1300:]==29))
        self.assertTrue(np.all(o[476:1234,86:994]!=0) is False or o[700,500].sum()>0)
    def test_fail_closed_missing_file(self):
        with self.assertRaises(FileNotFoundError):validate('/not/here.mp4','/tmp/new.mp4',{},'ai_work',WINDOW,EVIDENCE)
    def test_review_only_policy(self):
        self.assertFalse(POLICY['publication_approved'])
        self.assertFalse(POLICY['automatic_posting'])
        self.assertFalse(POLICY['external_upload'])
        self.assertFalse(POLICY['source_rights_reviewed'])
    def test_no_fake_metrics(self):
        import inspect,scene8_evidence_reveal
        src=inspect.getsource(scene8_evidence_reveal.render_panel)
        for bad in ('10倍','90%削減','実測時短'):
            self.assertNotIn(bad,src)

if __name__=='__main__':unittest.main()