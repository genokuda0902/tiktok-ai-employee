import unittest
from hook_overlay import hook_filter
class HookOverlayTest(unittest.TestCase):
    def test_overlay_is_time_limited(self):
        self.assertIn('between(t,0,2.8)',hook_filter())
    def test_invalid_duration(self):
        for value in [-1,0,5.1]:
            with self.assertRaises(ValueError): hook_filter(value)
    def test_uses_japanese_hook(self):
        self.assertIn('AIの回答、そのまま使う？',hook_filter())
if __name__=='__main__': unittest.main()
