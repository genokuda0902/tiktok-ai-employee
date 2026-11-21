import unittest
from cycle1626_audio_gate import assess

class AudioGateTests(unittest.TestCase):
    def test_silent_fails_even_if_all_approvals_true(self):
        m={"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"12"}}
        r=assess(m,japanese_speech_verified=True,captions_synced=True,assets_approved=True,employee_approved=True)
        self.assertFalse(r["posting_allowed"])
        self.assertFalse(r["checks"]["audio_stream"])
    def test_tone_track_not_proof_of_japanese(self):
        m={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"12"}}
        r=assess(m,captions_synced=True,assets_approved=True,employee_approved=True)
        self.assertFalse(r["posting_allowed"])
        self.assertFalse(r["checks"]["japanese_speech_verified"])
    def test_all_requirements_explicit(self):
        m={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"12"}}
        self.assertTrue(assess(m,japanese_speech_verified=True,captions_synced=True,assets_approved=True,employee_approved=True)["posting_allowed"])
if __name__=="__main__":unittest.main()
