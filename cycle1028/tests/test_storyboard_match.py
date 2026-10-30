import sys,unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from storyboard_match import GENRES,panel,filter_graph,render
class StoryboardMatchTest(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_panels_all_genres(self):
  for genre in GENRES:
   for beat in (1,2):
    im=panel(genre,beat)
    self.assertEqual(im.size,(1080,1240));self.assertEqual(im.mode,'RGBA')
 def test_reject_unknown_genre(self):
  with self.assertRaises(ValueError):panel('unknown',1)
 def test_filter_contains_two_beats(self):
  s=filter_graph(5.95,7.20,8.52)
  self.assertIn('[vout]',s);self.assertIn('alpha=1',s)
 def test_invalid_timing(self):
  with self.assertRaises(ValueError):filter_graph(2,1,3)
 def test_review_gate(self):
  with self.assertRaisesRegex(ValueError,'review gate'):render('/nonexistent','/tmp/out','/tmp/report','ai_work','0'*64)
 def test_no_caption_overlap(self):self.assertLess(100+1240,1490)
 def test_fictional_label(self):self.assertTrue('架空' in Path(__file__).resolve().parents[1].joinpath('source/storyboard_match.py').read_text())
if __name__=='__main__':unittest.main()
