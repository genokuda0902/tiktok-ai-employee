import unittest
from audio_diagnostics import inspect

class AudioDiagnosticsTests(unittest.TestCase):
    def test_missing_file_fails(self):
        with self.assertRaises(FileNotFoundError):
            inspect("/nonexistent/cycle1580.mp4")

    def test_unverified_audio_never_passes(self):
        import unittest.mock as mock
        import json
        payload = {"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio","codec_name":"aac"}],"format":{"duration":"12"}}
        with mock.patch("audio_diagnostics.Path.is_file",return_value=True), mock.patch("audio_diagnostics.subprocess.check_output",return_value=json.dumps(payload)):
            result=inspect("fake.mp4")
        self.assertTrue(result["has_audio"])
        self.assertFalse(result["publication_approved"])
        self.assertIn("JAPANESE_SPEECH_UNVERIFIED",result["blockers"])

if __name__ == "__main__":
    unittest.main()
