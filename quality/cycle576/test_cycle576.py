import unittest
from render_kinetic import GENRES, validate_chapters
class Tests(unittest.TestCase):
 def test_genres(self): self.assertEqual(len(GENRES), 10)
 def test_chapters(self): self.assertTrue(validate_chapters())
