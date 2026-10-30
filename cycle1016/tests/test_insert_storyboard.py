import importlib.util
from pathlib import Path
import tempfile
import unittest

module_path=Path(__file__).resolve().parents[1]/'source'/'insert_storyboard.py'
spec=importlib.util.spec_from_file_location('insert_storyboard',module_path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TestStoryboard(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_source_sha_gate(self):self.assertEqual(len(m.SOURCE_SHA),64)
 def test_insert_timing(self):
  self.assertEqual(len(m.INSERTS),2)
  self.assertTrue(all(s['end']>s['start'] and s['start']>0 for s in m.INSERTS))
  self.assertTrue(m.INSERTS[0]['end']<m.INSERTS[1]['start'])
 def test_original_content(self):
  self.assertTrue(all(len(s['rows'])==3 for s in m.INSERTS))
  self.assertEqual([s['kind'] for s in m.INSERTS],['tasks','template'])
 def test_fade(self):
  self.assertEqual(m.smooth(-1),0);self.assertEqual(m.smooth(2),1)
  self.assertAlmostEqual(m.smooth(.5),.5)
 def test_overlay_dimensions(self):self.assertEqual(m.make_frame(m.INSERTS[0],.5).size,(860,780))
 def test_transparent_ends(self):
  for t in [0,1]:
   im=m.make_frame(m.INSERTS[0],t)
   self.assertEqual(im.getpixel((25,50))[3],0)
 def test_fail_closed_missing_source(self):
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):m.validate(Path(tmp)/'missing.mp4',Path(tmp)/'out.mp4','ai_work',True,False)
 def test_fail_closed_unknown_genre(self):
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):m.validate(Path(tmp)/'missing.mp4',Path(tmp)/'out.mp4','invalid',True,False)
 def test_requires_review_flag(self):
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):m.validate(Path(tmp)/'missing.mp4',Path(tmp)/'out.mp4','ai_work',False,False)
if __name__=='__main__':unittest.main()
