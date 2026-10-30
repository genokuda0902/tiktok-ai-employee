import importlib.util, tempfile, unittest
from pathlib import Path
from PIL import ImageDraw, ImageFont
p=Path(__file__).resolve().parents[1]/'source'/'prompt_completeness.py'
spec=importlib.util.spec_from_file_location('prompt_completeness',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestPrompt(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_exact_source_gate(self):self.assertEqual(len(m.SOURCE_SHA),64)
 def test_timing(self):self.assertLess(m.START,m.END);self.assertLess(m.END,11.4)
 def test_dimensions(self):self.assertEqual(m.frame(.5).size,(860,550))
 def test_transparent_edges(self):
  for p in (0,1):self.assertEqual(m.frame(p).getpixel((20,30))[3],0)
 def test_complete_prompt(self):self.assertTrue(m.LINES[-1].endswith('まとめて'))
 def test_all_text_fits(self):
  im=m.frame(.95);d=ImageDraw.Draw(im);f=ImageFont.truetype(m.BOLD,40)
  self.assertTrue(all(m.text_fits(d,s,f,746) for s in m.LINES))
 def test_reject_overflow(self):
  with self.assertRaises(ValueError):m.frame(.5,('とても長い日本語の説明を繰り返して書き続けることにより画面からはみ出してしまう文章', '普通','普通'))
 def test_reject_missing_rows(self):
  with self.assertRaises(ValueError):m.frame(.5,('one','two'))
 def test_reject_missing_source(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(ValueError):m.validate(Path(t)/'none.mp4',Path(t)/'out.mp4','ai_work',True,False)
 def test_reject_no_review(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(ValueError):m.validate(Path(t)/'none.mp4',Path(t)/'out.mp4','ai_work',False,False)
 def test_reject_unknown_genre(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(ValueError):m.validate(Path(t)/'none.mp4',Path(t)/'out.mp4','unknown',True,False)
if __name__=='__main__':unittest.main()
