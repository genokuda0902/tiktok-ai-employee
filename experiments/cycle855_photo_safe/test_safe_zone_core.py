import unittest
from safe_zone_core import *

class TestSafeZones(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(PALETTES),10)
    def test_valid(self): self.assertTrue(validate())
    def test_all_semantic_boxes(self):
        for b in CRITICAL: self.assertTrue(b.safe(),b)
    def test_captions_above_bottom_ui(self): self.assertLessEqual(CAPTION.bottom,1260)
    def test_caption_avoids_buttons(self): self.assertLessEqual(CAPTION.right,780)
    def test_old_caption_location_fails(self): self.assertFalse(Box(130,1450,760,1620).safe())
    def test_button_collision_fails(self): self.assertFalse(Box(740,850,850,1000).safe())
    def test_edge_collision_fails(self): self.assertFalse(Box(80,280,500,400).safe())
    def test_bottom_collision_fails(self): self.assertFalse(Box(130,1080,760,1300).safe())
    def test_caption_height(self): self.assertGreaterEqual(CAPTION.bottom-CAPTION.top,150)

if __name__=='__main__':unittest.main()
