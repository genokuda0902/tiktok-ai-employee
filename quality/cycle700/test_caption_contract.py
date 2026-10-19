"""Offline contract tests for TikTok cycle700."""
import importlib.util
from pathlib import Path
import unittest
MODULE=Path(__file__).with_name("caption_contract.py")
spec=importlib.util.spec_from_file_location("caption_contract",MODULE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestCaptionContract(unittest.TestCase):
    def test_contract(self): self.assertTrue(m.validate())
    def test_ten_genres(self): self.assertEqual(len(m.GENRE_COLORS),10)
    def test_duration(self): self.assertEqual(sum(m.SCENE_FRAMES)/m.FPS,15.6)
    def test_scene_edges(self):
        self.assertEqual([m.scene_at(x) for x in (0,59,60,119,120,359,360,413,414,467)],
                         [0,0,1,1,2,5,6,6,7,7])
    def test_out_of_range(self):
        for x in (-1,468):
            with self.assertRaises(ValueError):m.scene_at(x)
    def test_full_caption_pairs(self):
        self.assertEqual(len(m.CAPTIONS),8)
        self.assertTrue(all(len(x)==2 for x in m.CAPTIONS))
    def test_safe_area(self):
        self.assertLessEqual(m.CAPTION_BAND[1],1536)
if __name__=="__main__":unittest.main()
