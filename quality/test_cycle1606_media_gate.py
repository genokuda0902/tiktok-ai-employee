import unittest
from quality.cycle1606_media_gate import publication_gate
class MediaGateTest(unittest.TestCase):
 def test_silent_video_rejected(self):
  self.assertFalse(publication_gate({"audio_track":False}))
 def test_audio_alone_not_enough(self):
  self.assertFalse(publication_gate({"audio_track":True,"width":720,"height":1280}))
 def test_fully_approved_metadata(self):
  m=dict.fromkeys(("rights_approved","privacy_approved","japanese_narration_verified","captions_synced_verified","human_approved"),True)
  m.update(audio_track=True,width=720,height=1280)
  self.assertTrue(publication_gate(m))
if __name__=="__main__":unittest.main()
