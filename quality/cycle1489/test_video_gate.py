import unittest
from video_gate import publication_gate
class GateTests(unittest.TestCase):
 def test_silent_video_rejected(self):
  self.assertFalse(publication_gate({"width":1080,"height":1920,"audio_track":False},True,True,True,True))
 def test_unverified_japanese_speech_rejected(self):
  self.assertFalse(publication_gate({"width":1080,"height":1920,"audio_track":True},False,True,True,True))
 def test_approval_required(self):
  self.assertFalse(publication_gate({"width":1080,"height":1920,"audio_track":True},True,True,True,False))
if __name__=="__main__":unittest.main()
