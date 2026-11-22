import unittest
from cycle1635_storyboard import SCENES,DURATION,FPS,SIZE,qa
class TestReviewGate(unittest.TestCase):
 def test_five_scenes(self):
  self.assertEqual(len(SCENES),5)
  self.assertEqual((DURATION,FPS,SIZE),(18,24,(1080,1920)))
 def test_silent_video_rejected(self):
  self.assertFalse(qa({"asset_approved":True,"employee_approved":True})["posting_allowed"])
 def test_missing_human_approval_rejected(self):
  self.assertFalse(qa({"audio_codec":"aac","speech_verified":True,"captions_synced":True,"asset_approved":True})["posting_allowed"])
if __name__=="__main__": unittest.main()
