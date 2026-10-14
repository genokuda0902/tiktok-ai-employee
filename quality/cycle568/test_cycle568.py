import unittest
from render import validate_data, INPUT_VALUES, TOTAL, W, H, FPS, HOOK_SECONDS
class TestCycle568(unittest.TestCase):
    def test_verified_total(self):
        self.assertEqual(sum(INPUT_VALUES), TOTAL)
        self.assertEqual(TOTAL, 720)
        self.assertTrue(validate_data())
    def test_mismatch_fails(self):
        with self.assertRaises(ValueError):
            validate_data((120,150,200,250),700)
    def test_invalid_inputs_fail(self):
        with self.assertRaises(ValueError):
            validate_data((120,150,-1,451),720)
    def test_vertical(self):
        self.assertEqual((W,H,FPS), (1080,1920,30))
    def test_hook_duration(self):
        self.assertEqual(HOOK_SECONDS,2)
if __name__ == '__main__':
    unittest.main()
