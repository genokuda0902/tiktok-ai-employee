import unittest
from qa_video import evaluate

class VideoQualityTests(unittest.TestCase):
    def test_silent_fails(self):
        p={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        self.assertIn("audio_stream_missing",evaluate(p)["issues"])
    def test_audio_is_not_japanese_proof(self):
        p={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertIn("japanese_speech_unverified",evaluate(p)["issues"])
    def test_requires_employee_approval(self):
        p={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertIn("employee_approval_missing",evaluate(p,japanese_voice_verified=True,captions_verified=True,rights_approved=True)["issues"])
    def test_resolution(self):
        p={"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}]}
        self.assertIn("portrait_1080x1920_required",evaluate(p)["issues"])
if __name__=="__main__":unittest.main()
