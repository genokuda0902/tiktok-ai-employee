import unittest
from qa import evaluate

class QATest(unittest.TestCase):
    def test_silent_fails(self):
        p={"streams":[{"codec_type":"video","codec_name":"h264","width":720,"height":1280}]}
        self.assertFalse(evaluate(p, narration_verified=True, subtitles_verified=True, rights_approved=True, employee_approved=True)["publication_approved"])
    def test_audio_alone_fails(self):
        p={"streams":[{"codec_type":"video","codec_name":"h264","width":720,"height":1280},{"codec_type":"audio","codec_name":"aac"}]}
        self.assertFalse(evaluate(p)["publication_approved"])
    def test_full_evidence_passes(self):
        p={"streams":[{"codec_type":"video","codec_name":"h264","width":720,"height":1280},{"codec_type":"audio","codec_name":"aac"}]}
        self.assertTrue(evaluate(p,narration_verified=True,subtitles_verified=True,rights_approved=True,employee_approved=True)["publication_approved"])

if __name__=="__main__": unittest.main()
