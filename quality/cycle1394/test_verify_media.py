import unittest
from verify_media import assess

class TestFailClosed(unittest.TestCase):
    def test_silent_video_blocked(self):
        m = {"streams": [{"codec_type":"video","width":1080,"height":1920}]}
        r = assess(m, True, True, True, True)
        self.assertIn("audio_stream_missing", r["failures"])
        self.assertFalse(r["posting_allowed"])

    def test_all_gates_required(self):
        m = {"streams": [{"codec_type":"video","width":1080,"height":1920},
                         {"codec_type":"audio","codec_name":"aac"}]}
        self.assertFalse(assess(m)["posting_allowed"])
        self.assertTrue(assess(m, True, True, True, True)["posting_allowed"])

    def test_low_resolution_blocked(self):
        m = {"streams": [{"codec_type":"video","width":720,"height":1280},
                         {"codec_type":"audio"}]}
        self.assertIn("resolution_or_video_missing",
                      assess(m, True, True, True, True)["failures"])

if __name__ == "__main__":
    unittest.main()
