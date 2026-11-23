import unittest
from quality.cycle1675_audio_gate import evaluate

class GateTests(unittest.TestCase):
    def test_no_audio_blocks(self):
        p={"streams":[{"codec_type":"video","width":720,"height":1280}]}
        self.assertFalse(evaluate(p,japanese_speech_verified=True,captions_synced=True,assets_approved=True,employee_approved=True)["posting_allowed"])
    def test_audio_without_speech_proof_blocks(self):
        p={"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}]}
        self.assertFalse(evaluate(p,captions_synced=True,assets_approved=True,employee_approved=True)["posting_allowed"])
    def test_all_gates_required(self):
        p={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertTrue(evaluate(p,japanese_speech_verified=True,captions_synced=True,assets_approved=True,employee_approved=True)["posting_allowed"])

if __name__=="__main__": unittest.main()
