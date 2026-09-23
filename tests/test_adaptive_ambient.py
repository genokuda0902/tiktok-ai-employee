import unittest

from video_engine.adaptive_ambient import adaptive_ambient_contract, adaptive_ambient_filter


class AdaptiveAmbientTests(unittest.TestCase):
    def test_filter_ducks_bed_under_narration(self):
        f = adaptive_ambient_filter(20.0)
        self.assertIn("anoisesrc=color=pink", f)
        self.assertIn("sidechaincompress=", f)
        self.assertIn("amix=inputs=2", f)
        self.assertIn("loudnorm=I=-16:TP=-1.5:LRA=7", f)

    def test_invalid_duration_or_rate_fails_closed(self):
        with self.assertRaises(ValueError):
            adaptive_ambient_filter(0)
        with self.assertRaises(ValueError):
            adaptive_ambient_filter(20, 44100)

    def test_release_policy_is_preserved(self):
        c = adaptive_ambient_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertFalse(c["changes_caption_copy"])

    def test_wrong_geometry_rejected(self):
        with self.assertRaises(ValueError):
            adaptive_ambient_contract(720, 1280)


if __name__ == "__main__":
    unittest.main()
