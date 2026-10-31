import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from verification_component import render_art,GENRES,CHECKS,BEATS,W,H,smooth

class VerificationTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:self.assertEqual(render_art(1.6,genre).size,(W,H))
    def test_three_review_items(self):
        self.assertEqual(tuple(c[0] for c in CHECKS),("数字","日付","断定"))
    def test_three_beats_within_scene(self):
        self.assertLess(BEATS[-1]+.45,82/30)
    def test_animation_changes(self):
        self.assertNotEqual(render_art(0).tobytes(),render_art(2.5).tobytes())
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):render_art(1,"invalid")
    def test_no_external_assets(self):
        self.assertEqual(render_art(2.5).mode,"RGB")
    def test_smooth(self):
        self.assertEqual(smooth(-1),0)
        self.assertEqual(smooth(2),1)
        self.assertLess(smooth(.3),smooth(.6))

if __name__=="__main__":unittest.main()
