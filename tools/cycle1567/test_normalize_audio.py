import unittest
from pathlib import Path
from unittest.mock import patch
from normalize_audio import normalize

class TestNormalize(unittest.TestCase):
    def test_same_path_rejected(self):
        with self.assertRaises(ValueError): normalize(Path("same.mp4"),Path("same.mp4"))
    @patch("normalize_audio.subprocess.run")
    def test_command(self, run):
        normalize(Path("a.mp4"),Path("b.mp4"))
        args=run.call_args.args[0]
        assert "0:s?" in args
        assert "loudnorm=I=-16:TP=-1.5:LRA=11" in args
