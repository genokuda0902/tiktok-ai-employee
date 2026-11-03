import unittest
from src.quality_scene_fades import fade_filter

class SceneFadeTests(unittest.TestCase):
    def test_three_cuts(self):
        s=fade_filter([3,6,20.5])
        self.assertEqual(s.count("fade=t=out"),3)
        self.assertIn("st=20.380",s)
    def test_sorted(self):
        self.assertEqual(fade_filter([6,3]),fade_filter([3,6]))
    def test_overlap(self):
        with self.assertRaises(ValueError): fade_filter([3,3.1])
    def test_duration(self):
        with self.assertRaises(ValueError): fade_filter([3],0.6)

if __name__=="__main__": unittest.main()
