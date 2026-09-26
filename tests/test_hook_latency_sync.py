import unittest

from video_engine.hook_latency_sync import hook_latency_contract, ffmpeg_audio_filter


class HookLatencySyncTests(unittest.TestCase):
    def test_measured_leading_silence_is_removed_without_touching_video_or_copy(self):
        c = hook_latency_contract(0.44, 20.0)
        self.assertIn("atrim=start=0.44", c["audio_filter"])
        self.assertIn("atrim=duration=20", c["audio_filter"])
        self.assertTrue(c["video_copy"])
        self.assertTrue(c["caption_copy_unchanged"])

    def test_rejects_unmeasured_large_shift(self):
        with self.assertRaises(ValueError):
            hook_latency_contract(0.76)
        with self.assertRaises(ValueError):
            hook_latency_contract(-0.01)

    def test_release_safety_and_zero_cost_are_preserved(self):
        c = hook_latency_contract(0.44)
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])

    def test_filter_default_matches_measured_cycle40_baseline(self):
        self.assertEqual(ffmpeg_audio_filter(), hook_latency_contract(0.44)["audio_filter"])

    def test_zero_shift_is_valid_for_already_trimmed_audio(self):
        self.assertIn("atrim=start=0.00", hook_latency_contract(0.0)["audio_filter"])


if __name__ == "__main__":
    unittest.main()
