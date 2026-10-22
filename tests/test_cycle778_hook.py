import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'video_engine'/'quality'))
from cycle778_hook import *
class TestHook(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_numbers(self):self.assertEqual(sum(MONTHS),650000)
 def test_dimensions(self):self.assertEqual(draw_frame(30).size,(1080,1920))
 def test_safety(self):self.assertTrue(safe_box((67,325,643,565)))
 def test_bounds(self):
  with self.assertRaises(ValueError):draw_frame(96)
if __name__=='__main__':unittest.main()
