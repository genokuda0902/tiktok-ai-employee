"""Cycle592 additional cross-genre frame regression (review only)."""
import unittest
from cycle592_clean_proof import Scene, GENRE_COLORS, draw_frame, W, H

class TenGenreRenderTests(unittest.TestCase):
 def test_each_genre_final_frame(self):
  self.assertEqual(len(GENRE_COLORS),10)
  for genre in GENRE_COLORS:
   with self.subTest(genre=genre):
    frame=draw_frame(59,Scene(genre=genre))
    self.assertEqual(frame.size,(W,H))

if __name__=="__main__":unittest.main()
