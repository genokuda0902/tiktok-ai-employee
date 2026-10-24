import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image

spec=importlib.util.spec_from_file_location('render817',Path(__file__).with_name('render817.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TestCycle817(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(m.GENRE_ACCENTS),10)
  self.assertIn('sales_business',m.GENRE_ACCENTS)
 def test_narration_text_matches(self):
  for parts in m.PHRASES:self.assertGreater(len(''.join(parts)),5)
  self.assertEqual(len(m.PHRASES),8)
 def test_scene_frames(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'timing.json'
   p.write_text(json.dumps({'sentences':[{'text':''.join(parts),'seconds':s} for parts,s in zip(m.PHRASES,[3.355,3.085,3.025,3.285,3.265,3.36,2.97,3.495])]}),encoding='utf8')
   boundaries=m.scene_frames(p)
   self.assertEqual(boundaries,[0,101,193,284,382,480,581,670,775])
 def test_reject_mismatched_narration(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'timing.json';p.write_text(json.dumps({'sentences':[{'text':'wrong','seconds':3.2}]*8}))
   with self.assertRaises(ValueError):m.scene_frames(p)
 def test_clean_source_removes_old_caption_area(self):
  with tempfile.TemporaryDirectory() as t:
   src=Path(t)/'s.png';dst=Path(t)/'d.png'
   Image.new('RGB',(1080,1920),'red').save(src)
   m.clean_slide(src,dst,'#5DE7C4')
   im=Image.open(dst)
   self.assertEqual(im.getpixel((500,1180)),(9,31,49))
   self.assertEqual(im.getpixel((500,1000)),(255,0,0))
 def test_pause_guided_boundaries_monotonic(self):
  cuts=m.speech_phases(0,3.0,[(0,0.2),(1.0,1.3),(2.0,2.2)])
  self.assertEqual(len(cuts),4)
  self.assertTrue(all(x<y for x,y in zip(cuts,cuts[1:])))
 def test_filter_renders_all_scenes(self):
  x=m.make_filter([101,92,91,98,98,101,89,105],Path('/tmp/captions.ass'))
  self.assertIn('concat=n=8:v=1:a=0',x)
  self.assertEqual(x.count('zoompan='),8)
 def test_no_external_network_or_post_calls(self):
  code=Path(m.__file__).read_text()
  for forbidden in ['requests.post(', 'httpx.post(', 'tiktok.upload(', 'curl https://']:
   self.assertNotIn(forbidden,code)

if __name__=='__main__':unittest.main()
