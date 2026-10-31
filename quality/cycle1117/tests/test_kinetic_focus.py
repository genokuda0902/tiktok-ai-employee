import sys, unittest
from pathlib import Path
from PIL import Image, ImageChops
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kinetic_focus import FOCUS_BOXES,GENRES,focus_index,draw_focus

class TestKineticFocus(unittest.TestCase):
 def test_eight_scenes(self):self.assertEqual(len(FOCUS_BOXES),8)
 def test_safe_illustration_bounds(self):
  for boxes in FOCUS_BOXES:
   for x1,y1,x2,y2 in boxes:
    self.assertTrue(75<=x1<x2<=1000 and 600<=y1<y2<=1270)
 def test_advances_all_scenes(self):
  for scene,boxes in enumerate(FOCUS_BOXES):
   self.assertEqual(focus_index(scene,0,3),0)
   self.assertEqual(focus_index(scene,2.999,3),len(boxes)-1)
 def test_10_genres(self):
  for genre in GENRES:
   im=Image.new("RGB",(1080,1920),(10,30,48))
   self.assertEqual(draw_focus(im,0,.5,3,genre).size,(1080,1920))
 def test_caption_area_unchanged(self):
  im=Image.new("RGB",(1080,1920),(10,30,48))
  original=im.crop((68,1365,872,1648)).tobytes()
  draw_focus(im,0,.5,3)
  self.assertEqual(original,im.crop((68,1365,872,1648)).tobytes())
 def test_visible_change(self):
  im=Image.new("RGB",(1080,1920),(10,30,48))
  self.assertIsNotNone(ImageChops.difference(im,draw_focus(im.copy(),0,.5,3)).getbbox())
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):
   draw_focus(Image.new("RGB",(1080,1920)),0,.5,3,"invalid")

if __name__=="__main__":unittest.main()
