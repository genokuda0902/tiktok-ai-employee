import unittest
from audio_gate import assess

GOOD = {"streams": [
    {"codec_type": "video", "codec_name": "h264", "width": 1080, "height": 1920},
    {"codec_type": "audio", "codec_name": "aac"}]}

class GateTests(unittest.TestCase):
    def test_silent_is_blocked(self):
        p = {"streams": GOOD["streams"][:1]}
        result = assess(p, narration_verified=True, captions_synced=True,
                        asset_rights_approved=True, employee_approved=True)
        self.assertFalse(result["posting_allowed"])
        self.assertIn("audio_stream_missing", result["reasons"])

    def test_audio_alone_is_not_approval(self):
        self.assertFalse(assess(GOOD)["posting_allowed"])

    def test_fully_verified_passes(self):
        self.assertTrue(assess(GOOD, narration_verified=True,
            captions_synced=True, asset_rights_approved=True,
            employee_approved=True)["posting_allowed"])

if __name__ == "__main__":
    unittest.main()
