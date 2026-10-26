import tempfile, unittest
from pathlib import Path
from cinematic_laptop import GENRES,TITLES,POLICY,ROI,COUNT,START,draw_frame,ease,validate,sha256
class CinematicLaptopTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(GENRES),10);self.assertEqual(set(GENRES),set(TITLES))
 def test_safe_caption_boundary(self):self.assertLess(ROI[1]+ROI[3],1490)
 def test_scene_bounds(self):self.assertEqual((START,START+COUNT-1),(507,587))
 def test_size(self):self.assertEqual(draw_frame(0).size,(1080,1120))
 def test_all_genres(self):
  for genre in GENRES:self.assertEqual(draw_frame(35,genre).size,(1080,1120))
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):draw_frame(0,'unknown')
 def test_invalid_frame(self):
  for f in (-1,COUNT):
   with self.assertRaises(ValueError):draw_frame(f)
 def test_frame_changes(self):self.assertNotEqual(draw_frame(4).tobytes(),draw_frame(70).tobytes())
 def test_ease(self):self.assertEqual((ease(-1),ease(2)),(0,1));self.assertLess(ease(.1),ease(.9))
 def test_fail_closed(self):self.assertTrue(POLICY['review_only']);self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['external_upload']);self.assertFalse(POLICY['automatic_posting'])
 def test_manifest(self):
  with tempfile.TemporaryDirectory() as td:
   src=Path(td)/'input.mp4';src.write_bytes(b'fictional synthetic media');out=Path(td)/'output.mp4'
   good={**POLICY,'source_sha256':sha256(src)}
   self.assertEqual(validate(src,out,good,'ai_work'),(src,out))
   with self.assertRaises(ValueError):validate(src,out,{**good,'source_sha256':'wrong'},'ai_work')
   out.write_bytes(b'x')
   with self.assertRaises(ValueError):validate(src,out,good,'ai_work')
 def test_missing_source(self):
  with self.assertRaises(FileNotFoundError):validate('/no/such/input.mp4','/tmp/new.mp4',{},'ai_work')
if __name__=='__main__':unittest.main()