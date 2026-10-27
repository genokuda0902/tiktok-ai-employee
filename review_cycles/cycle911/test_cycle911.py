"""Offline stdlib policy and geometry checks. Final private MP4 is local QA only."""
import ast
import hashlib
import importlib.util
import pathlib
import tempfile
import unittest

MOD=pathlib.Path(__file__).with_name('calc_capture_overlay.py')
spec=importlib.util.spec_from_file_location('cycle911_overlay',MOD)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestCycle911(unittest.TestCase):
 def test_syntax(self):ast.parse(MOD.read_text())
 def test_genre_count(self):self.assertEqual(len(m.GENRE_ACCENTS),10)
 def test_caption_safe(self):self.assertLess(m.OVERLAY_Y+m.OVERLAY_H,m.CAPTION_SAFE_Y)
 def test_exact_scene(self):self.assertEqual(m.END_FRAME-m.START_FRAME,87)
 def test_policy(self):self.assertEqual(m.POLICY,'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED')
 def test_no_posting(self):
  s=MOD.read_text()
  self.assertNotIn('upload_video(',s)
  self.assertNotIn('post_to_tiktok(',s)
 def test_fail_closed(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d);src=p/'source.mp4';src.write_bytes(b'sample')
   screens=[]
   for i in range(3):
    f=p/f'{i}.png';f.write_bytes(b'local');screens.append(f)
   sha=hashlib.sha256(b'sample').hexdigest()
   with self.assertRaises(ValueError):m.validate(src,p/'public.mp4',screens,sha,'ai_work')
   with self.assertRaises(ValueError):m.validate(src,p/'ok_REVIEW_ONLY.mp4',screens,'wrong','ai_work')
   with self.assertRaises(ValueError):m.validate(src,p/'ok_REVIEW_ONLY.mp4',screens,sha,'unknown')
   with self.assertRaises(ValueError):m.validate(src,p/'ok_REVIEW_ONLY.mp4',screens[:2],sha,'ai_work')
 def test_stage_labels(self):self.assertEqual(len(m.STAGES),3)
 def test_local_demo_label(self):
  s=MOD.read_text()
  self.assertIn('LibreOffice Calc',s)
  self.assertIn('架空データ',s)

if __name__=='__main__':unittest.main()
