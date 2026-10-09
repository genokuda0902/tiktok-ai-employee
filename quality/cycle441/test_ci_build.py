"""Cycle441 CI structural tests; fail closed on missing voice or timing."""
import unittest
from pathlib import Path
import ci_build as c
class QualityContract(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(c.GENRES),10)
 def test_scene_count(self): self.assertEqual(len(c.SLOTS),8)
 def test_20s_at_30fps(self): self.assertEqual(sum(round(s*30) for s in c.SLOTS),600)
 def test_voice_script(self): self.assertEqual(len(c.VOICE),8)
 def test_ja_characters(self): self.assertTrue(all(any(ord(ch)>0x3000 for ch in line) for line in c.VOICE[1:]))
 def test_no_posting(self):
  src=Path(c.__file__).read_text()
  self.assertNotIn("upload_to_tiktok",src)
  self.assertNotIn("auto_post",src)
 def test_no_paid_api(self): self.assertNotIn("api_key",Path(c.__file__).read_text())
if __name__=="__main__":unittest.main(verbosity=2)
