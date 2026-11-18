import unittest
from pathlib import Path
from unittest.mock import patch
from render import render

class TestCaptionRender(unittest.TestCase):
    def test_missing_source_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            render(Path('/missing.mp4'),Path('/missing.srt'),Path('/out.mp4'))
    def test_command_preserves_audio_and_selectable_subtitle(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            root=Path(tmp)
            source=root/'in.mp4'; srt=root/'ja.srt'
            source.write_bytes(b'x'); srt.write_text('test',encoding='utf8')
            with patch('subprocess.run') as run:
                render(source,srt,root/'out.mp4')
                args=run.call_args.args[0]
                self.assertIn('0:a:0',args)
                self.assertIn('0:s:0',args)
                self.assertIn('copy',args)
                self.assertIn('mov_text',args)
if __name__=='__main__': unittest.main()
