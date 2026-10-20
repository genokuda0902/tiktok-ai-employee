"""Unit tests for cycle721 safe-area settings; no network or posting."""
import unittest
from pathlib import Path
import importlib.util, sys
p = Path(__file__).resolve().parents[1] / "quality/cycle721/safe_zone.py"
s = importlib.util.spec_from_file_location("safe_zone_cycle721", p)
m = importlib.util.module_from_spec(s)
sys.modules[s.name] = m
s.loader.exec_module(m)

class SafeZoneTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRE_COLORS), 10)

    def test_caption_card_safe(self):
        self.assertTrue(m.is_inside_assumed_safe_zone())

    def test_right_margin(self):
        self.assertFalse(m.is_inside_assumed_safe_zone(m.Rect(901, 1400, 1, 100)))

    def test_bottom_margin(self):
        self.assertFalse(m.is_inside_assumed_safe_zone(m.Rect(56, 1500, 840, 106)))

    def test_valid_cues(self):
        cues = [{"phrases":["あ","い"],"start_s":i*2.5,
                 "boundary_s":i*2.5+1,"end_s":(i+1)*2.5} for i in range(8)]
        self.assertTrue(m.validate_cues(cues))
        cues[3]["start_s"] += 0.1
        with self.assertRaises(ValueError):
            m.validate_cues(cues)

if __name__ == "__main__":
    unittest.main()
