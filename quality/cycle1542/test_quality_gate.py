import unittest
from quality_gate import assess
P={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"12.1"}}
class GateTest(unittest.TestCase):
 def test_effect_audio_is_not_narration(self):
  result=assess(P)
  self.assertTrue(result["checks"]["audio_present"])
  self.assertFalse(result["checks"]["japanese_narration_verified"])
  self.assertFalse(result["publication_approved"])
 def test_approval_required(self):
  self.assertTrue(assess(P,True,True,True,True)["publication_approved"])
 def test_landscape_fails(self):
  p={"streams":[{"codec_type":"video","width":1920,"height":1080}],"format":{"duration":"12"}}
  self.assertFalse(assess(p)["checks"]["vertical"])
if __name__=="__main__":unittest.main()
