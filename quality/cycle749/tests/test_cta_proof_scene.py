"""Cycle749 QA: 10-genre proof CTA, fail-closed synthetic input."""
import sys
from pathlib import Path
import unittest
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cta_proof_scene import ACCENTS, START, END, smooth, verify_contract, draw_frame, capture_crop

class CTAProofTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(ACCENTS),10)
 def test_contract(self):self.assertEqual(verify_contract(),650000)
 def test_reject_mismatched_formula(self):
  with self.assertRaises(ValueError):verify_contract(formula='=SUM(B2:B4)')
 def test_reject_invalid_amount(self):
  with self.assertRaises(ValueError):verify_contract((1,-1,3,4))
 def test_reject_floats(self):
  with self.assertRaises(ValueError):verify_contract((1.,2,3,4))
 def test_time_bounds(self):self.assertEqual((END-START)/30,3.0)
 def test_smooth(self):
  self.assertEqual(smooth(0),0)
  self.assertEqual(smooth(1),1)
 def test_frames_every_genre(self):
  shot=Image.new('RGB',(468,184),'white')
  for g in ACCENTS:
   for i in (0,45,89):self.assertEqual(draw_frame(i,shot,g).size,(540,960))
 def test_bad_frame(self):
  with self.assertRaises(ValueError):draw_frame(90,Image.new('RGB',(468,184)))
 def test_bad_genre(self):
  with self.assertRaises(ValueError):draw_frame(0,Image.new('RGB',(468,184)),'unknown')
 def test_reject_wrong_screenshot(self):
  with self.assertRaises(ValueError):capture_crop(Path('/tmp/private_photo.png'))
if __name__=='__main__':unittest.main()
