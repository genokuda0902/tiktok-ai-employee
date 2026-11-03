import unittest
from src.cycle1194_caption_contrast import caption_contrast_filter

class CaptionContrastTests(unittest.TestCase):
    def test_region(self):
        self.assertIn("y=1370", caption_contrast_filter())
    def test_reject_opacity(self):
        with self.assertRaises(ValueError):
            caption_contrast_filter(opacity=0.8)
    def test_reject_size(self):
        with self.assertRaises(ValueError):
            caption_contrast_filter(width=0)
if __name__ == "__main__":
    unittest.main()
