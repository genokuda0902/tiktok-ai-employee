import unittest
from quality.cycle1588_gate import check_video
class TestGate(unittest.TestCase):
 def test_silent_video_rejected(self):
  result=check_video({"streams":[{"codec_type":"video","width":720,"height":1280}]})
  self.assertFalse(result["approved"])
  self.assertIn("missing_audio",result["issues"])
 def test_audio_alone_not_enough(self):
  result=check_video({"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]})
  self.assertIn("japanese_voice_unverified",result["issues"])
if __name__=="__main__": unittest.main()
