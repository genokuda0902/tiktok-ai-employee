import unittest
from video_engine.audio_mastering import narration_master_filter, mastering_contract

class AudioMasteringTest(unittest.TestCase):
    def test_filter_targets_speech_loudness(self):
        f = narration_master_filter()
        self.assertIn("highpass=f=80", f)
        self.assertIn("loudnorm=I=-16:TP=-1.5:LRA=7", f)

    def test_contract_accepts_tiktok_portrait(self):
        c = mastering_contract(1080, 1920, 48000, 2)
        self.assertTrue(c["zero_cost"])
        self.assertFalse(c["auto_post"])

    def test_contract_rejects_wrong_resolution(self):
        with self.assertRaises(ValueError):
            mastering_contract(720, 1280, 48000, 2)

    def test_contract_rejects_wrong_audio(self):
        with self.assertRaises(ValueError):
            mastering_contract(1080, 1920, 44100, 2)

if __name__ == "__main__":
    unittest.main()
