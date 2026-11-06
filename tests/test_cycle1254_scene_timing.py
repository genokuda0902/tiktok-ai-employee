import unittest
from quality.scene_timing import validate_scenes

class TestSceneTiming(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_scenes([(0,4,"入力"),(4,8,"整理"),(8,12,"結果")],12))
    def test_gap(self):
        with self.assertRaises(ValueError):
            validate_scenes([(0,4,"入力"),(5,12,"結果")],12)
    def test_missing_caption(self):
        with self.assertRaises(ValueError):
            validate_scenes([(0,12,"")],12)
    def test_duration(self):
        with self.assertRaises(ValueError):
            validate_scenes([(0,10,"結果")],12)

if __name__ == "__main__":
    unittest.main()
