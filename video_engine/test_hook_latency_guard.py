import unittest
from video_engine.hook_latency_guard import HookLatencyPlan, release_contract

class HookLatencyGuardTests(unittest.TestCase):
    def test_bounded_lead_silence_is_shifted_to_tail(self):
        f = HookLatencyPlan(0.094, target_duration=12.233).ffmpeg_audio_filter()
        self.assertIn("atrim=start=0.094", f)
        self.assertIn("apad=pad_dur=0.094", f)
        self.assertIn("atrim=duration=12.233", f)

    def test_excessive_shift_fails_closed(self):
        with self.assertRaises(ValueError):
            HookLatencyPlan(0.2, target_duration=12.233).validate()

    def test_invalid_duration_fails_closed(self):
        with self.assertRaises(ValueError):
            HookLatencyPlan(0.05, target_duration=0).validate()

    def test_release_policy_stays_manual(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["preserve_video"])
        self.assertTrue(c["preserve_burned_captions"])
        self.assertTrue(c["human_approval_required"])
        self.assertTrue(c["manual_post_only"])
        self.assertFalse(c["auto_post"])

if __name__ == "__main__":
    unittest.main()
