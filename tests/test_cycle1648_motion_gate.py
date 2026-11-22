import unittest
from qa.cycle1648_motion_gate import evaluate

class GateTests(unittest.TestCase):
    def test_no_audio_fails(self):
        m={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        self.assertFalse(evaluate(m, captions_timed=True, japanese_speech_verified=True,
                                  asset_rights_approved=True, employee_approved=True)["posting_allowed"])
    def test_synthetic_audio_is_not_japanese_speech(self):
        m={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertFalse(evaluate(m, captions_timed=True, asset_rights_approved=True,
                                  employee_approved=True)["posting_allowed"])
    def test_unapproved_assets_fail(self):
        m={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertFalse(evaluate(m, captions_timed=True, japanese_speech_verified=True,
                                  employee_approved=True)["posting_allowed"])

if __name__=="__main__": unittest.main()
