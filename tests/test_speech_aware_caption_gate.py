import unittest
from video_engine.speech_aware_caption_gate import Interval, render_policy, speech_intervals, validate_silences


class SpeechAwareCaptionGateTests(unittest.TestCase):
    def test_speech_intervals_are_complement_of_silence(self):
        silences = [Interval(1.5, 2.1), Interval(2.85, 3.29)]
        self.assertEqual(
            speech_intervals(silences, 4.0),
            [Interval(0.0, 1.5), Interval(2.1, 2.85), Interval(3.29, 4.0)],
        )

    def test_overlap_fails_closed(self):
        with self.assertRaises(ValueError):
            validate_silences([Interval(1.0, 2.0), Interval(1.9, 2.5)], 4.0)

    def test_out_of_bounds_fails_closed(self):
        with self.assertRaises(ValueError):
            validate_silences([Interval(3.0, 4.2)], 4.0)

    def test_policy_preserves_manual_release(self):
        policy = render_policy()
        self.assertTrue(policy["zero_cost"])
        self.assertTrue(policy["local_audio_analysis_only"])
        self.assertTrue(policy["caption_hidden_during_silence"])
        self.assertTrue(policy["human_quality_review_required"])
        self.assertFalse(policy["auto_post"])


if __name__ == "__main__":
    unittest.main()
