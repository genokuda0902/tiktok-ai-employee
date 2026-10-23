import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from hook_card import draw_frame,load_genres,export_frames,FRAMES
ROOT=Path(__file__).parent
class TestHook(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(load_genres(ROOT/"genres.json")),10)
    def test_size(self): self.assertEqual(draw_frame().size,(1080,1360))
    def test_motion(self): self.assertNotEqual(draw_frame(0).tobytes(),draw_frame(FRAMES-1).tobytes())
    def test_unsupported_genre_guard(self):
        with self.assertRaises(ValueError):
            export_frames("/tmp/cycle782-ignored",ROOT/"genres.json","美容・身だしなみ")
    def test_invalid_frame(self):
        with self.assertRaises(ValueError):draw_frame(-1)
if __name__=="__main__":unittest.main()
