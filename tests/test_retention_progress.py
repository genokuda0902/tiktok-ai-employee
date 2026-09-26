import unittest

from video_engine.retention_progress import (
    AUTO_POST_ALLOWED,
    REQUIRES_HUMAN_APPROVAL,
    progress_filter,
    validate_delivery,
)


class RetentionProgressTests(unittest.TestCase):
    def test_filter_is_time_based_and_subtle(self):
        filt = progress_filter(20.0)
        self.assertIn("min(t/20.000000,1)", filt)
        self.assertIn("h=10", filt)

    def test_rejects_bad_duration_or_height(self):
        with self.assertRaises(ValueError):
            progress_filter(0)
        with self.assertRaises(ValueError):
            progress_filter(20, height=30)

    def test_delivery_gate_accepts_verified_shape(self):
        validate_delivery(1080, 1920, True, 0.0)

    def test_delivery_gate_rejects_wrong_shape_audio_or_black(self):
        for args in [(720, 1280, True, 0.0), (1080, 1920, False, 0.0), (1080, 1920, True, 0.5)]:
            with self.assertRaises(ValueError):
                validate_delivery(*args)

    def test_manual_release_policy_is_preserved(self):
        self.assertTrue(REQUIRES_HUMAN_APPROVAL)
        self.assertFalse(AUTO_POST_ALLOWED)


if __name__ == "__main__":
    unittest.main()
