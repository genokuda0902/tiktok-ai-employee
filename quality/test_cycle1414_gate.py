import unittest
from quality.cycle1414_gate import evaluate
class GateTest(unittest.TestCase):
 def test_silent_review_is_blocked(self):
  q={"audio_streams":0,"japanese_narration":"ABSENT","speech_synced_captions":"ABSENT","decode":"PASS","resolution":[1080,1920]}
  self.assertFalse(evaluate(q)["publication_approved"])
 def test_approval_required(self):
  q={"audio_streams":1,"japanese_narration":"VERIFIED","speech_synced_captions":"VERIFIED","decode":"PASS","resolution":[1080,1920]}
  self.assertFalse(evaluate(q)["publication_approved"])
  self.assertTrue(evaluate(q,approved=True)["publication_approved"])
if __name__=="__main__":unittest.main()
