"""Offline tests for crop-safe local browser footage and reusable genre configuration."""
import unittest
from quality_core import *

class QualityCoreTest(unittest.TestCase):
    def test_default_safe(self):self.assertTrue(validate_layout())
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:self.assertTrue(validate_layout(genre=genre))
    def test_bad_genre(self):
        with self.assertRaises(ValueError):validate_layout(genre='other')
    def test_crop_must_contain_all_ui(self):
        with self.assertRaises(ValueError):validate_layout(crop=(100,300,870,1050))
    def test_no_subtitle_collision(self):
        with self.assertRaises(ValueError):validate_layout(dest=(90,600,990,1540))
    def test_crop_bounds(self):
        with self.assertRaises(ValueError):validate_layout(crop=(-10,285,870,1135))
    def test_aspect_ratio(self):
        with self.assertRaises(ValueError):validate_layout(dest=(90,450,990,1200))
    def test_scenes(self):self.assertTrue(validate_scenes())
    def test_scene_gap(self):
        s=list(SCENES);s[2]=(6,8.45)
        with self.assertRaises(ValueError):validate_scenes(s)
    def test_duration(self):self.assertEqual(round(DURATION*FPS),691)
    def test_caption_beat_count(self):
        beats=[{'start':i*.9,'end':i*.9+.8,'text':'テスト'} for i in range(24)]
        self.assertTrue(validate_beats(beats))

if __name__=='__main__':unittest.main()
