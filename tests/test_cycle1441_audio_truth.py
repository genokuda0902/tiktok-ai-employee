import unittest
from quality.cycle1441_audio_truth import assess
class TestGate(unittest.TestCase):
 def test_silent_track_fails(self):
  r=assess(1080,1920,True,True,False,False,True,False)
  self.assertFalse(r["posting_allowed"])
  self.assertIn("japanese_narration",r["issues"])
 def test_unapproved_fails(self):
  self.assertFalse(assess(1080,1920,True,True,True,True,False,True)["posting_allowed"])
 def test_complete_passes(self):
  self.assertTrue(assess(1080,1920,True,True,True,True,True,True)["posting_allowed"])
if __name__=="__main__": unittest.main()
