import unittest
from quality.camera_motion import camera_filter

class TestCameraMotion(unittest.TestCase):
    def test_native_portrait(self):
        self.assertIn("1080x1920", camera_filter())
    def test_zoom(self):
        self.assertIn("zoompan", camera_filter())
    def test_reject_bad_duration(self):
        with self.assertRaises(ValueError):
            camera_filter(0)

if __name__ == "__main__":
    unittest.main()
