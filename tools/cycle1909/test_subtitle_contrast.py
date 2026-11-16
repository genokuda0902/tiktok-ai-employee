import unittest
from subtitle_contrast import filtergraph

class TestSubtitleContrast(unittest.TestCase):
    def test_default_geometry(self):
        self.assertIn("y=1546:w=1080:h=202", filtergraph())
    def test_range(self):
        with self.assertRaises(ValueError):
            filtergraph(opacity=.8)
    def test_custom_dimensions(self):
        self.assertIn("w=720",filtergraph(720,1280))

if __name__ == "__main__":
    unittest.main()
