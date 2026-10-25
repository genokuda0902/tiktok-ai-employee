import unittest
from experiments.cycle836.safe_zone import (
    SUBTITLE_CENTER_Y, LOWER_UI_START,
    subtitle_inside_safe_zone, move_ass_caption_center
)
class TestSafeZone(unittest.TestCase):
    def test_default_caption_estimate(self):
        self.assertTrue(subtitle_inside_safe_zone())
    def test_old_position_not_safe(self):
        self.assertFalse(subtitle_inside_safe_zone(center=1640))
    def test_ass_position_replacement(self):
        self.assertIn("pos(540,1395)",
                      move_ass_caption_center("pos(540,1640)"))
    def test_bottom_exclusion_starts_at_1536(self):
        self.assertEqual(LOWER_UI_START, 1536)
if __name__ == "__main__":
    unittest.main()
