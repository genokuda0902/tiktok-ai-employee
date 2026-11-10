import unittest
from tools.cycle1360_review_gate import publication_allowed
class GateTest(unittest.TestCase):
 def test_fail_closed(self):
  self.assertFalse(publication_allowed({}))
  self.assertFalse(publication_allowed({'narration_verified':True}))
 def test_all_explicit(self):
  self.assertTrue(publication_allowed(dict.fromkeys(('narration_verified','spoken_caption_sync_verified','asset_rights_verified','human_approved'),True)))
if __name__=='__main__': unittest.main()
