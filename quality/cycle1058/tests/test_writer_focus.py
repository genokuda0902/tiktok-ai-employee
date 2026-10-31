import sys
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from real_writer_focus import PALETTES, START, COUNT, stage, render_frame

class TestWriterFocus(unittest.TestCase):
    def setUp(self):
        self.shot=Image.new('RGB',(1600,900),'white')
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES),10)
        for genre in PALETTES:
            self.assertEqual(render_frame(35,self.shot,genre).size,(1080,1270))
    def test_stage_boundaries(self):
        self.assertEqual([stage(x) for x in (0,27,28,58,59,88)],[0,0,1,1,2,2])
    def test_motion(self):
        self.assertNotEqual(render_frame(1,self.shot).tobytes(),render_frame(80,self.shot).tobytes())
    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError):render_frame(1,self.shot,'unapproved')
    def test_small_capture_rejected(self):
        with self.assertRaises(ValueError):render_frame(1,Image.new('RGB',(1000,600)))
    def test_frame_bounds(self):
        for x in (-1,COUNT):
            with self.assertRaises(ValueError):stage(x)
    def test_scene_and_caption_protection(self):
        self.assertEqual(START,520)
        self.assertEqual(COUNT,89)
        self.assertLess(1270,1280)
if __name__=='__main__':unittest.main()
