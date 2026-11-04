import unittest
from src.caption_safe_area import CaptionBox, validate_caption_boxes

class CaptionSafeAreaTests(unittest.TestCase):
    def test_safe_caption(self):
        self.assertTrue(validate_caption_boxes([CaptionBox(110, 1200, 860, 160)]))
    def test_bottom_ui_overlap_rejected(self):
        with self.assertRaisesRegex(ValueError, "unsafe"):
            validate_caption_boxes([CaptionBox(110, 1530, 860, 120)])
    def test_right_edge_rejected(self):
        with self.assertRaisesRegex(ValueError, "unsafe"):
            validate_caption_boxes([CaptionBox(400, 1000, 700, 100)])
    def test_missing_boxes_rejected(self):
        with self.assertRaises(ValueError):
            validate_caption_boxes([])
    def test_invalid_geometry_rejected(self):
        with self.assertRaises(ValueError):
            validate_caption_boxes([CaptionBox(110, 1000, -1, 120)])
    def test_empty_safe_area_rejected(self):
        with self.assertRaises(ValueError):
            validate_caption_boxes([CaptionBox(1, 1, 1, 1)], bottom_margin=1800)
if __name__ == "__main__":
    unittest.main()
