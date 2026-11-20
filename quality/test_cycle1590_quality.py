import unittest
from cycle1590_quality import assess,SCENES
class TestQuality(unittest.TestCase):
 def test_silent_rejected(self): self.assertFalse(assess({"video_decoded":True})["publication_approved"])
 def test_all_verified(self): self.assertTrue(assess(dict.fromkeys(("video_decoded","japanese_speech_verified","captions_speech_aligned","asset_rights_approved","employee_approved"),True))["publication_approved"])
 def test_three_scenes(self): self.assertEqual(len(SCENES),3)
if __name__=="__main__": unittest.main()
