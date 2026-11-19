import unittest
from quality.cycle1571_gate import validate
class TestGate(unittest.TestCase):
 def test_silent_video_not_approved(self):
  p={"streams":[{"width":540,"height":960}],"format":{"duration":"12"}}
  self.assertFalse(validate(p)["publication_approved"])
 def test_missing_metadata_fails_closed(self):
  self.assertFalse(validate({})["publication_approved"])
 def test_approved_evidence(self):
  p={"streams":[{"width":1080,"height":1920}],"format":{"duration":"20"}}
  self.assertTrue(validate(p,japanese_voice_verified=True,captions_verified=True,rights_approved=True,employee_approved=True)["publication_approved"])
if __name__=="__main__":unittest.main()
