import unittest

from video_engine.ambient_bed import ambient_bed_filter, mix_contract


class AmbientBedTests(unittest.TestCase):
    def test_filter_is_synthesized_and_band_limited(self):
        f = ambient_bed_filter(20.0)
        self.assertIn("anoisesrc=color=pink", f)
        self.assertIn("highpass=f=180", f)
        self.assertIn("lowpass=f=1800", f)

    def test_invalid_duration_or_rate_fails_closed(self):
        with self.assertRaises(ValueError):
            ambient_bed_filter(0)
        with self.assertRaises(ValueError):
            ambient_bed_filter(20, 44100)

    def test_contract_preserves_zero_cost_manual_release(self):
        c = mix_contract()
        self.assertTrue(c["zero_cost"])
        self.assertFalse(c["external_music_asset_required"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertLess(c["bed_weight"], c["narration_weight"])

    def test_wrong_geometry_rejected(self):
        with self.assertRaises(ValueError):
            mix_contract(720, 1280)


if __name__ == "__main__":
    unittest.main()
