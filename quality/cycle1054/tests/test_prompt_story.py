import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from prompt_story import render_frame,PALETTES,GENRES,CARDS
class TestStory(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(set(GENRES),set(PALETTES))
        for g in GENRES:self.assertEqual(render_frame(40,g).size,(1080,1270))
    def test_three_steps(self):self.assertEqual([x[1] for x in CARDS],['目的','条件','形式'])
    def test_frames_differ(self):
        self.assertNotEqual(render_frame(5).tobytes(),render_frame(70).tobytes())
    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError):render_frame(5,'fake')
    def test_out_of_range_fails(self):
        with self.assertRaises(ValueError):render_frame(87)
    def test_overlay_no_private_media(self):
        self.assertEqual(render_frame(20).mode,'RGBA')
if __name__=='__main__':unittest.main()
