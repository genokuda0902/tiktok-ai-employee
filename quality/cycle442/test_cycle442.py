"""No-media unit checks; video integration checks require the source MP4."""
import unittest
from pathlib import Path
import render
class TestCycle442(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(set(render.GENRES)),10)
 def test_three_chips(self):self.assertEqual(len(render.CHIPS),3)
 def test_timing(self):self.assertTrue(all(0<=s<e<=20 for s,e,_ in render.CHIPS))
 def test_japanese_text(self):self.assertTrue(all(len(text)>3 for _,_,text in render.CHIPS))
 def test_explicit_voice_gate(self):
  code=Path(render.__file__).read_text()
  self.assertIn("'japanese_voice':'MISSING'",code)
  self.assertIn("PUBLICATION_NOT_APPROVED",code)
 def test_no_posting(self):self.assertNotIn("tiktok.upload",Path(render.__file__).read_text())
if __name__=='__main__':unittest.main()
