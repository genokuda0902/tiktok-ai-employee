"""Offline layout contract tests for 540x960 portrait CTA."""
import unittest

SAFE = (26, 118, 432, 766)
BOXES = {
    'brand': (28, 120, 428, 160),
    'heading': (28, 174, 428, 231),
    'steps': (28, 246, 428, 421),
    'evidence': (28, 440, 428, 644),
    'formula': (28, 659, 428, 710),
    'cta': (28, 721, 428, 764),
}

class SafeZoneTests(unittest.TestCase):
    def test_all_critical_boxes_inside_safe_region(self):
        x0, y0, x1, y1 = SAFE
        for a, b, c, d in BOXES.values():
            self.assertTrue(x0 <= a < c <= x1)
            self.assertTrue(y0 <= b < d <= y1)

if __name__ == '__main__':
    unittest.main()
