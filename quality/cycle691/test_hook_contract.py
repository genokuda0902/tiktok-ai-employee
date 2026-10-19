import unittest
from dataclasses import replace
from hook_contract import GENRES,FRAMES,Hook,state,validate,publication_gate,SAFE_TOP,SAFE_BOTTOM
class TestHook(unittest.TestCase):
 def sample(self,g='ai_productivity'):return Hook(g,'その集計、まだ手作業？','手入力','表に整理','架空データ')
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for g in GENRES:self.assertTrue(validate(self.sample(g)))
 def test_frame_boundaries(self):
  self.assertEqual(state(0)['progress'],0)
  self.assertEqual(state(FRAMES-1)['progress'],1)
  for i in (-1,FRAMES,0.5):
   with self.assertRaises(ValueError):state(i)
 def test_motion_monotonic(self):
  x=[state(i)['progress'] for i in range(FRAMES)]
  self.assertTrue(all(a<=b for a,b in zip(x,x[1:])))
 def test_reject_unverified_claim(self):
  with self.assertRaises(ValueError):validate(replace(self.sample(),after='10分→1分'))
 def test_reject_missing_evidence(self):
  with self.assertRaises(ValueError):validate(replace(self.sample(),evidence=''))
 def test_reject_unapproved_assets(self):
  with self.assertRaises(ValueError):validate(replace(self.sample(),rights='UNKNOWN'))
  with self.assertRaises(ValueError):validate(replace(self.sample(),synthetic=False))
 def test_safe_zone(self):
  self.assertGreaterEqual(SAFE_TOP,192);self.assertLessEqual(SAFE_BOTTOM,1536)
 def test_release_gate(self):
  self.assertFalse(publication_gate(native_ja=True))
  self.assertTrue(publication_gate(rights_approved=True,native_ja=True,subtitles_synced=True,staff_approved=True,phone_playback_verified=True))
if __name__=='__main__':unittest.main()
