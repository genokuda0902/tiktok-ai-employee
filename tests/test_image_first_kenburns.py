import unittest
from video_engine.image_first_kenburns import MotionProfile

class MotionProfileTest(unittest.TestCase):
    def test_portrait_defaults(self):
        p = MotionProfile()
        self.assertEqual((p.width, p.height, p.fps), (1080, 1920, 30))
        p.validate()

    def test_zoom_guard(self):
        with self.assertRaises(ValueError):
            MotionProfile(max_zoom=1.08).validate()

if __name__ == "__main__":
    unittest.main()
