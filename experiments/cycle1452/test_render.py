from pathlib import Path
import unittest
from render import render
class TestRender(unittest.TestCase):
    def test_missing_source_fails_closed(self):
        with self.assertRaises(FileNotFoundError): render(Path('/no-source.mp4'),Path('/no-captions.srt'),Path('/tmp/never.mp4'))
    def test_caption_file_exists(self):
        self.assertIn('合計をまだ手入力',Path(__file__).with_name('captions.srt').read_text(encoding='utf8'))
if __name__=='__main__': unittest.main()
