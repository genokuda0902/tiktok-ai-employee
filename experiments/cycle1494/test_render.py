import unittest
from pathlib import Path
from render import SCENES
class TestTimeline(unittest.TestCase):
 def test_four_scenes(self): self.assertEqual(len(SCENES),4)
 def test_nonempty_japanese_copy(self): self.assertTrue(all(a and b for a,b in SCENES))
 def test_srt_segments(self):
  text=(Path(__file__).parent/'captions.srt').read_text(encoding='utf-8')
  self.assertEqual(text.count(' --> '),len(SCENES))
 def test_review_not_approved(self):
  source=(Path(__file__).parent/'render.py').read_text(encoding='utf-8')
  self.assertIn('投稿未承認',source)
if __name__=='__main__':unittest.main()
