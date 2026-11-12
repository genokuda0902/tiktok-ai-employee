import unittest
from quality.cycle1405_gate import assess
class GateTests(unittest.TestCase):
 def test_silent_mp4_is_not_approved(self):
  m={"streams":[{"codec_type":"video","width":1080,"height":1920}],"full_decode":True}
  self.assertFalse(assess(m)["posting_allowed"])
  self.assertIn("narration",assess(m)["issues"])
 def test_complete_evidence(self):
  m={"streams":[{"codec_type":"video","width":1080,"height":1920}],"full_decode":True,"japanese_narration_verified":True,"speech_synced_captions_verified":True,"asset_rights_approved":True,"employee_approved":True}
  self.assertTrue(assess(m)["posting_allowed"])
if __name__=="__main__":unittest.main()
