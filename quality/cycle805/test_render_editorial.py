import json
import tempfile
import unittest
from pathlib import Path
from render_editorial import (W,H,FPS,SAFE,GENRES,THEMES,TITLES,TAGS,
                             render_slide,get_timing,frame_counts)

class EditorialTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(set(GENRES),set(THEMES))
    def test_eight_unique_scenes(self):
        self.assertEqual(len(TITLES),8)
        self.assertEqual(len(TAGS),8)
        self.assertEqual(len(set(TAGS)),8)
    def test_safe_area(self):
        self.assertGreaterEqual(SAFE[0],100)
        self.assertGreaterEqual(SAFE[1],100)
        self.assertGreaterEqual(SAFE[3],250)
    def test_timing_avoids_accumulated_drift(self):
        times=[3.355,3.085,3.025,3.285,3.265,3.36,2.97,3.495]
        counts=frame_counts(times)
        self.assertEqual(sum(counts),round(sum(times)*FPS))
        self.assertTrue(all(n>50 for n in counts))
    def test_reject_wrong_voice_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'timing.json';p.write_text(json.dumps({'genre':'ai_work','sentences':[]}))
            with self.assertRaises(ValueError):get_timing(p)
    def test_scene_renders_original_pixels(self):
        im=render_slide(0,'仕事ができる人は、質問が違う。')
        self.assertEqual(im.size,(W,H))
        self.assertNotEqual(im.getpixel((540,520)),im.getpixel((540,1050)))
    def test_scene_8_caption_and_theme(self):
        im=render_slide(7,'小さな改善が、強いチームをつくる。')
        self.assertEqual(im.size,(W,H))
    def test_all_ten_genre_layouts(self):
        for genre in GENRES:
            with self.subTest(genre=genre):
                self.assertEqual(render_slide(1,'まず、目指すゴールを確認する。',genre).size,(W,H))

if __name__=='__main__':unittest.main()
