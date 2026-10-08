import unittest
from src.cycle424_native_voice_probe import CAPTIONS,GENRES,W,H,FPS,SR
class ContractTests(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(GENRES),10);self.assertEqual(len(set(GENRES)),10)
 def test_japanese_captions(self): self.assertEqual(len(CAPTIONS),7);self.assertTrue(all(any(ord(c)>0x3000 for c in t) for t in CAPTIONS))
 def test_resolution(self): self.assertEqual((W,H,FPS,SR),(1080,1920,30,24000))
 def test_no_posting(self):
  import inspect
  from src import cycle424_native_voice_probe as m
  self.assertNotIn("upload_video",inspect.getsource(m))
if __name__=="__main__":unittest.main()
