import unittest
from unittest.mock import patch, Mock
from src.review_audio_level import probe_audio, render_review

class AudioLevelTests(unittest.TestCase):
    @patch("src.review_audio_level.subprocess.run")
    def test_probe_present(self, run):
        run.return_value=Mock(stdout='{"streams":[{"codec_name":"aac"}]}')
        self.assertEqual(probe_audio("a.mp4")["codec_name"],"aac")

    @patch("src.review_audio_level.subprocess.run")
    def test_probe_missing(self, run):
        run.return_value=Mock(stdout='{"streams":[]}')
        with self.assertRaises(ValueError): probe_audio("a.mp4")

    def test_missing_input(self):
        with self.assertRaises(FileNotFoundError): render_review("/does/not/exist.mp4","out.mp4")

if __name__=="__main__": unittest.main()
