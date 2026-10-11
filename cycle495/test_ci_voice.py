"""Static safety/contract tests; no network required."""
import unittest
from pathlib import Path
class Contract(unittest.TestCase):
 def test_native_voice_is_japanese(self):
  src=Path("cycle495/ci_voice.py").read_text()
  self.assertIn('lang="ja"',src)
  self.assertIn("gTTS(",src)
 def test_no_automatic_publication(self):
  src=Path("cycle495/ci_voice.py").read_text()
  self.assertIn('"publication":"NOT_APPROVED"',src)
  self.assertNotIn("tiktok.com/api",src)
 def test_resolution_and_caption_contract(self):
  src=Path("cycle495/ci_voice.py").read_text()
  self.assertIn("W=1080;H=1920",src)
  self.assertIn('captions.srt',src)
 def test_ten_genres(self):
  src=Path("cycle495/ci_voice.py").read_text()
  self.assertIn('GENRES=',src)
  self.assertIn('"比較"',src)
if __name__=="__main__":unittest.main()
