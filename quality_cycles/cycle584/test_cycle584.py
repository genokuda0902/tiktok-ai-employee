import unittest
from dataclasses import replace
from arith_hook import DEFAULT, GENRES, Proof, state, frame
from build import CAPTIONS, BASE_SHA

class HookTests(unittest.TestCase):
 def test_true_totals(self):self.assertEqual(DEFAULT.running_totals(),(120,270,470,720))
 def test_no_fake_intermediate_values(self):
  allowed={120,270,470,720}
  for i in range(60):
   s=state(DEFAULT,i)
   self.assertTrue(s['running_total'] is None or s['running_total'] in allowed)
 def test_final_value(self):self.assertEqual(state(DEFAULT,59)['running_total'],720)
 def test_progress_monotonic(self):
  a=[state(DEFAULT,i)['completed'] for i in range(60)]
  self.assertEqual(a,sorted(a))
 def test_reject_mismatch(self):
  with self.assertRaises(ValueError):replace(DEFAULT,expected=721).validate()
 def test_reject_unverified(self):
  with self.assertRaises(ValueError):replace(DEFAULT,verified=False).validate()
 def test_genre_profiles(self):
  for g in GENRES:self.assertTrue(replace(DEFAULT,genre=g).validate())
 def test_bad_genre(self):
  with self.assertRaises(ValueError):replace(DEFAULT,genre='invalid').validate()
 def test_no_negative(self):
  with self.assertRaises(ValueError):replace(DEFAULT,items=(-1,151,200,250)).validate()
 def test_safe_canvas(self):self.assertEqual(frame(DEFAULT,59).size,(540,960))
 def test_caption_intervals(self):
  self.assertEqual(CAPTIONS[0][:2],(0,2));self.assertEqual(CAPTIONS[-1][:2],(19,20))
  self.assertTrue(all(a<b for a,b,_ in CAPTIONS))
 def test_sha_guard(self):self.assertEqual(len(BASE_SHA),64)

if __name__=='__main__':unittest.main()
