import unittest
from timing import ease_out

class TimingTests(unittest.TestCase):
    def test_endpoints(self):
        self.assertEqual(ease_out(0), 0)
        self.assertEqual(ease_out(1), 1)

    def test_monotonic(self):
        values = [ease_out(i / 100) for i in range(101)]
        self.assertTrue(all(a <= b for a, b in zip(values, values[1:])))

if __name__ == '__main__':
    unittest.main()
