"""Cycle671 caption/narration contract tests; no third-party media required."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[1]/'video_engine'/'quality'/'cycle671_caption_voice.py'
spec=importlib.util.spec_from_file_location('cycle671_caption_voice',SOURCE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CaptionContractTests(unittest.TestCase):
 def test_ten_genres_and_complete_timeline(self):
  self.assertEqual(len(m.GENRES),10);self.assertTrue(m.validate_cues())
 def test_gap_rejected(self):
  cues=list(m.CUES);cues[1]=(2.2,4.,cues[1][2],cues[1][3])
  with self.assertRaises(ValueError):m.validate_cues(cues)
 def test_long_caption_rejected(self):
  cues=list(m.CUES);cues[0]=(0,2,'長'*23,'発話')
  with self.assertRaises(ValueError):m.validate_cues(cues)
 def test_srt_full_coverage_and_ass_safe_area(self):
  with tempfile.TemporaryDirectory() as tmp:
   srt,ass=m.write_subtitles(tmp)
   s=srt.read_text(encoding='utf-8');a=ass.read_text(encoding='utf-8')
   self.assertIn('00:00:20,000',s)
   self.assertEqual(s.count('-->'),10)
   self.assertEqual(a.count('Dialogue:'),10)
   self.assertIn('100,100,170,1',a)
 def test_voice_gate_fails_without_engine(self):
  original=m.find_openjtalk_assets
  try:
   m.find_openjtalk_assets=lambda: (_ for _ in ()).throw(FileNotFoundError('not installed'))
   with self.assertRaises(FileNotFoundError):m.synthesize_voice('/tmp')
  finally:m.find_openjtalk_assets=original
 def test_missing_baseline_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(FileNotFoundError):m.compose(Path(tmp)/'missing.mp4',Path(tmp)/'out.mp4')
 def test_result_not_announced_before_evidence(self):
  for start,end,caption,_ in m.CUES:
   if start<12.4:self.assertNotIn('650',caption)
 def test_time_formats(self):
  self.assertEqual(m.fmt_srt(20),'00:00:20,000')
  self.assertEqual(m.fmt_ass(2.34),'0:00:02.34')
if __name__=='__main__':unittest.main()
