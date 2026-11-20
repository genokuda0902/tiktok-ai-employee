import unittest
from unittest.mock import patch, Mock
from pathlib import Path
import json
from audio_evidence import inspect

class AudioEvidenceTests(unittest.TestCase):
    @patch("audio_evidence.Path.is_file", return_value=True)
    @patch("audio_evidence.subprocess.run")
    def test_audio_is_not_narration_proof(self, run, exists):
        run.return_value = Mock(stdout=json.dumps({"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio","codec_name":"aac"}]}))
        result = inspect("sample.mp4")
        self.assertTrue(result["has_audio_track"])
        self.assertFalse(result["japanese_narration_verified"])
        self.assertFalse(result["posting_allowed"])
    @patch("audio_evidence.Path.is_file", return_value=True)
    @patch("audio_evidence.subprocess.run")
    def test_silent_fails_closed(self, run, exists):
        run.return_value = Mock(stdout=json.dumps({"streams":[{"codec_type":"video","width":720,"height":1280}]}))
        self.assertFalse(inspect("sample.mp4")["has_audio_track"])
    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError): inspect("nonexistent_media_1602.mp4")
if __name__ == "__main__": unittest.main()
