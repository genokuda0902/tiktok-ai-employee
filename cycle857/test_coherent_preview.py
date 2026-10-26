import unittest
from pathlib import Path
import tempfile
import numpy as np
from coherent_preview import GENRES,POLICY,WINDOW,COVER,PREVIEW_CROP,draw_panel,preview_crop_from_frame,validate,sha256

class CoherentPreviewTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_unique_genres(self):self.assertEqual(len(set(GENRES)),10)
    def test_three_beats_all_genres(self):
        a=np.zeros((448,607,3),dtype=np.uint8)
        for g in GENRES:
            for b in range(3):
                out=draw_panel(a,g,b)
                self.assertEqual(out.shape,(COVER[3]-COVER[1],COVER[2]-COVER[0],3))
    def test_distinct_highlights(self):
        a=np.full((448,607,3),127,dtype=np.uint8)
        self.assertFalse(np.array_equal(draw_panel(a,'ai_work',0),draw_panel(a,'ai_work',2)))
    def test_crop_actual_frame(self):
        a=np.zeros((1920,1080,3),dtype=np.uint8)
        x0,y0,x1,y1=PREVIEW_CROP
        a[y0:y1,x0:x1]=[11,22,33]
        c=preview_crop_from_frame(a,PREVIEW_CROP)
        self.assertEqual(c.shape,(y1-y0,x1-x0,3))
        self.assertEqual(c[0,0].tolist(),[33,22,11])
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):draw_panel(np.zeros((448,607,3),dtype=np.uint8),'unknown',0)
    def test_unknown_beat_rejected(self):
        with self.assertRaises(ValueError):draw_panel(np.zeros((448,607,3),dtype=np.uint8),'ai_work',3)
    def test_review_only_policy(self):
        for k in ('publication_approved','automatic_posting','external_upload','source_rights_reviewed','contains_personal_data'):
            self.assertFalse(POLICY[k])
        self.assertTrue(POLICY['review_only'])
    def test_window_not_subtitle(self):
        self.assertEqual(WINDOW,(170,251))
        self.assertLessEqual(COVER[3],1250)
        self.assertGreaterEqual(COVER[1],330)
    def test_invalid_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):validate(Path(d)/'no.mp4',Path(d)/'out.mp4',{},'ai_work',WINDOW,362,PREVIEW_CROP)
    def test_bad_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fake.mp4';p.write_bytes(b'not video')
            with self.assertRaises(ValueError):validate(p,Path(d)/'out.mp4',{},'ai_work',WINDOW,362,PREVIEW_CROP)
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'same.mp4';p.write_bytes(b'bad')
            with self.assertRaises(ValueError):validate(p,p,{**POLICY,'source_sha256':sha256(p)},'ai_work',WINDOW,362,PREVIEW_CROP)
if __name__=='__main__':unittest.main()