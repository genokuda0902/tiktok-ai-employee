"""Tests for cycle831 editorial photo/slide renderer. No external API."""
import importlib.util,tempfile,unittest
from pathlib import Path
from PIL import Image
spec=importlib.util.spec_from_file_location('scene831',Path(__file__).with_name('scene831.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestCycle831(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(m.COLORS),10)
  for genre,c in m.COLORS.items():self.assertEqual(len(m.rgb(c)),3,genre)
 def test_exact_frames(self):
  self.assertEqual(len(m.FRAMES),8)
  self.assertEqual(sum(m.FRAMES),775)
 def test_eight_scenes(self):
  self.assertEqual(len(m.HEAD),8)
  self.assertEqual(len(m.ACT),8)
 def test_storyboard_cropping(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'collage.png';Image.new('RGB',(1214,1295),(100,140,170)).save(p)
   for i in range(8):
    crop=m.storyboard_panel(p,i)
    self.assertGreater(crop.width,100)
    self.assertGreater(crop.height,100)
 def test_ten_genre_layouts(self):
  with tempfile.TemporaryDirectory() as tmp:
   art=Image.new('RGB',(300,480),(180,170,160))
   for genre in m.COLORS:
    p=Path(tmp)/f'{genre}.png';m.slide(0,art,p,genre)
    with Image.open(p) as im:self.assertEqual(im.size,(1080,1920))
 def test_unknown_genre_fails_closed(self):
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):m.slide(0,Image.new('RGB',(300,480)),Path(tmp)/'x.png','unknown')
if __name__=='__main__':unittest.main()
