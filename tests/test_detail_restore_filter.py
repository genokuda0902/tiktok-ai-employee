import unittest
from video_engine.detail_restore import ffmpeg_filter

class TestDetailRestore(unittest.TestCase):
    def test_default(self):
        self.assertEqual(ffmpeg_filter(), "unsharp=5:5:0.28:3:3:0.0")

    def test_bounds(self):
        for value in (-0.01, 0.41):
            with self.assertRaises(ValueError):
                ffmpeg_filter(value)

if __name__ == "__main__":
    unittest.main()
