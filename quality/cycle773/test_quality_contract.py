import unittest
from quality.cycle773.quality_contract import GENRES,MONTHS,validate
class TestCycle773Contract(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(GENRES),10)
 def test_arithmetic(self):
  self.assertEqual(sum(MONTHS.values()),650000)
  self.assertEqual(MONTHS['4月']-MONTHS['3月'],-20000)
 def test_review_only(self):
  m={'supported_genres':list(GENRES),'review_status':'HUMAN_REVIEW','quality_approved':False,'post_policy':'employee_manual_after_approval','media_rights':'unverified_review_only','data':MONTHS}
  self.assertTrue(validate(m))
  for key,value in [('quality_approved',True),('post_policy','auto'),('media_rights','unknown'),('data',{'1月':100})]:
   bad=dict(m);bad[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):validate(bad)
if __name__=='__main__':unittest.main()
