import importlib.util
import math
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('scene_voice_leveler',Path(__file__).resolve().parents[1]/'src'/'scene_voice_leveler.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestSceneVoiceLeveler(unittest.TestCase):
    def test_ten_genre_profiles(self): self.assertEqual(len(m.GENRE_PROFILES),10)
    def test_genre_bounds(self):
        for p in m.GENRE_PROFILES.values():
            self.assertGreater(p['transition_ms'],0)
            self.assertLessEqual(p['max_adjust_db'],1.2)
    def test_db_gain(self): self.assertAlmostEqual(m.db_to_gain(6.0206),2,places=4)
    def test_gain_median(self): self.assertEqual(m.bounded_scene_adjustments([-20,-18,-16],2),[2,0,-2])
    def test_gain_caps(self): self.assertEqual(m.bounded_scene_adjustments([-30,-20,-10],1),[1,0,-1])
    def test_gain_rejects_nan(self):
        with self.assertRaises(ValueError):m.bounded_scene_adjustments([float('nan')])
    def test_gain_rejects_empty(self):
        with self.assertRaises(ValueError):m.bounded_scene_adjustments([])
    def test_transition_start(self): self.assertAlmostEqual(m.interpolate_db(2.8,[0,3,6],[0,2],.2),0)
    def test_transition_mid(self): self.assertAlmostEqual(m.interpolate_db(3.,[0,3,6],[0,2],.2),1)
    def test_transition_end(self): self.assertAlmostEqual(m.interpolate_db(3.1,[0,3,6],[0,2],.2),2)
    def test_invalid_edges(self):
        with self.assertRaises(ValueError):m.interpolate_db(1,[0,3,2],[0,1],.2)
    def test_mismatched_edges(self):
        with self.assertRaises(ValueError):m.interpolate_db(1,[0,3,6],[0],.2)
    def test_no_publish_methods(self):
        src=Path(m.__file__).read_text()
        for term in ['requests.post(', 'upload_file(', 'tiktok.publish(', 'git push']:
            self.assertNotIn(term,src)
    def test_scene_edges(self):
        self.assertEqual(len(m.SCENE_EDGES),9)
        self.assertEqual(m.SCENE_EDGES[0],0)
        self.assertTrue(all(a<b for a,b in zip(m.SCENE_EDGES,m.SCENE_EDGES[1:])))

if __name__=='__main__':unittest.main()
