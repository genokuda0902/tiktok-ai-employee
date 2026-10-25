import unittest,hashlib
from editorial_core import W,H,FPS,FRAMES,GENRES,POLICY,SCENES,render,validate
class Cycle847Tests(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for g in GENRES:validate(g,POLICY)
 def test_8_scenes(self):self.assertEqual(len(SCENES),8)
 def test_timeline(self):self.assertEqual(sum(FRAMES),691)
 def test_native_resolution(self):self.assertEqual(render(0).size,(1080,1920))
 def test_distinct_scenes(self):
  self.assertEqual(len({hashlib.sha256(render(i).tobytes()).hexdigest() for i in range(8)}),8)
 def test_palette(self):
  self.assertNotEqual(render(0,'ai_work').getpixel((56,175)),render(0,'romance').getpixel((56,175)))
 def test_reject_unknown_genre(self):
  with self.assertRaises(ValueError):validate('other',POLICY)
 def test_reject_approval(self):
  with self.assertRaises(ValueError):validate('ai_work',{**POLICY,'publication_approved':True})
 def test_reject_post(self):
  with self.assertRaises(ValueError):validate('ai_work',{**POLICY,'automatic_posting':True})
 def test_reject_upload(self):
  with self.assertRaises(ValueError):validate('ai_work',{**POLICY,'external_upload':True})
 def test_reject_rights_bypass(self):
  with self.assertRaises(ValueError):validate('ai_work',{**POLICY,'source_rights_reviewed':True})
 def test_reject_policy_missing(self):
  with self.assertRaises(ValueError):validate('ai_work',{})
if __name__=='__main__':unittest.main()
