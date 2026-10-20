import unittest
from story_contract import SCENE_TITLES, SCENE_SUBTITLES, validate_scenes, sales_proof

class TestStoryboard(unittest.TestCase):
    def test_scene_count(self):
        self.assertTrue(validate_scenes(SCENE_TITLES, SCENE_SUBTITLES))
    def test_sales(self):
        self.assertEqual(sales_proof()['total'], 720000)

if __name__ == '__main__':
    unittest.main()
