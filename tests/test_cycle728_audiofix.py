"""Cycle728 corrected renderer tests. No network or posting."""
import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'video_engine'/'quality'))
import cycle728_hero_cleanroom_audiofix as m
class CleanroomTests(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(m.GENRE_ACCENTS),10)
  for g in m.GENRE_ACCENTS:self.assertTrue(m.validate(g))
 def test_unknown_genre_rejected(self):
  with self.assertRaises(ValueError):m.validate('unlisted')
 def test_65man_synthetic_proof(self):self.assertEqual(sum(m.SALES),65)
 def test_caption_safe(self):self.assertLessEqual(m.SAFE[3],1536)
 def test_original_robot_rgba(self):self.assertEqual(m.make_robot(m.GENRE_ACCENTS['ai_work']).mode,'RGBA')
 def test_native_frame(self):
  a=m.GENRE_ACCENTS['ai_work'];self.assertEqual(m.draw_frame(m.background(a),m.make_robot(a),a,0).size,(1080,1920))
 def test_animation_changes_frame(self):
  a=m.GENRE_ACCENTS['ai_work'];bg=m.background(a);r=m.make_robot(a)
  self.assertNotEqual(m.draw_frame(bg,r,a,0).tobytes(),m.draw_frame(bg,r,a,65).tobytes())
if __name__=='__main__':unittest.main(verbosity=2)
