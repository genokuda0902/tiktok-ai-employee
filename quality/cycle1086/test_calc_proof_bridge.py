import unittest
from PIL import Image
from quality.cycle1086.calc_proof_bridge import PALETTES, overlay, validate, check_hash, START, END, SAFE_Y
DATA={'categories':['4月','5月','6月'],'series':[{'name':'営業A','values':[12,16,18]},{'name':'営業B','values':[8,9,12]}],'note':'架空データ'}
class ProofTest(unittest.TestCase):
 def test_data(self):self.assertEqual(validate(DATA),[46,29])
 def test_fail_closed_missing_sha(self):
  with self.assertRaises(ValueError):check_hash(__file__,'0'*64)
 def test_negative_rejected(self):
  bad={'categories':['4月'],'series':[{'name':'A','values':[-1]},{'name':'B','values':[2]}],'note':'x'}
  with self.assertRaises(ValueError):validate(bad)
 def test_non_integer_rejected(self):
  bad={'categories':['4月'],'series':[{'name':'A','values':[1.2]},{'name':'B','values':[2]}],'note':'x'}
  with self.assertRaises(ValueError):validate(bad)
 def test_genres_and_frame_bounds(self):
  ui=Image.new('RGB',(908,484),'white')
  self.assertEqual(len(PALETTES),10)
  for g in PALETTES:
   im=overlay(END-START-1,ui,DATA,g)
   self.assertEqual(im.size,(1080,SAFE_Y))
  with self.assertRaises(ValueError):overlay(-1,ui,DATA,'ai_work')
  with self.assertRaises(ValueError):overlay(0,ui,DATA,'unknown')
 def test_fictional_sum_not_correction(self):
  d={**DATA,'series':[{'name':'営業A','values':[2,3,4]},{'name':'営業B','values':[5,6,7]}]}
  self.assertEqual(validate(d),[9,18])
if __name__=='__main__':unittest.main()
