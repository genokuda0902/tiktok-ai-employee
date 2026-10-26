import tempfile,unittest
from pathlib import Path
from PIL import Image
from proof_compare import GENRES,COPY,ACCENTS,POLICY,ROI,COUNT,START,draw,ease,validate,sha256
class ProofTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(GENRES),10);self.assertEqual(set(GENRES),set(COPY));self.assertEqual(set(GENRES),set(ACCENTS))
 def test_no_unsupported_genre(self):
  with self.assertRaises(ValueError):draw(0,'bad')
 def test_frame_boundaries(self):
  for f in (-1,COUNT):
   with self.assertRaises(ValueError):draw(f)
 def test_subtitle_safe_area(self):self.assertLess(ROI[1]+ROI[3],1490)
 def test_scene_bounds(self):self.assertEqual((START,START+COUNT-1),(425,506))
 def test_render_dimensions(self):self.assertEqual(draw(40).size,(1000,1090))
 def test_all_genres_render(self):
  for genre in GENRES:self.assertEqual(draw(55,genre).size,(1000,1090))
 def test_temporal_change(self):
  a=draw(5);b=draw(65);self.assertNotEqual(a.tobytes(),b.tobytes())
 def test_factual_example(self):self.assertEqual(COPY['ai_work'][1:3],('17','18'))
 def test_nonquantitative_other_genres(self):
  for genre in GENRES[1:]:self.assertEqual(COPY[genre][1:3],('未確認','確認済') if genre!='romance' else ('推測','確認'))
 def test_smooth_monotonic(self):self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1);self.assertLess(ease(.2),ease(.8))
 def test_policy_closed(self):self.assertTrue(POLICY['review_only']);self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['automatic_posting']);self.assertFalse(POLICY['external_upload'])
 def test_pin_and_overwrite(self):
  with tempfile.TemporaryDirectory() as td:
   s=Path(td)/'source';s.write_bytes(b'synthetic');o=Path(td)/'out'
   good={**POLICY,'source_sha256':sha256(s)}
   self.assertEqual(validate(s,o,good,'ai_work'),(s,o))
   with self.assertRaises(ValueError):validate(s,o,{**good,'source_sha256':'bad'},'ai_work')
   o.write_text('x')
   with self.assertRaises(ValueError):validate(s,o,good,'ai_work')
 def test_missing_source(self):
  with self.assertRaises(FileNotFoundError):validate('/nonexistent','/tmp/out',{},'ai_work')
if __name__=='__main__':unittest.main()