import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from tools.normalize_audio import normalize

class TestNormalize(unittest.TestCase):
    def test_missing_source(self):
        with TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                normalize(Path(d)/'missing.mp4',Path(d)/'out.mp4')
    def test_audio_filter_video_copy(self):
        with TemporaryDirectory() as d:
            src=Path(d)/'input.mp4'; src.touch()
            with patch('tools.normalize_audio.subprocess.run') as run:
                normalize(src,Path(d)/'output.mp4')
                args=run.call_args.args[0]
                self.assertIn('loudnorm=I=-16:TP=-2:LRA=11',args)
                self.assertEqual(args[args.index('-c:v')+1],'copy')
                self.assertEqual(args[args.index('-ar')+1],'48000')
