import unittest
from quality.cycle1443_gate import inspect_probe

class GateTests(unittest.TestCase):
    def test_silent_video_rejected(self):
        p={"streams":[{"codec_type":"video","codec_name":"h264","width":1080,"height":1920}]}
        result=inspect_probe(p,captions_embedded=True)
        self.assertFalse(result["publication_approved"])
        self.assertIn("audio_missing",result["issues"])
    def test_audio_track_is_not_speech_proof(self):
        p={"streams":[{"codec_type":"video","codec_name":"h264","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}
        self.assertIn("japanese_voice_unverified",inspect_probe(p)["issues"])
    def test_all_gates_require_explicit_approval(self):
        p={"streams":[{"codec_type":"video","codec_name":"h264","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}
        self.assertTrue(inspect_probe(p,captions_embedded=True,japanese_voice_verified=True,rights_approved=True,employee_approved=True)["publication_approved"])
if __name__=="__main__":unittest.main()
