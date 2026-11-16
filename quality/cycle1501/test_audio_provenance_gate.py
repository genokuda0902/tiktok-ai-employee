import unittest
from unittest.mock import patch
from types import SimpleNamespace
import json
from audio_provenance_gate import classify

class ProvenanceTests(unittest.TestCase):
    @patch("audio_provenance_gate.subprocess.run")
    def test_synthetic_cues_rejected_as_narration(self, run):
        run.return_value = SimpleNamespace(returncode=0, stdout=json.dumps({"streams":[{"codec_type":"video"},{"codec_type":"audio"}]}))
        self.assertEqual(classify("review.mp4", {"audio_origin":"synthetic_cues"})["reason"], "audio_is_not_narration")
    @patch("audio_provenance_gate.subprocess.run")
    def test_narration_without_sync_rejected(self, run):
        run.return_value = SimpleNamespace(returncode=0, stdout=json.dumps({"streams":[{"codec_type":"video"},{"codec_type":"audio"}]}))
        self.assertEqual(classify("review.mp4", {"audio_origin":"original_narration","japanese_speech_verified":True})["reason"], "caption_sync_unverified")
    @patch("audio_provenance_gate.subprocess.run")
    def test_unknown_origin_rejected(self, run):
        run.return_value = SimpleNamespace(returncode=0, stdout=json.dumps({"streams":[{"codec_type":"video"},{"codec_type":"audio"}]}))
        self.assertEqual(classify("review.mp4", {})["reason"], "unknown_audio_provenance")

if __name__ == "__main__":
    unittest.main()
