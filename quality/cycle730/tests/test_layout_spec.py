import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import layout_spec as s
class TestLayoutSpec(unittest.TestCase):
 def test_contract(self):self.assertTrue(s.validate())
 def test_genres(self):self.assertEqual(len(s.GENRES),10)
 def test_distinct_colors(self):self.assertEqual(len(set(s.GENRES.values())),10)
 def test_portrait(self):self.assertEqual(s.FRAME_SIZE,(1080,1920))
 def test_speech_gate(self):self.assertEqual(s.caption_at(15.0),'')
 def test_cues(self):self.assertEqual(s.caption_at(14.4),'出力。')
 def test_safe_zone(self):self.assertLess(s.CAPTION_BOUNDS[3],s.BOTTOM_SAFE_LIMIT)
 def test_frame_count(self):self.assertEqual(s.FRAME_RANGE[1]-s.FRAME_RANGE[0],69)
if __name__=='__main__':unittest.main()
