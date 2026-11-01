import unittest
from quality.cycle1084.proof_reconcile import ACCENTS,SAMPLE,SAFE_Y,W,H,START,END,frame,validate

class ReconciliationTests(unittest.TestCase):
 def test_arithmetic(self):
  self.assertEqual(validate(SAMPLE),[46,29]);self.assertEqual(sum(validate(SAMPLE)),75)
 def test_ten_genres_caption_safe(self):
  for g in ACCENTS:
   with self.subTest(genre=g):
    im=frame(END-START-1,SAMPLE,g)
    self.assertEqual(im.size,(W,H))
    self.assertIsNone(im.crop((0,SAFE_Y,W,H)).getbbox())
 def test_different_totals_not_hardcoded(self):
  import copy
  d=copy.deepcopy(SAMPLE);d['series'][0]['values']=[1,2,3]
  self.assertEqual(validate(d),[6,29]);self.assertIsNotNone(frame(END-START-1,d).getbbox())
 def test_reject_unvalidated_values(self):
  import copy
  d=copy.deepcopy(SAMPLE);d['series'][0]['values'][0]=-1
  with self.assertRaises(ValueError):frame(0,d)
 def test_reject_unknown_genre(self):
  with self.assertRaises(ValueError):frame(0,SAMPLE,'unknown')
 def test_reject_frame_outside_scene(self):
  with self.assertRaises(ValueError):frame(END-START)
 def test_frame_progress(self):
  self.assertNotEqual(frame(0).tobytes(),frame(END-START-1).tobytes())

if __name__=='__main__':unittest.main()
