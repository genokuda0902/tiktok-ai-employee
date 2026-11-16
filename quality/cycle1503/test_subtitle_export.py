import tempfile,unittest
from pathlib import Path
from subtitle_export import export
class Tests(unittest.TestCase):
 def test_missing(self):
  with self.assertRaises(FileNotFoundError): export("missing.mp4","missing.srt","out.mp4")
 def test_no_timing(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/"v.mp4").touch();(p/"c.srt").write_text("日本語")
   with self.assertRaises(ValueError): export(p/"v.mp4",p/"c.srt",p/"o.mp4")
 def test_no_japanese(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/"v.mp4").touch();(p/"c.srt").write_text("00:00:00,000 --> 00:00:01,000\nhello")
   with self.assertRaises(ValueError): export(p/"v.mp4",p/"c.srt",p/"o.mp4")
if __name__=="__main__": unittest.main()
