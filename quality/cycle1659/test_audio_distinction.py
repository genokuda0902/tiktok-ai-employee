import unittest
from audio_distinction import assess
class Tests(unittest.TestCase):
 def test_sound_effect_does_not_count_as_speech(self):
  result=assess([{"codec_type":"video"},{"codec_type":"audio"}])
  self.assertFalse(result["publication_approved"])
  self.assertIn("japanese_narration_unverified",result["reasons"])
 def test_approved_requires_all_evidence(self):
  self.assertTrue(assess([{"codec_type":"video"},{"codec_type":"audio"}],True,True,True,True)["publication_approved"])
if __name__=="__main__": unittest.main()
