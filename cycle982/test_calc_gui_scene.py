import unittest
from PIL import Image
from calc_gui_scene import START,END,SAFE_Y,GENRES,artwork,validate
class SceneTests(unittest.TestCase):
 def setUp(self):self.gui=Image.new('RGB',(1280,800),'white')
 def test_frame_bounds(self):
  for i in [0,END-START-1]:self.assertEqual(artwork(self.gui,i).size,(1080,SAFE_Y))
  for i in [-1,END-START]:
   with self.assertRaises(ValueError):artwork(self.gui,i)
 def test_fail_closed(self):
  for genre in GENRES[1:]:
   with self.assertRaises(ValueError):validate(genre)
 def test_unknown(self):
  with self.assertRaises(ValueError):validate('unknown')
 def test_synthetic_other_genre(self):validate('finance',synthetic=True)
 def test_small_screen(self):
  with self.assertRaises(ValueError):artwork(Image.new('RGB',(300,200)),0)
 def test_caption_region_never_drawn(self):
  self.assertEqual(artwork(self.gui,40).height,SAFE_Y)
 def test_frame_variation(self):
  self.assertNotEqual(artwork(self.gui,0).tobytes(),artwork(self.gui,86).tobytes())
if __name__=='__main__':unittest.main()
