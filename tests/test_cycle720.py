"""Cycle720 contract tests; no publication permission is granted."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from cycle720_render import GENRES,SALES,SCENES,FPS,validate,stamp
class Cycle720(unittest.TestCase):
 def test_genres(self):
  self.assertEqual(len(GENRES),10)
  self.assertEqual(len(set(GENRES)),10)
 def test_fictional_sales_math(self):
  self.assertEqual(sum(SALES),65)
  self.assertEqual(max(SALES),20)
  self.assertEqual(SALES.index(20),2)
 def test_eight_ja_narrations(self):
  self.assertEqual(len(SCENES),8)
  for heading,spoken,kind in SCENES:
   self.assertTrue(heading and spoken and kind)
   self.assertTrue(any(ord(c)>127 for c in spoken))
 def test_timeline_format(self):
  self.assertEqual(stamp(0),"00:00:00,000")
  self.assertEqual(stamp(3.5),"00:00:03,500")
  self.assertEqual(FPS,30)
 def test_validation(self):
  self.assertTrue(validate())
if __name__=="__main__":unittest.main()
