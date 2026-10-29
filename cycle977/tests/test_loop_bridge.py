import importlib.util,tempfile,unittest
from pathlib import Path
from PIL import Image
p=Path(__file__).resolve().parents[1]/'code'/'loop_bridge.py'
spec=importlib.util.spec_from_file_location('loop_bridge',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestBridge(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(m.PALETTES),10)
 def test_unknown_rejected(self):
  with self.assertRaises(ValueError):m.verify_genre('unreviewed')
 def test_other_genre_fail_closed(self):
  with self.assertRaises(ValueError):m.verify_genre('finance')
 def test_other_genre_synthetic_allowed(self):m.verify_genre('finance',True)
 def test_duration(self):self.assertEqual(m.BRIDGE_SECONDS,0.55)
 def test_safe_region(self):self.assertLess(m.FADE_BOTTOM,1310)
 def test_mask_preserves_caption(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'first.png';dst=Path(d)/'overlay.png'
   Image.new('RGB',(1080,1920),'white').save(src)
   m.make_bridge_image(src,dst);im=Image.open(dst)
   self.assertEqual(im.getpixel((200,300))[3],255)
   self.assertGreater(im.getpixel((200,1200))[3],0)
   self.assertEqual(im.getpixel((200,1230))[3],0)
   self.assertEqual(im.getpixel((200,1600))[3],0)
 def test_wrong_size_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'bad.png';Image.new('RGB',(100,100),'white').save(src)
   with self.assertRaises(ValueError):m.make_bridge_image(src,Path(d)/'out.png')
if __name__=='__main__':unittest.main()
