import unittest
from upper_denoise import video_filter

class DenoiseTests(unittest.TestCase):
    def test_lower_caption_protection(self):
        self.assertIn("crop=iw:1350:0:0", video_filter())
    def test_audio_not_in_filter(self):
        self.assertNotIn("[0:a]", video_filter())
    def test_invalid_height(self):
        with self.assertRaises(ValueError): video_filter(1920)

if __name__ == "__main__":
    unittest.main()
