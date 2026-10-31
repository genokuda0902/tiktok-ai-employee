import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
from .proof_before_after import PALETTES,START,END,FPS,SAFE_Y,frame,sha256,render
class ProofTests(unittest.TestCase):
 def test_10_genres(self):self.assertEqual(len(PALETTES),10)
 def test_unique_palettes(self):self.assertEqual(len(set(PALETTES.values())),10)
 def test_scene_range(self):self.assertEqual((START,END,END-START),(429,520,91))
 def test_scene_timing(self):self.assertAlmostEqual(START/FPS,14.3)
 def test_frame_dimensions(self):self.assertEqual(frame(0,Image.new('RGB',(836,345))).size,(1080,1920))
 def test_caption_safe_region_transparent(self):
  for i in (0,35,65,90):
   im=frame(i,Image.new('RGB',(836,345)))
   self.assertIsNone(im.getbbox() if False else im.crop((0,SAFE_Y,1080,1920)).getbbox())
 def test_frames_animated(self):
  proof=Image.new('RGB',(836,345))
  self.assertNotEqual(frame(0,proof).tobytes(),frame(60,proof).tobytes())
 def test_all_genres_render(self):
  proof=Image.new('RGB',(836,345))
  for genre in PALETTES:
   with self.subTest(genre=genre):self.assertEqual(frame(90,proof,genre).size,(1080,1920))
 def test_unknown_genre_rejected(self):
  with self.assertRaises(ValueError):frame(0,Image.new('RGB',(836,345)),'unknown')
 def test_hash(self):
  with TemporaryDirectory() as td:
   p=Path(td)/'x';p.write_bytes(b'abc')
   self.assertEqual(sha256(p),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
 def test_missing_source_fail_closed(self):
  with self.assertRaises(FileNotFoundError):render('/no/file','/tmp/out','fake')
 def test_no_posting(self):
  src=Path(__file__).with_name('proof_before_after.py').read_text()
  for x in ('tiktok.com/upload','api.tiktok.com','requests.post('):self.assertNotIn(x,src)
if __name__=='__main__':unittest.main()
