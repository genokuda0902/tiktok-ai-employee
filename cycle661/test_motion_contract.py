"""Run with python -m unittest discover -s cycle661 -p 'test_*.py'."""
import unittest
from motion_contract import GENRES, FPS, WIDTH, HEIGHT, TOTAL_SECONDS, SCENE_ENDS, smoothstep, scene_at, dolly_zoom, global_progress, dissolve_alpha

class MotionContractTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES),10)
    def test_video_contract(self):
        self.assertEqual((WIDTH,HEIGHT,FPS),(1080,1920,30))
        self.assertEqual(int(TOTAL_SECONDS*FPS),468)
    def test_timeline(self):
        self.assertEqual(len(SCENE_ENDS),8)
        self.assertEqual(scene_at(0),0)
        self.assertEqual(scene_at(2.1),1)
        self.assertEqual(scene_at(15.59),7)
    def test_easing(self):
        self.assertEqual(smoothstep(0),0)
        self.assertEqual(smoothstep(1),1)
        self.assertTrue(0<smoothstep(.25)<smoothstep(.75)<1)
    def test_zoom(self):
        self.assertAlmostEqual(dolly_zoom(0),1)
        self.assertAlmostEqual(dolly_zoom(1),1.028)
    def test_progress(self):
        self.assertGreater(global_progress(200),global_progress(10))
        self.assertEqual(global_progress(467),1)
    def test_dissolve(self):
        self.assertAlmostEqual(dissolve_alpha(4/FPS),0)
        self.assertAlmostEqual(dissolve_alpha(0),1)

if __name__=="__main__":unittest.main()
