import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from scene_motion import GENRES,scenes,totals,row_removal_progress,speech_timing,review_gate
class Cycle699Tests(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(set(GENRES)),10)
 def test_totals(self):self.assertEqual(totals(),{"before":9000,"after":6000,"removed":3000,"rows_before":4,"rows_after":3})
 def test_scenes(self):
  s=scenes()
  self.assertEqual(len(s),8);self.assertEqual(s[-1].end,20)
  self.assertTrue(all(a.end==b.start for a,b in zip(s,s[1:])))
 def test_animation(self):
  self.assertEqual(row_removal_progress(10.4),0)
  self.assertTrue(0<row_removal_progress(11.1)<1)
  self.assertEqual(row_removal_progress(12.1),1)
 def test_voice_sync(self):
  x=speech_timing([1.5]*8)
  self.assertEqual(x[0]["end"],1.5);self.assertEqual(x[-1]["end"],19.0)
  with self.assertRaises(ValueError):speech_timing([2.5]*8)
 def test_publication_gate(self):
  self.assertEqual(review_gate(True,False,False,False,False),"PUBLICATION_NOT_APPROVED")
  self.assertEqual(review_gate(True,True,True,True,True),"PUBLICATION_NOT_APPROVED")
if __name__=="__main__":unittest.main()
