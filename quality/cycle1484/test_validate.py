import unittest
from unittest.mock import patch
from quality.cycle1484.validate import validate

class GateTests(unittest.TestCase):
    @patch("quality.cycle1484.validate.probe")
    def test_silent_video_is_blocked(self, p):
        p.return_value = {"streams":[{"codec_type":"video","width":720,"height":1280}]}
        result = validate("synthetic.mp4", captions_synced=True, rights_approved=True, employee_approved=True)
        self.assertFalse(result["posting_allowed"])
        self.assertIn("japanese_narration_not_verified", result["reasons"])

    @patch("quality.cycle1484.validate.probe")
    def test_unapproved_video_is_blocked(self, p):
        p.return_value = {"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertFalse(validate("synthetic.mp4", narration_verified=True, captions_synced=True)["posting_allowed"])

if __name__ == "__main__":
    unittest.main()
