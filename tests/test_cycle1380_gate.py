import unittest
from quality.cycle1380_gate import assess
class GateTests(unittest.TestCase):
 def test_silent_rejected(self):
  x=assess({"streams":[{"codec_type":"video","width":1080,"height":1920}]},True,True,True)
  self.assertFalse(x["publication_approved"])
 def test_audio_not_narration(self):
  x=assess({"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]},False,True,True)
  self.assertFalse(x["publication_approved"])
 def test_approved(self):
  x=assess({"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]},True,True,True)
  self.assertTrue(x["publication_approved"])
if __name__=="__main__":unittest.main()
