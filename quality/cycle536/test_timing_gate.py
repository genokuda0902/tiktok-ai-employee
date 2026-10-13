import unittest
from quality.cycle536.timing_gate import validate_timeline, validate_safe_rect

class TestSceneGeometry(unittest.TestCase):
    def test_frame_count(self):
        self.assertEqual(validate_timeline(),75)
    def test_invalid_duration(self):
        with self.assertRaises(ValueError):validate_timeline(6.0,20.5,30)
    def test_safe_text(self):
        self.assertTrue(validate_safe_rect((120,400,900,1300)))
        self.assertFalse(validate_safe_rect((10,400,900,1300)))

if __name__=='__main__':unittest.main()
