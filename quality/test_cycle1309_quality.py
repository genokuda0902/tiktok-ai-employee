import unittest
from cycle1309_quality import public_ready
class QualityTest(unittest.TestCase):
 def test_no_narration_fails(self):
  self.assertFalse(public_ready(dict(video_ok=True,vertical_1080p=True,audio_stream=True,narration_verified=False,caption_sync_verified=True,publish_approved=True)))
 def test_audio_alone_fails(self):
  self.assertFalse(public_ready(dict(video_ok=True,vertical_1080p=True,audio_stream=True)))
 def test_all_verified_pass(self):
  self.assertTrue(public_ready(dict.fromkeys(("video_ok","vertical_1080p","audio_stream","narration_verified","caption_sync_verified","publish_approved"),True)))
if __name__=="__main__":unittest.main()
