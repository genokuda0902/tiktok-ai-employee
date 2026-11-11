import tempfile
import unittest
from pathlib import Path
from render import burn

class RenderTest(unittest.TestCase):
    def test_missing_inputs_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            with self.assertRaises(FileNotFoundError): burn(p/"absent.mp4",p/"absent.srt",p/"out.mp4")
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/"a.mp4").touch();(p/"a.srt").write_text("x")
            with self.assertRaises(ValueError): burn(p/"a.mp4",p/"a.srt",p/"a.mp4")
if __name__=="__main__": unittest.main()
