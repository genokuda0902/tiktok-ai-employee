import unittest
from unittest.mock import patch
from quality.cycle1543.narration_gate import evaluate
class GateTest(unittest.TestCase):
 @patch("quality.cycle1543.narration_gate.subprocess.run")
 def test_audio_cues_not_narration(self, run):
  run.return_value.stdout='{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}'
  self.assertFalse(evaluate("demo.mp4","日本語",False)["publication_approved"])
 @patch("quality.cycle1543.narration_gate.subprocess.run")
 def test_explicit_approval(self, run):
  run.return_value.stdout='{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}'
  self.assertTrue(evaluate("demo.mp4","日本語",True,True,True)["publication_approved"])
if __name__=="__main__": unittest.main()
