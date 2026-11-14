import unittest
from pathlib import Path
from render import CAPTIONS
class ReviewTests(unittest.TestCase):
 def test_three_japanese_captions(self):
  self.assertEqual(len(CAPTIONS),3)
  self.assertTrue(all(any(ord(c)>127 for c in line) for line in CAPTIONS))
 def test_no_publication_claim(self):
  self.assertFalse(Path(__file__).with_name("PUBLICATION_APPROVED").exists())
if __name__=="__main__":unittest.main()
