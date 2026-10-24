"""Cycle823 visual regression/safety tests."""
import importlib.util, pathlib, unittest
from PIL import Image,ImageChops
p=pathlib.Path(__file__).resolve().parent/'cycle823_ci.py'
spec=importlib.util.spec_from_file_location('cycle823',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestUI(unittest.TestCase):
 def test_10_genre_accents(self):
  self.assertEqual(len(m.art.PALETTES),10)
  for c in m.art.PALETTES.values():
   im=Image.new('RGB',(1080,1920),'white')
   m.ui(im,3,c)
   self.assertNotEqual(im.getpixel((160,550)),(255,255,255))
 def test_8_distinct_scenes(self):
  pics=[]
  for i in range(8):
   im=Image.new('RGB',(1080,1920),'white')
   m.ui(im,i,m.art.PALETTES['ai_work'])
   pics.append(im.crop((120,625,945,1080)).resize((100,50)))
  self.assertTrue(all(ImageChops.difference(pics[i],pics[i+1]).getbbox() for i in range(7)))
 def test_script_unchanged(self):
  self.assertEqual(len(m.CAPTIONS),8)
  self.assertEqual(m.CAPTIONS,m.prior.LINES)
 def test_review_only(self):
  import inspect
  s=inspect.getsource(m)
  self.assertIn('架空の画面 / DEMO',s)
  self.assertNotIn('requests.post(',s)
if __name__=='__main__':unittest.main()
