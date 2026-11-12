import unittest
from unittest.mock import patch
from audio_evidence import inspect

class AudioEvidenceTest(unittest.TestCase):
    @patch("subprocess.check_output", return_value='{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}')
    def test_audio_stream_not_equivalent_to_narration(self, _):
        report=inspect("demo.mp4")
        self.assertTrue(report["audio_track_present"])
        self.assertFalse(report["japanese_narration_verified"])
        self.assertFalse(report["publication_allowed"])

    @patch("subprocess.check_output", return_value='{"streams":[{"codec_type":"video","width":720,"height":1280}]}')
    def test_no_audio_and_low_resolution_block(self, _):
        report=inspect("demo.mp4",True,True,True,True)
        self.assertFalse(report["audio_track_present"])
        self.assertFalse(report["resolution_ok"])
        self.assertFalse(report["publication_allowed"])

if __name__=="__main__": unittest.main()
