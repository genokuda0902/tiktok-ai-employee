"""Offline tests for source-safe 10-genre animated attention overlay."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('evidence_pointer',Path(__file__).with_name('evidence_pointer.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TestReviewOverlay(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(m.ACCENTS),10)
 def test_review_policy(self):self.assertIn('PUBLICATION_NOT_APPROVED',m.POLICY)
 def test_stage_boundaries(self):
  self.assertEqual([m.stage(i) for i in (0,28,29,57,58,86)],[0,0,1,1,2,2])
 def test_out_of_range(self):
  for i in (-1,87):
   with self.assertRaises(ValueError):m.stage(i)
 def test_pointer_bounds(self):
  for i in range(87):
   x,y=m.pointer_xy(i)
   self.assertTrue(0<=x<m.W and 0<=y<m.SAFE_Y)
 def test_smooth(self):
  self.assertEqual(m.smooth(-1),0)
  self.assertEqual(m.smooth(2),1)
 def test_safezone(self):self.assertLess(m.SAFE_Y,m.H)
 def test_genre_reject(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'source.mp4';p.write_bytes(b'synthetic')
   with self.assertRaisesRegex(ValueError,'genre'):
    m.validate(p,Path(tmp)/'out_REVIEW_ONLY.mp4',m.sha256(p),'unsafe')
 def test_sha_reject(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'source.mp4';p.write_bytes(b'synthetic')
   with self.assertRaisesRegex(ValueError,'SHA'):
    m.validate(p,Path(tmp)/'out_REVIEW_ONLY.mp4','wrong','ai_work')
 def test_policy_reject(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'source.mp4';p.write_bytes(b'synthetic')
   with self.assertRaisesRegex(ValueError,'policy'):
    m.validate(p,Path(tmp)/'out_REVIEW_ONLY.mp4',m.sha256(p),'ai_work',policy='APPROVED')
 def test_output_reject(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'source.mp4';p.write_bytes(b'synthetic')
   with self.assertRaisesRegex(ValueError,'review-only'):
    m.validate(p,Path(tmp)/'out.mp4',m.sha256(p),'ai_work')
 def test_no_source_overwrite(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'source_REVIEW_ONLY.mp4';p.write_bytes(b'synthetic')
   with self.assertRaisesRegex(ValueError,'overwrite'):
    m.validate(p,p,m.sha256(p),'ai_work')

if __name__=='__main__':unittest.main()
