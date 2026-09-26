import unittest
from video_engine.clean_mobile_contrast import ffmpeg_filter, output_contract

class CleanMobileContrastTests(unittest.TestCase):
    def test_default_filter_is_subtle(self):
        self.assertEqual(ffmpeg_filter(), "eq=contrast=1.025:brightness=0.004:saturation=1.015")
    def test_rejects_aggressive_contrast(self):
        with self.assertRaises(ValueError):
            ffmpeg_filter(contrast=1.2)
    def test_delivery_contract(self):
        c = output_contract()
        self.assertEqual((c["width"], c["height"]), (1080, 1920))
        self.assertTrue(c["audio_passthrough"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertFalse(c["heavy_vignette_allowed"])

if __name__ == "__main__":
    unittest.main()
