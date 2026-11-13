import unittest
from media_gate import inspect_streams

class GateTests(unittest.TestCase):
    def test_silent_video_rejected(self):
        probe={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        result=inspect_streams(probe,captions_synced=True,rights_approved=True,employee_approved=True)
        self.assertFalse(result["publication_approved"])
        self.assertIn("audio_missing",result["problems"])
    def test_approved_complete_video(self):
        probe={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}
        result=inspect_streams(probe,japanese_voice_verified=True,captions_synced=True,rights_approved=True,employee_approved=True)
        self.assertTrue(result["publication_approved"])
if __name__ == "__main__":
    unittest.main()
