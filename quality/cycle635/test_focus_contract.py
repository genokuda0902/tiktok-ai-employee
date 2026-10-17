import unittest
from focus_contract import FOCUS_REGIONS, focus_geometry
class FocusTest(unittest.TestCase):
    def test_safe_zone(self):
        for region in FOCUS_REGIONS.values():
            self.assertLess(region[3], 755)
    def test_progress(self):
        self.assertIsNone(focus_geometry("hook", 0.5))
        self.assertEqual(focus_geometry("select", 0)[1], 0)
        self.assertEqual(focus_geometry("proof", 1)[1], 1)
if __name__ == "__main__":
    unittest.main()
