import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
from .chart_bridge import ACCENTS,START,END,SAFE_Y,SAMPLE,frame,validate,sha256,render
class ChartBridgeTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(ACCENTS),10)
 def test_distinct_palettes(self):self.assertEqual(len(set(ACCENTS.values())),10)
 def test_scene_range(self):self.assertEqual((START,END,END-START),(380,429,49))
 def test_chart_totals(self):self.assertEqual(validate(SAMPLE),[46,29])
 def test_totals_derive_from_data(self):
  x={**SAMPLE,'series':[{'name':'A','values':[1,2,3]},{'name':'B','values':[4,5,6]}]}
  self.assertEqual(validate(x),[6,15])
 def test_no_bad_numbers(self):
  x={**SAMPLE,'series':[{'name':'A','values':[1,-2,3]},SAMPLE['series'][1]]}
  with self.assertRaises(ValueError):validate(x)
 def test_reject_missing_note(self):
  with self.assertRaises(ValueError):validate({**SAMPLE,'note':''})
 def test_safe_subtitle_island(self):
  for i in [0,15,35,48]:self.assertIsNone(frame(i).crop((0,SAFE_Y,1080,1920)).getbbox())
 def test_animation_changes(self):self.assertNotEqual(frame(0).tobytes(),frame(45).tobytes())
 def test_ten_genres_draw(self):
  for g in ACCENTS:self.assertEqual(frame(45,genre=g).size,(1080,1920))
 def test_bad_genre(self):
  with self.assertRaises(ValueError):frame(0,genre='unknown')
 def test_hash(self):
  with TemporaryDirectory() as td:
   p=Path(td)/'x';p.write_bytes(b'abc')
   self.assertEqual(sha256(p),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
 def test_fail_closed(self):
  with self.assertRaises(FileNotFoundError):render('/not/exists','/tmp/out','bad')
 def test_no_posting(self):
  code=Path(__file__).with_name('chart_bridge.py').read_text()
  for x in ('api.tiktok.com','requests.post(','tiktok.com/upload'):self.assertNotIn(x,code)
if __name__=='__main__':unittest.main()
