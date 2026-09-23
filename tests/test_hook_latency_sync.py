import unittest

from video_engine.hook_latency_sync import hook_latency_contract, ffmpeg_audio_filter


class HookLatencySyncTests(unittest.TestCase):
    def test_measured_leading_silence_is_removed_without_touching_video_or_copy(self):
        c = hook_latency_contract(0.42, 20.0)
        self.assertIn("atrim=start=0.42", c["audio_filter"])
        self.assertIn("atrim=duration=20", c["audio_filter"])
        self.assertTrue(c["video_copy"])
        self.assertTrue(c["caption_copy_unchanged"])

    def test_rejects_unmeasured_large_shift(self):
        with self.assertRaises(ValueError):
            hook_latency_contract(0.76)
        with self.assertRaises(ValueError):
            hook_latency_contract(-0.01)

    def test_release_safety_and_zero_cost_are_preserved(self):
        c = hook_latency_contract(0.42)
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])

    def test_filter_is_deterministic(self):
        self.assertEqual(ffmpeg_audio_filter(), hook_latency_contract(0.42)["audio_filter"])


if __name__ == "__main__":
    unittest.main()
