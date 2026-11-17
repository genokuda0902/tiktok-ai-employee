import unittest
from unittest.mock import patch
from qa.audio_proof_gate import review

class GateTests(unittest.TestCase):
    @patch("qa.audio_proof_gate.probe")
    def test_audio_stream_does_not_prove_speech(self,p):
        p.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        r=review("dummy.mp4",assets_approved=True,human_approved=True,captions_verified=True)
        self.assertFalse(r["publishable"])
        self.assertIn("japanese_speech_unverified",r["problems"])
    @patch("qa.audio_proof_gate.probe")
    def test_silent_video_is_rejected(self,p):
        p.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        self.assertIn("missing_audio",review("dummy.mp4")["problems"])
    @patch("qa.audio_proof_gate.probe")
    def test_full_evidence_passes(self,p):
        p.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertTrue(review("dummy.mp4",speech_verified=True,captions_verified=True,assets_approved=True,human_approved=True)["publishable"])

if __name__=="__main__": unittest.main()
