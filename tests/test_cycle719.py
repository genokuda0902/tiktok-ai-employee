import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from cycle719_slide_schema import PALETTES,ProofScreen,validate,WIDTH,HEIGHT,FPS,SCENE_FRAMES
from cycle719_tts import LINES
class Cycle719Tests(unittest.TestCase):
 def test_portrait(self):self.assertEqual((WIDTH,HEIGHT,FPS),(1080,1920,30))
 def test_ten_genres(self):self.assertEqual(len(PALETTES),10)
 def test_scene(self):self.assertEqual(SCENE_FRAMES,59)
 def test_copy(self):validate("science",ProofScreen())
 def test_bad_genre(self):
  with self.assertRaises(ValueError):validate("bad",ProofScreen())
 def test_narration_segments(self):self.assertEqual(len(LINES),8)
 def test_japanese_content(self):self.assertTrue(all(any(ord(ch)>127 for ch in line) for line in LINES))
if __name__=="__main__":unittest.main()
