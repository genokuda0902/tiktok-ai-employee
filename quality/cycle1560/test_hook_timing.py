import unittest
from hook_timing import Hook, hook_for_sum

class HookTests(unittest.TestCase):
    def test_boundaries(self):
        hook = Hook("sample")
        self.assertEqual(hook.opacity(-1), 0)
        self.assertEqual(hook.opacity(0), 1)
        self.assertAlmostEqual(hook.opacity(1), 0.5)
        self.assertEqual(hook.opacity(2), 0)
    def test_total(self):
        self.assertEqual(hook_for_sum((1000,2000,3000,4000)).text, "10,000 円")
    def test_invalid(self):
        with self.assertRaises(ValueError):
            hook_for_sum(())
if __name__ == "__main__":
    unittest.main()
