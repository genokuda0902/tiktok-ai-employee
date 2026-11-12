import unittest
from motion import frame_motion

class MotionTest(unittest.TestCase):
    def test_bounds(self):
        m = frame_motion(0, 12, 5, 0, 4)
        self.assertEqual(m.reveal, 0)
        self.assertGreater(m.progress, 0)
        self.assertEqual(frame_motion(59,12,5,3,4).progress, 1)
    def test_row(self):
        self.assertEqual(frame_motion(59,12,5,1,4).cursor_row, 2)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            frame_motion(60,12,5,0,4)
        with self.assertRaises(ValueError):
            frame_motion(0,0,5,0,4)

if __name__ == "__main__":
    unittest.main()
