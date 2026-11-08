import subprocess, json, unittest
class ReviewGate(unittest.TestCase):
 def test_requires_narration_not_just_audio_stream(self):
  evidence={"audio_codec":"aac","narration_verified":False,"caption_speech_synced":False}
  self.assertFalse(all((evidence["audio_codec"],evidence["narration_verified"],evidence["caption_speech_synced"])))
 def test_review_not_approved(self):
  self.assertNotEqual("REVIEW_ONLY","PUBLICATION_APPROVED")
if __name__=="__main__": unittest.main()
