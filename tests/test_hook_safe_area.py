import unittest
from video_engine.quality.hook_safe_area import validate_hook_safe_area

class HookSafeAreaTests(unittest.TestCase):
    def test_valid_elements_pass(self):
        ok, errors = validate_hook_safe_area([{"important": True, "box": [90,250,810,800]}])
        self.assertTrue(ok); self.assertEqual([], errors)
    def test_right_rail_fails(self):
        ok, errors = validate_hook_safe_area([{"important": True, "box": [850,500,120,120]}])
        self.assertFalse(ok); self.assertIn("element_0_outside_safe_area", errors)
    def test_bottom_zone_fails(self):
        ok, errors = validate_hook_safe_area([{"important": True, "box": [100,1550,700,100]}])
        self.assertFalse(ok); self.assertIn("element_0_outside_safe_area", errors)
    def test_decoration_can_be_outside(self):
        ok, _ = validate_hook_safe_area([{"important": False, "box": [0,0,1080,1920]}])
        self.assertTrue(ok)
    def test_missing_fails(self):
        ok, errors = validate_hook_safe_area([])
        self.assertFalse(ok); self.assertIn("hook_elements_missing", errors)
