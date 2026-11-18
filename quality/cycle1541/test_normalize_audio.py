import unittest
from unittest.mock import patch
from normalize_audio import normalize

class Tests(unittest.TestCase):
    @patch("normalize_audio.probe",return_value={"streams":[{"codec_type":"video"}]})
    def test_no_audio_rejected(self,_):
        with self.assertRaisesRegex(ValueError,"audio"):
            normalize("in.mp4","out.mp4")

    @patch("normalize_audio.subprocess.run")
    @patch("normalize_audio.probe",return_value={"streams":[{"codec_type":"video"},{"codec_type":"audio"}]})
    def test_normalization_and_decode(self,_,run):
        normalize("in.mp4","out.mp4")
        self.assertEqual(run.call_count,2)
        self.assertIn("loudnorm=I=-16:TP=-1.5:LRA=11",run.call_args_list[0].args[0])
