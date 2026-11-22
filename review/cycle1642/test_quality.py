import unittest
from verify import quality
class TestGate(unittest.TestCase):
 def test_audio_not_equal_speech(self):
  d={"streams":[{"codec_type":"video","width":1080,"height":1920,"codec_name":"h264"},{"codec_type":"audio","codec_name":"aac"}]}
  q=quality(d)
  self.assertTrue(q["audio_stream_present"])
  self.assertFalse(q["japanese_narration_verified"])
  self.assertFalse(q["publication_approved"])
 def test_silent_fails_audio(self):
  d={"streams":[{"codec_type":"video","width":1080,"height":1920,"codec_name":"h264"}]}
  self.assertFalse(quality(d)["audio_stream_present"])
if __name__=="__main__":unittest.main()
