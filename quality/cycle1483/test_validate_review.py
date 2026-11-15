import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).parent))
import validate_review

class QualityGateTests(unittest.TestCase):
    @patch("validate_review.subprocess.check_output")
    def test_silent_video_is_not_approved(self, probe):
        probe.return_value = '{"streams":[{"codec_type":"video","width":720,"height":1280}]}'
        result = validate_review.inspect("sample.mp4")
        self.assertFalse(result["audio_present"])
        self.assertFalse(result["posting_allowed"])
        self.assertEqual(result["status"], "PUBLICATION_NOT_APPROVED")

    @patch("validate_review.subprocess.check_output")
    def test_audio_stream_does_not_prove_japanese_voice(self, probe):
        probe.return_value = '{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}'
        result = validate_review.inspect("sample.mp4")
        self.assertTrue(result["audio_present"])
        self.assertFalse(result["japanese_narration_verified"])
        self.assertFalse(result["posting_allowed"])

if __name__ == "__main__":
    unittest.main()
