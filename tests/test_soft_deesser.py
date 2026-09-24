import unittest

from video_engine.soft_deesser import deesser_filter, release_contract


class SoftDeesserTests(unittest.TestCase):
    def test_default_filter_is_conservative(self):
        self.assertEqual(deesser_filter(), "deesser=i=0.15:m=0.25:f=0.60")

    def test_aggressive_settings_fail_closed(self):
        with self.assertRaises(ValueError):
            deesser_filter(intensity=0.30)
        with self.assertRaises(ValueError):
            deesser_filter(max_deessing=0.50)
        with self.assertRaises(ValueError):
            deesser_filter(frequency=0.90)

    def test_delivery_and_manual_release_policy(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["video_stream_passthrough"])
        self.assertTrue(c["caption_copy_preserved"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertFalse(c["claims_publish_ready"])

    def test_wrong_delivery_contract_fails_closed(self):
        with self.assertRaises(ValueError):
            release_contract(720, 1280)
        with self.assertRaises(ValueError):
            release_contract(sample_rate=44100)


if __name__ == "__main__":
    unittest.main()
