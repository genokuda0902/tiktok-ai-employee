import unittest
from quality.cycle616.hook_contract import HookSpec, GENRES, phase, check_caption_box
class TestHook(unittest.TestCase):
 def test_genres(self):
  self.assertEqual(len(GENRES),10)
  for genre in GENRES: HookSpec(genre=genre).validate()
 def test_phases(self):
  self.assertEqual([phase(x) for x in (0,30,60)],["question","benefit","bridge"])
 def test_safe(self):
  self.assertTrue(check_caption_box(150,230))
  self.assertFalse(check_caption_box(0,100))
