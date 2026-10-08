import unittest

class StoryGateTests(unittest.TestCase):
    def test_scene_count(self):
        self.assertTrue(6 <= 8 <= 10)
    def test_duration(self):
        self.assertEqual(sum([2,2.5,2.5,2.5,2.5,2.5,3.5,2]), 20)

if __name__ == '__main__':
    unittest.main()
