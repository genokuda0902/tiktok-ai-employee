import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from depth_component import GENRES,draw_depth_hero
from PIL import ImageChops,ImageStat

class DepthHeroTest(unittest.TestCase):
    def test_all_ten_genres(self):
        for genre in GENRES:
            self.assertEqual(draw_depth_hero(1.7,genre).size,(951,803))
    def test_animation_is_real(self):
        a,b=draw_depth_hero(0),draw_depth_hero(1.9)
        diff=ImageChops.difference(a,b)
        self.assertGreater(sum(ImageStat.Stat(diff).mean),10)
    def test_palette_changes(self):
        self.assertIsNotNone(ImageChops.difference(draw_depth_hero(1.5,"ai_work"),draw_depth_hero(1.5,"travel")).getbbox())
    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError): draw_depth_hero(.3,"unsupported")
    def test_review_only(self):
        import depth_component
        self.assertFalse(hasattr(depth_component,"post_to_tiktok"))
if __name__=="__main__": unittest.main()
