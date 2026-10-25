import tempfile,unittest
from pathlib import Path
import numpy as np
from calc_inset import GENRES,POLICY,make_label,composite,CARD,LABEL,validate,sha256
class TestCalcInset(unittest.TestCase):
 def setUp(self):
  self.base=np.zeros((1920,1080,3),np.uint8);self.base[:]=35
  self.capture=np.zeros((900,1440,3),np.uint8);self.capture[:]=200
 def test_genres(self):self.assertEqual(len(GENRES),10)
 def test_policy_review_only(self):
  self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['automatic_posting']);self.assertFalse(POLICY['external_upload'])
 def test_caption_unchanged(self):
  o=composite(self.base,self.capture,make_label());self.assertTrue(np.array_equal(o[1540:],self.base[1540:]))
 def test_header_unchanged(self):
  o=composite(self.base,self.capture,make_label());self.assertTrue(np.array_equal(o[:400],self.base[:400]))
 def test_untouched_side(self):
  o=composite(self.base,self.capture,make_label());self.assertTrue(np.array_equal(o[1450:1535],self.base[1450:1535]))
 def test_image_area_changed(self):
  o=composite(self.base,self.capture,make_label());self.assertGreater(float(np.mean(o[550:1100,100:900])),float(np.mean(self.base[550:1100,100:900])))
 def test_input_immutable(self):
  x=self.base.copy();composite(self.base,self.capture,make_label());self.assertTrue(np.array_equal(self.base,x))
 def test_invalid_dimensions(self):
  with self.assertRaises(ValueError):composite(np.zeros((100,100,3),np.uint8),self.capture,make_label())
 def test_invalid_crop(self):
  with self.assertRaises(ValueError):composite(self.base,np.zeros((100,100,3),np.uint8),make_label())
 def test_manifest_reject(self):
  with tempfile.TemporaryDirectory() as d:
   a=Path(d)/'a';b=Path(d)/'b';a.write_bytes(b'a');b.write_bytes(b'b')
   with self.assertRaisesRegex(ValueError,'fail-closed'):
    validate(a,b,Path(d)/'out',POLICY,'ai_work',(0,1))
 def test_genre_reject(self):
  with tempfile.TemporaryDirectory() as d:
   a=Path(d)/'a';b=Path(d)/'b';a.write_bytes(b'a');b.write_bytes(b'b')
   with self.assertRaisesRegex(ValueError,'unsupported genre'):
    validate(a,b,Path(d)/'out',{**POLICY,'source_sha256':sha256(a),'capture_sha256':sha256(b)},'unlisted',(0,1))
 def test_window_reject(self):
  with tempfile.TemporaryDirectory() as d:
   a=Path(d)/'a';b=Path(d)/'b';a.write_bytes(b'a');b.write_bytes(b'b')
   with self.assertRaisesRegex(ValueError,'invalid window'):
    validate(a,b,Path(d)/'out',{**POLICY,'source_sha256':sha256(a),'capture_sha256':sha256(b)},'ai_work',(2,1))
 def test_label_is_rendered(self):
  label=make_label();self.assertEqual(label.shape,(90,900,4));self.assertGreater(np.count_nonzero(label[:,:,3]),100)
if __name__=='__main__':unittest.main()
