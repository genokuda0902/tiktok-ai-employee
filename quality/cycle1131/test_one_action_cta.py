import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from one_action_cta import GENRE_DATA,render_art,state_at
class TestCTA(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(GENRE_DATA),10)
 def test_reveal_sequence(self):self.assertEqual([state_at(t) for t in (0,.4,1.0,1.7)],[0,1,2,3])
 def test_all_genres(self):
  for genre in GENRE_DATA:
   with self.subTest(genre=genre):self.assertEqual(render_art(2.7,genre).size,(951,803))
 def test_animation(self):self.assertNotEqual(render_art(.05).tobytes(),render_art(2.9).tobytes())
 def test_determinism(self):self.assertEqual(render_art(1.9).tobytes(),render_art(1.9).tobytes())
 def test_bad_genre(self):
  with self.assertRaises(ValueError):render_art(0,'unknown')
if __name__=='__main__':unittest.main()
