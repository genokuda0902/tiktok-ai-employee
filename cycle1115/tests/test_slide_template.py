import importlib.util
import unittest
from pathlib import Path

p=Path(__file__).resolve().parents[1]/'code'/'slide_template.py'
s=importlib.util.spec_from_file_location('slide_template',p)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)

class TestOriginalJapaneseSlides(unittest.TestCase):
    def test_genre_count(self):
        self.assertEqual(len(m.GENRES),10)
    def test_scene_count(self):
        self.assertEqual(len(m.SCENES),8)
        self.assertEqual(len(m.TIMES),9)
        self.assertAlmostEqual(m.TIMES[-1],22.5)
    def test_reveal_timing(self):
        for i,t in enumerate(m.REVEALS):
            self.assertTrue(m.TIMES[i]+.1<t<m.TIMES[i+1]-.1)
    def test_all_genres_render(self):
        for genre in m.GENRES:
            im=m.slide(0,genre)
            self.assertEqual(im.size,(1080,1920))
            self.assertEqual(im.mode,'RGB')
    def test_japanese_caption_reveal(self):
        before=m.slide(3,reveal=False)
        after=m.slide(3,reveal=True)
        self.assertNotEqual(before.crop((110,1520,820,1600)).tobytes(),
                            after.crop((110,1520,820,1600)).tobytes())
    def test_app_safe_zones(self):
        before=m.slide(4,reveal=False)
        after=m.slide(4,reveal=True)
        self.assertEqual(before.crop((900,1360,1080,1650)).tobytes(),
                         after.crop((900,1360,1080,1650)).tobytes())
        self.assertEqual(before.crop((0,1650,1080,1920)).tobytes(),
                         after.crop((0,1650,1080,1920)).tobytes())
    def test_fail_closed(self):
        with self.assertRaises(ValueError):m.slide(0,'unknown')
        with self.assertRaises(ValueError):m.slide(8)
    def test_distinct_scenes(self):
        self.assertNotEqual(m.slide(0).tobytes(),m.slide(1).tobytes())

if __name__=='__main__':unittest.main()
