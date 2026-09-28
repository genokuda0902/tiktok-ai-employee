import unittest

from video_engine.mobile_speech_presence import speech_presence_filter, safety_contract


class MobileSpeechPresenceTests(unittest.TestCase):
    def test_filter_is_bounded_and_phone_focused(self):
        f = speech_presence_filter()
        self.assertIn("highpass=f=90", f)
        self.assertIn("f=2800", f)
        self.assertIn("g=1.5", f)
        self.assertIn("alimiter=limit=0.93", f)

    def test_wrong_delivery_format_fails_closed(self):
        with self.assertRaises(ValueError):
            speech_presence_filter(720, 1280)
        with self.assertRaises(ValueError):
            speech_presence_filter(sample_rate=44100)

    def test_release_policy_and_timing_are_preserved(self):
        c = safety_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_timing"])
        self.assertTrue(c["preserve_caption_copy"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertLessEqual(c["presence_gain_db"], c["max_presence_gain_db"])


if __name__ == "__main__":
    unittest.main()
