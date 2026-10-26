import tempfile, unittest
from pathlib import Path
from clean_hook import COUNT,START,FRAMES,GENRES,HOOKS,POLICY,ROI,LAYOUT,draw_frame,layout_ok,intersects,contract,sha256,ease
class CleanHookTests(unittest.TestCase):
 def test_ten_distinct_genres(self):self.assertEqual(len(GENRES),10);self.assertEqual(len(HOOKS),10);self.assertEqual(len(set(HOOKS.values())),10)
 def test_opening_duration(self):self.assertEqual((START,COUNT,FRAMES),(0,89,691))
 def test_caption_safety(self):self.assertLess(ROI[1]+ROI[3],1490)
 def test_no_text_overlap(self):self.assertTrue(layout_ok())
 def test_all_regions_disjoint(self):
  b=list(LAYOUT.values());self.assertTrue(all(not intersects(x,y) for i,x in enumerate(b) for y in b[i+1:]))
 def test_first_frame(self):self.assertEqual(draw_frame(0).size,(1080,1120))
 def test_motion(self):self.assertNotEqual(draw_frame(1).tobytes(),draw_frame(80).tobytes())
 def test_each_genre(self):
  for g in GENRES:self.assertEqual(draw_frame(75,g).size,(1080,1120))
 def test_bad_genre(self):
  with self.assertRaises(ValueError):draw_frame(0,'other')
 def test_bad_frames(self):
  for f in (-1,COUNT):
   with self.assertRaises(ValueError):draw_frame(f)
 def test_ease(self):self.assertEqual((ease(-1),ease(3)),(0,1))
 def test_fail_closed(self):self.assertTrue(POLICY['review_only']);self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['external_upload']);self.assertFalse(POLICY['automatic_posting'])
 def test_manifest(self):
  with tempfile.TemporaryDirectory() as td:
   src=Path(td)/'source.mp4';src.write_bytes(b'fictional data');out=Path(td)/'out.mp4';good={**POLICY,'source_sha256':sha256(src)}
   self.assertEqual(contract(src,out,good,'ai_work'),(src,out))
   with self.assertRaises(ValueError):contract(src,out,{**good,'source_sha256':'bad'},'ai_work')
   out.write_bytes(b'x')
   with self.assertRaises(ValueError):contract(src,out,good,'ai_work')
 def test_missing_source(self):
  with self.assertRaises(FileNotFoundError):contract('/no/file.mp4','/tmp/out.mp4',{},'ai_work')
if __name__=='__main__':unittest.main()
