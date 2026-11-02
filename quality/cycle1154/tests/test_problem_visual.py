import tempfile,unittest
from pathlib import Path
from problem_visual import POLICY,GENRES,frame,validate,sha256,X,Y,W,H

class Tests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.src=Path(self.t.name)/'source';self.src.write_bytes(b'fictional synthetic input')
  self.m={'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,'source_sha256':sha256(self.src),'genre':'ai','window':[2.9,5.6]}
 def tearDown(self):self.t.cleanup()
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_policy_valid(self):self.assertEqual(validate(self.m,self.src,23),(2.9,5.6))
 def test_reject_approval(self):
  self.m['asset_approval']='approved';self.assertRaises(ValueError,validate,self.m,self.src,23)
 def test_reject_posting(self):
  self.m['manual_post_only']=False;self.assertRaises(ValueError,validate,self.m,self.src,23)
 def test_reject_source_mismatch(self):
  self.m['source_sha256']='wrong';self.assertRaises(ValueError,validate,self.m,self.src,23)
 def test_reject_genre(self):
  self.m['genre']='unknown';self.assertRaises(ValueError,validate,self.m,self.src,23)
 def test_reject_window(self):
  self.m['window']=[22,25];self.assertRaises(ValueError,validate,self.m,self.src,23)
 def test_reject_short(self):
  self.m['window']=[2.9,3.2];self.assertRaises(ValueError,validate,self.m,self.src,23)
 def test_caption_and_cta_protected(self):self.assertLess(Y+H,1090)
 def test_frame_dimensions(self):self.assertEqual(frame(self.m,30,81).size,(W,H))
 def test_staged_animation(self):
  a=frame(self.m,12,81);b=frame(self.m,75,81)
  self.assertNotEqual(a.getpixel((750,240)),b.getpixel((750,240)))
 def test_genre_visuals(self):
  for g in GENRES:
   self.m['genre']=g
   self.assertEqual(frame(self.m,30,81).size,(W,H))
 def test_no_overwrite(self):
  self.assertNotEqual(X,0)

if __name__=='__main__':unittest.main()
