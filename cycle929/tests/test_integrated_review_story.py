import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('story',Path(__file__).resolve().parents[1]/'src'/'integrated_review_story.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ReviewTests(unittest.TestCase):
 def test_policy(self):self.assertTrue(m.validate());self.assertIn('PUBLICATION_NOT_APPROVED',m.POLICY)
 def test_frame_count(self):self.assertEqual(m.FRAMES,691)
 def test_safe_caption(self):self.assertEqual(m.CAPTION_SAFE_Y,1460)
 def test_ten_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_stage5(self):self.assertEqual([m.beat(x,5) for x in [348,378,408,434]],[0,1,2,2])
 def test_stage8(self):self.assertEqual([m.beat(x,8) for x in [609,637,665,690]],[0,1,2,2])
 def test_bounds(self):
  with self.assertRaises(ValueError):m.beat(347,5)
  with self.assertRaises(ValueError):m.beat(691,8)
 def test_all_genres_render(self):
  for genre in m.GENRES:
   with self.subTest(genre=genre):
    im=m.render(380,5,genre)
    self.assertEqual(im.size,(1080,1460))
 def test_outro_render(self):self.assertEqual(m.render(640,8).size,(1080,1460))
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):m.render(400,5,'not-a-genre')
 def test_scene_difference(self):
  a=m.render(348,5).tobytes();b=m.render(420,5).tobytes();self.assertNotEqual(a,b)
 def test_review_outro_different(self):self.assertNotEqual(m.render(609,8).tobytes(),m.render(690,8).tobytes())
if __name__=='__main__':unittest.main()
