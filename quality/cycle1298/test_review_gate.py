import unittest
from quality.cycle1298.review_gate import evaluate
class ReviewGateTests(unittest.TestCase):
 def test_silent_clip_rejected(self):
  result=evaluate([{"codec_type":"video","width":1080,"height":1920}])
  self.assertFalse(result["publication_approved"])
  self.assertIn("audio_missing",result["issues"])
 def test_all_requirements_needed(self):
  streams=[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]
  self.assertTrue(evaluate(streams,captions_synced=True,assets_approved=True,employee_approved=True)["publication_approved"])
if __name__=="__main__":unittest.main()
