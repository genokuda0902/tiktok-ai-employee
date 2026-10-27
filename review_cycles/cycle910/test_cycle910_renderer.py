"""Local visual tests (requires Pillow + Noto CJK fonts). CI only runs dependency-free policy tests."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from hook_comparison import *
class TestHook(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(PALETTES),10)
 def test_layout(self):self.assertTrue(validate_layout())
 def test_first_frame(self):self.assertEqual(draw_overlay(0).size,(952,1015))
 def test_last_frame(self):self.assertEqual(draw_overlay(86).size,(952,1015))
 def test_frames_differ(self):self.assertNotEqual(draw_overlay(0).tobytes(),draw_overlay(70).tobytes())
 def test_genre_differs(self):self.assertNotEqual(draw_overlay(50,'health').tobytes(),draw_overlay(50,'ai_work').tobytes())
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):draw_overlay(0,'bad')
 def test_invalid_frame(self):
  with self.assertRaises(ValueError):draw_overlay(87)
 def test_disclaimer(self):self.assertIn('実績ではなく説明用イメージ',Path(__file__).with_name('hook_comparison.py').read_text())
 def test_no_upload(self):self.assertNotIn('requests.',Path(__file__).with_name('hook_comparison.py').read_text())
if __name__=='__main__':unittest.main()
