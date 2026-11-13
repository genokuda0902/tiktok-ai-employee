import unittest
from quality_gate import review_status
class TestGate(unittest.TestCase):
 def test_cue_is_not_narration(self):
  r=review_status({'codec_name':'h264','width':1080,'height':1920},{'codec_name':'aac'})
  self.assertFalse(r['publication_approved'])
  self.assertIn('japanese_narration_unverified',r['issues'])
 def test_approved(self):
  r=review_status({'codec_name':'h264','width':1080,'height':1920},{'codec_name':'aac'},True,True,True,True)
  self.assertTrue(r['publication_approved'])
if __name__=='__main__':unittest.main()
