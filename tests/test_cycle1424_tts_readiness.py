import unittest
from quality.cycle1424_tts_readiness import check_offline_japanese_voice, assert_narrated_video

class TestTTSReadiness(unittest.TestCase):
    def test_unknown_voice_fails_closed(self):
        self.assertFalse(check_offline_japanese_voice()["ready"])
    def test_silent_video_rejected(self):
        with self.assertRaises(ValueError):
            assert_narrated_video(False,False,False,True,False)
    def test_all_gates(self):
        assert_narrated_video(True,True,True,True,True)

if __name__ == "__main__":
    unittest.main()
