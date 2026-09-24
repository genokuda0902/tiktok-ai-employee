import unittest

from video_engine.audio_mastering import mastering_contract, narration_master_filter


class NarrationMasteringTests(unittest.TestCase):
    def test_filter_is_deterministic_and_zero_cost(self):
        chain = narration_master_filter()
        self.assertIn("highpass=f=80", chain)
        self.assertIn("lowpass=f=12000", chain)
        self.assertIn("acompressor=", chain)
        self.assertIn("loudnorm=I=-16:TP=-1.5:LRA=7", chain)

    def test_contract_requires_portrait_delivery(self):
        with self.assertRaises(ValueError):
            mastering_contract(720, 1280, 48000, 2)

    def test_contract_requires_48k_stereo(self):
        with self.assertRaises(ValueError):
            mastering_contract(1080, 1920, 44100, 2)
        with self.assertRaises(ValueError):
            mastering_contract(1080, 1920, 48000, 1)

    def test_contract_keeps_manual_approval_and_no_auto_post(self):
        contract = mastering_contract(1080, 1920, 48000, 2)
        self.assertTrue(contract["zero_cost"])
        self.assertTrue(contract["preserve_video"])
        self.assertTrue(contract["preserve_burned_captions"])
        self.assertTrue(contract["human_approval_required"])
        self.assertTrue(contract["manual_post_only"])
        self.assertFalse(contract["auto_post"])


if __name__ == "__main__":
    unittest.main()
