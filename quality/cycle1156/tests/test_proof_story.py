import tempfile
import unittest
from pathlib import Path
from proof_story import POLICY,GENRES,ROWS,totals,frame,validate,sha256,X,Y,W,H

class TestProofStory(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.src=Path(self.tmp.name)/'synthetic.mp4';self.src.write_bytes(b'fictional test media')
        self.m={'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,'source_sha256':sha256(self.src),'genre':'ai','window':[11.55,14.35]}
    def tearDown(self):self.tmp.cleanup()
    def test_10_genres(self):self.assertEqual(len(GENRES),10)
    def test_provenance_arithmetic(self):
        self.assertEqual(totals(),(46,29,75))
        self.assertEqual([a+b for _,a,b in ROWS],[20,25,30])
    def test_valid_manifest(self):self.assertEqual(validate(self.m,self.src,23.033),(11.55,14.35))
    def test_no_publication(self):
        self.m['asset_approval']='approved';self.assertRaises(ValueError,validate,self.m,self.src,23.033)
    def test_manual_post(self):
        self.m['manual_post_only']=False;self.assertRaises(ValueError,validate,self.m,self.src,23.033)
    def test_sha_pinned(self):
        self.m['source_sha256']='wrong';self.assertRaises(ValueError,validate,self.m,self.src,23.033)
    def test_window(self):
        self.m['window']=[22,25];self.assertRaises(ValueError,validate,self.m,self.src,23.033)
    def test_genre(self):
        self.m['genre']='invalid';self.assertRaises(ValueError,validate,self.m,self.src,23.033)
    def test_safe_region(self):self.assertLessEqual(Y+H,1050)
    def test_three_distinct_phases(self):
        a,b,c=(frame(self.m,i,84) for i in (8,42,77))
        self.assertEqual(a.size,(W,H))
        self.assertNotEqual(a.tobytes(),b.tobytes())
        self.assertNotEqual(b.tobytes(),c.tobytes())
    def test_ten_genre_frames(self):
        for genre in GENRES:
            self.m['genre']=genre
            self.assertEqual(frame(self.m,45,84).size,(W,H))

if __name__=='__main__':unittest.main()
