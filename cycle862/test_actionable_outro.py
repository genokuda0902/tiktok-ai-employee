import tempfile, unittest
from pathlib import Path
from PIL import Image
from actionable_outro import GENRES,ACCENTS,COPY,POLICY,ROI,FPS,TOTAL,START,N,draw,sha,smooth,validate

class OutroTests(unittest.TestCase):
 def setUp(self):self.shots=[Image.new('RGB',(414,290),'#334455'),Image.new('RGB',(414,290),'#556677')]
 def test_ten_genres(self):self.assertEqual(len(GENRES),10);self.assertEqual(set(GENRES),set(ACCENTS));self.assertEqual(set(GENRES),set(COPY))
 def test_three_steps_each(self):self.assertTrue(all(len(COPY[g][1])==3 for g in GENRES))
 def test_time(self):self.assertEqual((FPS,TOTAL,START,N,START+N-1),(30,691,631,60,690))
 def test_caption_safe(self):x,y,w,h=ROI;self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,300);self.assertLessEqual(x+w,1080);self.assertLess(y+h,1490)
 def test_review_only(self):self.assertTrue(POLICY['review_only']);self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['automatic_posting']);self.assertFalse(POLICY['external_upload']);self.assertFalse(POLICY['source_rights_reviewed'])
 def test_smooth(self):self.assertEqual(smooth(-1),0);self.assertEqual(smooth(2),1);self.assertAlmostEqual(smooth(.5),.5)
 def test_bad_frame(self):
  with self.assertRaises(ValueError):draw(-1,self.shots)
  with self.assertRaises(ValueError):draw(N,self.shots)
 def test_bad_genre(self):
  with self.assertRaises(ValueError):draw(0,self.shots,'unknown')
 def test_requires_two_shots(self):
  with self.assertRaises(ValueError):draw(0,[self.shots[0]])
 def test_synthetic_frames_all_genres(self):
  for g in GENRES:self.assertEqual(draw(59,self.shots,g).size,ROI[2:])
 def test_progressive_reveal(self):
  self.assertNotEqual(draw(0,self.shots).tobytes(),draw(58,self.shots).tobytes())
 def test_hash_gate(self):
  with tempfile.TemporaryDirectory() as td:
   src=Path(td)/'source.mp4';src.write_bytes(b'synthetic');out=Path(td)/'out.mp4'
   with self.assertRaises(ValueError):validate(src,out,{},'ai_work')
   with self.assertRaises(ValueError):validate(src,out,{**POLICY,'source_sha256':'wrong'},'ai_work')
   self.assertEqual(validate(src,out,{**POLICY,'source_sha256':sha(src)},'ai_work'),(src,out))
   out.write_bytes(b'x')
   with self.assertRaises(ValueError):validate(src,out,{**POLICY,'source_sha256':sha(src)},'ai_work')

if __name__=='__main__':unittest.main()