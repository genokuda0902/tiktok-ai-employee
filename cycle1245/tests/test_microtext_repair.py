import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import microtext_repair as m

class RepairTests(unittest.TestCase):
    def test_all_genres(self):
        for g in m.PALETTE:
            with self.subTest(genre=g):
                self.assertTrue(m.validate(g))
                self.assertIn('drawtext',m.filter_graph(g))
                self.assertIn(m.PALETTE[g],m.filter_graph(g))
    def test_reject_bad_genre(self):
        with self.assertRaises(ValueError):m.validate('unknown')
    def test_reject_resolution(self):
        with self.assertRaises(ValueError):m.validate('ai',720,1280)
    def test_reject_missing_font(self):
        with self.assertRaises(FileNotFoundError):m.validate('ai',font='/not/found.ttf')
    def test_time_confined_to_scene_two(self):
        self.assertGreater(m.START,3.0)
        self.assertLess(m.END,5.7)
    def test_rect_protects_subtitle_and_disclosure(self):
        x,y,w,h=m.RECT
        self.assertGreaterEqual(x,70)
        self.assertLessEqual(x+w,875)
        self.assertGreaterEqual(y,1230)
        self.assertLessEqual(y+h,1310)
        self.assertLess(y+h,1380)
    def test_audio_is_stream_copied(self):
        import inspect
        self.assertIn("'-c:a','copy'",inspect.getsource(m.render))
    def test_japanese_copy(self):
        self.assertIn('繰り返し',m.TEXT)
        self.assertIn('書き出す',m.TEXT)

if __name__=='__main__':unittest.main()
