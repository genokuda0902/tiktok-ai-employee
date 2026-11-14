from pathlib import Path
import unittest
class Captions(unittest.TestCase):
 def test_four_blocks(self):
  t=(Path(__file__).parent/'captions.srt').read_text();self.assertEqual(t.count('-->'),4)
 def test_ends_at_fourteen(self):
  t=(Path(__file__).parent/'captions.srt').read_text();self.assertIn('00:00:14,000',t)
 def test_has_japanese(self):
  t=(Path(__file__).parent/'captions.srt').read_text();self.assertIn('検算',t)
if __name__=='__main__': unittest.main()
