"""Cycle728 contract and image rendering tests; no publishing."""
import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'video_engine'/'quality'))
import cycle728_hero_cleanroom as m
class HeroTests(unittest.TestCase):
 def test_genres(self):
  self.assertEqual(len(m.GENRE_ACCENTS),10)
  for genre in m.GENRE_ACCENTS:self.assertTrue(m.validate(genre))
 def test_unknown_genre_fails(self):
  with self.assertRaises(ValueError):m.validate('unknown')
 def test_evidence(self):self.assertEqual(sum(m.SALES),65)
 def test_safe_area(self):self.assertLessEqual(m.SAFE[3],1536)
 def test_robot_is_original_rgba(self):self.assertEqual(m.make_robot(m.GENRE_ACCENTS['ai_work']).mode,'RGBA')
 def test_first_frame_native(self):
  a=m.GENRE_ACCENTS['ai_work'];im=m.draw_frame(m.background(a),m.make_robot(a),a,0)
  self.assertEqual(im.size,(1080,1920))
 def test_animation_changes_frames(self):
  a=m.GENRE_ACCENTS['ai_work'];bg=m.background(a);r=m.make_robot(a)
  self.assertNotEqual(m.draw_frame(bg,r,a,0).tobytes(),m.draw_frame(bg,r,a,65).tobytes())
if __name__=='__main__':unittest.main(verbosity=2)
