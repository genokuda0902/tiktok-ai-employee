import unittest
from render import segments,manifest
class TestReview(unittest.TestCase):
 def test_contiguous(self):
  s=segments();self.assertEqual(s[0][0],0);self.assertEqual(s[-1][1],6);self.assertTrue(all(a[1]==b[0] for a,b in zip(s,s[1:])))
 def test_no_fake_approval(self):
  m=manifest();self.assertFalse(m["posting_allowed"]);self.assertFalse(m["narration_verified"]);self.assertFalse(m["caption_speech_sync_verified"])
 def test_no_private_asset(self):
  self.assertEqual(manifest()["source"],"original synthetic graphics")
if __name__=="__main__":unittest.main()
