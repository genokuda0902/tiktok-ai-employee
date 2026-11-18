import unittest
from unittest.mock import patch
import audio_gate

class GateTests(unittest.TestCase):
    def test_audio_only_not_narration(self):
        with patch.object(audio_gate, "probe", return_value={"streams": [
            {"codec_type": "video", "width": 1080, "height": 1920},
            {"codec_type": "audio", "codec_name": "aac"}]}):
            result = audio_gate.assess("demo.mp4", rights_approved=True,
                                       employee_approved=True)
            self.assertFalse(result["publication_approved"])
            self.assertIn("japanese_narration_unverified", result["reasons"])

    def test_silent_fails(self):
        with patch.object(audio_gate, "probe", return_value={"streams": [
            {"codec_type": "video", "width": 1080, "height": 1920}]}):
            self.assertIn("audio_missing", audio_gate.assess("demo.mp4")["reasons"])

    def test_all_evidence_passes(self):
        with patch.object(audio_gate, "probe", return_value={"streams": [
            {"codec_type": "video", "width": 1080, "height": 1920},
            {"codec_type": "audio", "codec_name": "aac"}]}):
            self.assertTrue(audio_gate.assess("demo.mp4", True, True, True, True)["publication_approved"])

if __name__ == "__main__":
    unittest.main()
